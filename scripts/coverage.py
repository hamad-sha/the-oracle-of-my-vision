"""
Quick diagnostic: checks how many times each image has appeared across
all logged comparisons so far. Run this any time during labeling to see
coverage — no need to stop your Gradio session first.
"""

import json
from pathlib import Path

LOG_PATH = Path("C:/the-oracle-of-my-vision/pipeline/results/comparisons.jsonl")  # adjust if needed


def get_appearance_counts():
    counts = {}
    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            counts[entry["image_a"]] = counts.get(entry["image_a"], 0) + 1
            counts[entry["image_b"]] = counts.get(entry["image_b"], 0) + 1
    return counts


def report():
    counts = get_appearance_counts()
    if not counts:
        print("No comparisons logged yet.")
        return

    values = list(counts.values())
    avg = sum(values) / len(values)

    print(f"Images with at least 1 appearance: {len(counts)}")
    print(f"Min appearances: {min(values)}")
    print(f"Max appearances: {max(values)}")
    print(f"Average appearances: {avg:.2f}")

    # flag the least-covered images specifically — useful to know which ones need more comparisons
    sorted_by_count = sorted(counts.items(), key=lambda x: x[1])
    print("\nLeast-compared images (bottom 10):")
    for name, count in sorted_by_count[:10]:
        print(f"  {name}: {count}")


if __name__ == "__main__":
    report()