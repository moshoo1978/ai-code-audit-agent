import cv2
import numpy as np
import os
from PIL import Image

def generate_plan_diff(image_path_old, image_path_new, output_diff_path="output_data/diff_overlay.png"):
    """
    Compares two drawing sheet images, aligns them, and highlights visual changes:
    - RED: Removed geometry (Present in Old, missing in New)
    - GREEN: Added geometry (New in Revised drawing)
    - BLUE/DARK: Unchanged geometry
    """
    os.makedirs(os.path.dirname(output_diff_path), exist_ok=True)

    # Load images in grayscale
    img_old = cv2.imread(image_path_old, cv2.IMREAD_GRAYSCALE)
    img_new = cv2.imread(image_path_new, cv2.IMREAD_GRAYSCALE)

    if img_old is None or img_new is None:
        raise FileNotFoundError("Could not read one or both input plan images for diffing.")

    # Resize new image to match old image dimensions if needed
    if img_old.shape != img_new.shape:
        img_new = cv2.resize(img_new, (img_old.shape[1], img_old.shape[0]))

    # Threshold images to pure binary (black lines on white background)
    _, thresh_old = cv2.threshold(img_old, 200, 255, cv2.THRESH_BINARY_INV)
    _, thresh_new = cv2.threshold(img_new, 200, 255, cv2.THRESH_BINARY_INV)

    # Calculate additions and deletions
    added = cv2.subtract(thresh_new, thresh_old)
    removed = cv2.subtract(thresh_old, thresh_new)
    unchanged = cv2.bitwise_and(thresh_old, thresh_new)

    # Create 3-channel RGB overlay canvas (White background)
    diff_rgb = np.ones((img_old.shape[0], img_old.shape[1], 3), dtype=np.uint8) * 255

    # Draw Unchanged lines in Dark Gray/Black
    diff_rgb[unchanged > 0] = [50, 50, 50]

    # Draw Added geometry in Green (BGR format for OpenCV: [B, G, R])
    diff_rgb[added > 0] = [0, 220, 0]

    # Draw Removed geometry in Bright Red
    diff_rgb[removed > 0] = [0, 0, 255]

    # Save highlighted overlay
    cv2.imwrite(output_diff_path, diff_rgb)
    return output_diff_path