"""
The Oracle of My Vision — Pairwise A/B Preference Labeling App
----------------------------------------------------------------
Run this file () and a local web UI opens
where you pick which of two images you prefer. Every decision is
logged to comparisons.jsonl automatically. Close the browser tab /
stop the script any time — your progress is saved after every click,
nothing is lost, and running it again later picks up where you left off.

Generated with Claude Sonnet 5, reviewed and implemented.
"""

import json
import random
from pathlib import Path

import gradio as gr

# ---- CONFIG: adjust these paths if your folders differ ----
DATASET_DIR = Path("C:/the-oracle-of-my-vision/pipeline/sampled_renamed")
LOG_PATH = Path("C:/the-oracle-of-my-vision/pipeline/results/comparisons.jsonl")


# ---------------- Backend logic (your existing functions) ----------------

def load_images():
    return [
        p.name for p in DATASET_DIR.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]


def load_shown_pairs():
    """Reads existing log, returns set of pairs already shown (order-independent)."""
    shown = set()
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as f:
            for line in f:
                entry = json.loads(line)
                shown.add(frozenset([entry["image_a"], entry["image_b"]]))
    return shown


def pick_new_pair(images, shown_pairs, max_attempts=50):
    for _ in range(max_attempts):
        a, b = random.sample(images, 2)
        if frozenset([a, b]) not in shown_pairs:
            return a, b
    return None  # pool likely exhausted of new unique pairs


def log_comparison(image_a, image_b, winner, review=""):
    entry = {"image_a": image_a, "image_b": image_b, "winner": winner, "review": review}
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_appearance_counts():
    """Diagnostic: how many times has each image appeared so far."""
    counts = {}
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as f:
            for line in f:
                entry = json.loads(line)
                counts[entry["image_a"]] = counts.get(entry["image_a"], 0) + 1
                counts[entry["image_b"]] = counts.get(entry["image_b"], 0) + 1
    return counts


def average_appearances():
    counts = get_appearance_counts()
    if not counts:
        return 0
    return sum(counts.values()) / len(counts)


def total_comparisons_logged():
    if not LOG_PATH.exists():
        return 0
    with open(LOG_PATH, "r") as f:
        return sum(1 for _ in f)


# ---------------- Gradio UI wiring ----------------

# Load the pool once at startup
all_images = load_images()
if len(all_images) < 2:
    raise RuntimeError(f"Need at least 2 images in {DATASET_DIR}, found {len(all_images)}.")

shown_pairs_cache = load_shown_pairs()


def get_status_text():
    total = total_comparisons_logged()
    avg = average_appearances()
    return f"**Comparisons logged: {total}**  |  Avg. appearances per image: {avg:.1f}  |  Pool size: {len(all_images)}"


def new_round():
    """Picks a fresh pair and returns their file paths + updated status text."""
    pair = pick_new_pair(all_images, shown_pairs_cache)
    if pair is None:
        return None, None, "No new unique pairs left to show — pool exhausted at current size.", "", ""
    a, b = pair
    path_a = str(DATASET_DIR / a)
    path_b = str(DATASET_DIR / b)
    return path_a, path_b, get_status_text(), a, b


def choose_winner(winner_side, image_a_name, image_b_name, review_text):
    """Called when user clicks 'A' or 'B'. Logs the result, then serves the next pair."""
    if image_a_name is None or image_b_name is None:
        # nothing to log yet (e.g. app just opened) — just serve a pair
        return new_round() + ("",)

    winner_filename = image_a_name if winner_side == "A" else image_b_name
    log_comparison(image_a_name, image_b_name, winner_filename, review_text)
    shown_pairs_cache.add(frozenset([image_a_name, image_b_name]))

    path_a, path_b, status, a, b = new_round()
    return path_a, path_b, status, a, b, ""  # last "" clears the review textbox


with gr.Blocks(title="The Oracle of My Vision — A/B Preference Labeling") as demo:
    gr.Markdown("## The Oracle of My Vision\n### Which photo do you prefer?")
    status_display = gr.Markdown(get_status_text())

    # Hidden state: track which filenames are currently displayed
    image_a_state = gr.State(None)
    image_b_state = gr.State(None)

    with gr.Row():
        img_a = gr.Image(label="A", type="filepath", height=400)
        img_b = gr.Image(label="B", type="filepath", height=400)

    review_box = gr.Textbox(
        label="Optional: why do you prefer one? (saved for future use, not required)",
        placeholder="e.g. rule of thirds, better lighting, stronger subject...",
    )

    with gr.Row():
        btn_a = gr.Button("Prefer A", variant="primary")
        btn_b = gr.Button("Prefer B", variant="primary")

    # Wire buttons: clicking either updates state, logs the choice, loads the next pair
    btn_a.click(
        fn=lambda a, b, r: choose_winner("A", a, b, r),
        inputs=[image_a_state, image_b_state, review_box],
        outputs=[img_a, img_b, status_display, image_a_state, image_b_state, review_box],
    )
    btn_b.click(
        fn=lambda a, b, r: choose_winner("B", a, b, r),
        inputs=[image_a_state, image_b_state, review_box],
        outputs=[img_a, img_b, status_display, image_a_state, image_b_state, review_box],
    )

    # Load the very first pair when the app opens
    demo.load(
        fn=new_round,
        inputs=None,
        outputs=[img_a, img_b, status_display, image_a_state, image_b_state],
    )

if __name__ == "__main__":
    demo.launch(allowed_paths=[str(DATASET_DIR)])