import torch
import torch.nn.functional as F
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

# 1. Device Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Load Vision Transformer
model_name = "google/vit-base-patch16-224"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
model.eval()

# 3. Helper Function to Get Embedding
def get_image_embedding(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        # Normalize the embedding so its vector length is 1
        embedding = outputs.pooler_output
        normalized_embedding = F.normalize(embedding, p=2, dim=1)
    return normalized_embedding

# 4. Create Two Test Images
# Image A: Deep Purple
image_a = Image.new("RGB", (500, 500), color=(130, 80, 200))

# Image B: Light Blue
image_b = Image.new("RGB", (500, 500), color=(100, 200, 255))

# 5. Extract Embeddings on GPU
emb_a = get_image_embedding(image_a)
emb_b = get_image_embedding(image_b)

# 6. Cosine Similarity
similarity = torch.mm(emb_a, emb_b.T).item()

print("--- Stage 3 Complete ---")
print(f"Device: {emb_a.device}")
print(f"Embedding A Shape: {emb_a.shape}")
print(f"Embedding B Shape: {emb_b.shape}")
print(f"Cosine Similarity Score: {similarity:.4f}")