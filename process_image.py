from rembg import remove
from PIL import Image, ImageOps
import numpy as np
import cv2
import os

def process_image(input_path, output_path, size=1000):
    # Step 1: Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)

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
    cropped.thumbnail((size * 0.9, size * 0.9), Image.LANCZOS)  # scale down if needed

    # Step 5: Center on white background
    final_img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    paste_x = (size - cropped.width) // 2
    paste_y = (size - cropped.height) // 2
    final_img.paste(cropped, (paste_x, paste_y), cropped)

    # Step 6: Save final image
    final_img.convert("RGB").save(output_path, "JPEG")

    # Cleanup
    os.remove("temp.png")

    print(f"Processed: {output_path}")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python process_image.py input.jpg output.jpg")
    else:
        process_image(sys.argv[1], sys.argv[2])
