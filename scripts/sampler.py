import csv
import random
import shutil
from pathlib import Path
SOURCE_DIR = Path("C:/the-oracle-of-my-vision/pipeline/source_images")   # full AVA pool
STAGING_DIR = Path("C:/the-oracle-of-my-vision/pipeline/sampled")         # newly sampled, pre-rename
TRACKING_CSV = Path("C:/the-oracle-of-my-vision/pipeline/extracted_log.csv")

def load_extracted_filenames():
    """Reads the CSV and returns a set of source filenames already extracted before."""
    if not TRACKING_CSV.exists():
        return set()
    with open(TRACKING_CSV, "r", newline="") as f:
        reader = csv.DictReader(f)
        return {row["source_filename"] for row in reader}

def log_extracted_filenames(filenames):
    """Appends newly extracted filenames to the CSV so future runs skip them."""
    file_exists = TRACKING_CSV.exists()
    with open(TRACKING_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["source_filename"])  # header, only written once
        for name in filenames:
            writer.writerow([name])

def sample_new_images(sample_size, seed=42):
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    already_extracted = load_extracted_filenames()

    available = [
        p for p in SOURCE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in valid_extensions
        and p.name not in already_extracted
    ]

    if len(available) < sample_size:
        print(f"Only {len(available)} unextracted images remain — requested {sample_size}.")
        return

    random.seed(seed)
    chosen = random.sample(available, sample_size)

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    for p in chosen:
        shutil.copy(p, STAGING_DIR / p.name)

    log_extracted_filenames([p.name for p in chosen])
    print(f"Sampled {sample_size} new images into {STAGING_DIR}")

sample_new_images(sample_size=200)
#Generated with Claude Sonnet 5, tested and implemented.  