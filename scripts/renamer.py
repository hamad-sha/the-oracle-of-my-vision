from pathlib import Path
import shutil
input_directory = "C:/the-oracle-of-my-vision/dataset-testing/sampled"
output_directory = "C:/the-oracle-of-my-vision/dataset-testing/sampled_renamed"
answer = input("WARNING: MAKE SURE YOUR IMAGE INDEX HAS BEEN SET ACCORDING ESP IF MERGING IMAGES, TYPE YES OR NO")
if answer == "yes":
    pass
else:
    print("PRESS CONTROL Z TO AVOID DATA TERMINATION")
def organize_photos(input_directory, output_directory, prefix="ref"):
    input_path = Path(input_directory)
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    images = []
    for p in input_path.iterdir():
        if p.is_file() and p.suffix.lower() in valid_extensions:
            images.append(p)  # more efficeintly: images = [p for p in input_path.iterdir() if p.is_file() and p.suffix.lower() in valid_extensions] 
    if not images:
        print(f"No supported images found in {input_directory}.")
        return
    print(f"\n--- Found {len(images)} images. Processing... ---\n")
    index = 0
    for image_path in images:
        formatted_id_number = f"{index:03d}"
        clean_extension = image_path.suffix.lower()
        new_filename = f"ref_{formatted_id_number}{clean_extension}"
        destination_path = output_path / new_filename
        shutil.copy(image_path, destination_path)
        print(f"Copied {image_path.name} -> {new_filename}")
        index += 1
organize_photos(input_directory, output_directory)