import gradio as gr
import json
import os
import uuid

DATASET_PATH = "dataset/preferences.json"
os.makedirs("dataset", exist_ok=True)
os.makedirs("dataset/images", exist_ok=True)

def save_preference(img_a, img_b, choice, rationale):
    if img_a is None or img_b is None:
        return "Error: Please provide both Image A and Image B."
    
    uid = str(uuid.uuid4())[:8]
    path_a = f"dataset/images/{uid}_a.jpg"
    path_b = f"dataset/images/{uid}_b.jpg"
    
    img_a.save(path_a)
    img_b.save(path_b)
    
    record = {
        "id": uid,
        "image_a": path_a,
        "image_b": path_b,
        "chosen": choice,
        "rationale": rationale if rationale else "No rationale provided."
    }
    
    data = []
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
                
    data.append(record)
    
    with open(DATASET_PATH, "w") as f:
        json.dump(data, f, indent=4)
        
    return f"✅ Saved successfully! Total pairs in dataset: {len(data)}"

with gr.Blocks(title="Visual Preference Collector") as demo:
    gr.Markdown("# Personal Aesthetic Preference Collector")
    gr.Markdown("Upload two images side-by-side, choose your preferred one, and write down *why* (lighting, composition, mood, etc.).")
    
    with gr.Row():
        with gr.Column():
            img_a_input = gr.Image(type="pil", label="Image A")
        with gr.Column():
            img_b_input = gr.Image(type="pil", label="Image B")
            
    rationale_input = gr.Textbox(
        label="Your Rationale (Why do you prefer one over the other?)", 
        placeholder="e.g., Image A has cleaner framing and better shadow contrast...",
        lines=3
    )
    
    with gr.Row():
        btn_a = gr.Button("Prefer Image A 👈", variant="primary", scale=1)
        btn_b = gr.Button("Prefer Image B 👉", variant="primary", scale=1)
        
    output_status = gr.Textbox(label="Status Log", interactive=False)
    
    btn_a.click(
        fn=lambda a, b, r: save_preference(a, b, "image_a", r), 
        inputs=[img_a_input, img_b_input, rationale_input], 
        outputs=output_status
    )
    btn_b.click(
        fn=lambda a, b, r: save_preference(a, b, "image_b", r), 
        inputs=[img_a_input, img_b_input, rationale_input], 
        outputs=output_status
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)