from rembg import remove
from PIL import Image
import numpy as np
import cv2
import os

def process_image(input_path, output_path, size=1000):
    # Step 0: Validate input image
    try:
        img_test = Image.open(input_path)
        img_test.verify()
    except Exception:
        raise ValueError("Invalid or corrupted image file.")

    # Step 1: Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)

    if output_data is None:
        raise ValueError("Background removal failed. The image might be unsupported or corrupt.")

    with open('temp.png', 'wb') as o:
        o.write(output_data)

    # Step 2: Open image and convert to RGBA
    img = Image.open('temp.png').convert("RGBA")

    # Step 3: Convert to OpenCV format to find bounding box
    cv_img = np.array(img)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    x, y, w, h = cv2.boundingRect(thresh)

    # Step 4: Crop and resize proportionally
    cropped = img.crop((x, y, x + w, y + h))
    cropped.thumbnail((size * 0.9, size * 0.9), Image.LANCZOS)

    # Step 5: Center on white background
    final_img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    paste_x = (size - cropped.width) // 2
    paste_y = (size - cropped.height) // 2
    final_img.paste(cropped, (paste_x, paste_y), cropped)

    # Step 6: Save final image in format based on output extension
    ext = os.path.splitext(output_path)[1].lower()
    if ext == '.png':
        final_img.save(output_path, 'PNG')
    elif ext == '.webp':
        final_img.save(output_path, 'WEBP')
    else:
        final_img.convert("RGB").save(output_path, "JPEG")

    # Cleanup
    os.remove("temp.png")

    print(f"Processed: {output_path}")

# Optional CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python process_image.py input.jpg output.jpg")
    else:
        process_image(sys.argv[1], sys.argv[2])

def process_directory(input_dir, output_dir, size=1000):
    supported_exts = ('.jpg', '.jpeg', '.png', '.webp')
    processed = 0
    skipped = 0

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_exts):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            try:
                process_image(input_path, output_path, size)
                processed += 1
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                skipped += 1

    return processed, skipped
