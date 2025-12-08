import cv2
import numpy as np
import os
import sys

def remove_chromakey(image_path, output_path):
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    mask_fg = cv2.inRange(hsv, lower_green, upper_green)

    mask_fg = cv2.bitwise_not(mask_fg)

    mask_fg = cv2.erode(mask_fg, np.ones((3, 3), np.uint8), iterations=1)
    mask_fg = cv2.dilate(mask_fg, np.ones((3, 3), np.uint8), iterations=1)

    result = cv2.bitwise_and(img, img, mask=mask_fg)

    b_channel, g_channel, r_channel = cv2.split(result)
    alpha_channel = mask_fg
    
    bgra_image = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    cv2.imwrite(output_path, bgra_image)
    print(f"Chromakey background removed image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chromakey_remover.py <image_file_path>")
        print("Example: python chromakey_remover.py my_chromakey_shot.jpg")
        sys.exit(1)

    input_file = sys.argv[1]
    
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_chroma_removed.png"

    remove_chromakey(input_file, output_file)