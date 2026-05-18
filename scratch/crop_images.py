from PIL import Image
import os

def crop_and_split():
    # Source image path
    src_path = r"C:/Users/scsof/.gemini/antigravity/brain/tempmediaStorage/media__1779058580915.png"
    dest_dir = r"c:\Users\scsof\Downloads\Inspector_1-main\Inspector_1-main\inspector-frontend\public\images"
    
    print("Opening source image...")
    img = Image.open(src_path)
    width, height = img.size
    print(f"Dimensions: {width}x{height}")
    
    # Split down the middle
    mid_x = width // 2
    
    # Left crop: Hiding Eyes
    print("Cropping left side (hiding eyes)...")
    left_box = (0, 0, mid_x, height)
    left_img = img.crop(left_box)
    
    # Right crop: Crossed Hands
    print("Cropping right side (crossed hands)...")
    right_box = (mid_x, 0, width, height)
    right_img = img.crop(right_box)
    
    # Save as PNG
    left_dest = os.path.join(dest_dir, "hiding_eyes.png")
    right_dest = os.path.join(dest_dir, "crossed_hands.png")
    
    # Ensure dest_dir exists
    os.makedirs(dest_dir, exist_ok=True)
    
    left_img.save(left_dest, "PNG")
    right_img.save(right_dest, "PNG")
    
    print(f"Saved: {left_dest}")
    print(f"Saved: {right_dest}")

if __name__ == "__main__":
    crop_and_split()
