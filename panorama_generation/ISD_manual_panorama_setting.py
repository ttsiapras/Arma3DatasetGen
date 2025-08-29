"""
"""
import cv2
import numpy as np

def cylindrical_projection_physical(img, f):
    """
    Project image onto the outside of a cylinder using true 3D projection math.
    f: focal length (radius in pixels)
    """
    h, w = img.shape[:2]
    cx = w / 2
    cy = h / 2

    # Output canvas size matches input
    y_i, x_i = np.indices((h, w))
    x_c = x_i - w / 2
    y_c = y_i - h / 2

    theta = x_c / f
    h_ = y_c / f

    X = np.sin(theta)
    Y = h_
    Z = np.cos(theta)

    x_map = f * X / Z + cx
    y_map = f * Y / Z + cy

    map_x = x_map.astype(np.float32)
    map_y = y_map.astype(np.float32)

    return cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

def create_global_frame(images, overlap, f):
    """
    Projects and composites multiple images using cylindrical projection,
    blending based on black borders (only non-black pixels are copied).
    """
    projected_images = [cylindrical_projection_physical(img, f) for img in images]

    # Resize all images to the same height
    target_height = 400
    projected_images = [
        cv2.resize(img, (int(img.shape[1] * target_height / img.shape[0]), target_height))
        for img in projected_images
    ]

    widths = [img.shape[1] for img in projected_images]
    total_width = widths[0] + sum(w - overlap for w in widths[1:])
    height = target_height

    canvas = np.zeros((height, total_width, 3), dtype=np.uint8)
    x_offset = 0

    for img in projected_images:
        h, w = img.shape[:2]

        roi = canvas[0:h, x_offset:x_offset + w]
        mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 10  # True where not black
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)  # Make 3-channel

        # Blend: only copy non-black pixels
        roi[mask] = img[mask]
        canvas[0:h, x_offset:x_offset + w] = roi

        x_offset += w - overlap

    return canvas


# -------------------- Main Script --------------------

if __name__ == "__main__":
    import sys
    import glob
    import os
    # List your image paths here
    IMAGE_DIR = './images'

    image_paths = glob.glob(os.path.join(IMAGE_DIR, '*.png'))
    if len(image_paths) < 2:
        print("Error: Need at least two images to stitch.")
        exit()
    images = [cv2.resize(cv2.imread(p),(0,0),fx=0.6,fy=0.6)  for p in image_paths]
    if any(img is None for img in images):
        print("Error: One or more images failed to load.")
        sys.exit(1)

    overlap = 50  # pixels
    f = 500       # focal length
    last_overlap = overlap
    last_f = f

    print(f"Initial overlap: {overlap} px")
    print(f"Initial focal length (radius): {f}")

    while True:
        frame = create_global_frame(images, overlap, f)
        display = frame.copy()

        # Overlay current settings
        cv2.putText(display, f"Overlap: {overlap}px | Focal Length: {f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        screen_width = 1920
        display_h, display_w = frame.shape[:2]
        scale_factor = screen_width / display_w
        new_height = int(display_h * scale_factor)
        cv2.imshow("Cylindrical Panorama Viewer", cv2.resize(display, (screen_width, new_height)))
        key = cv2.waitKey(30) & 0xFF

        if key == 27:  # ESC
            break
        elif key == ord('a'):
            overlap += 5
        elif key == ord('s'):
            overlap = max(0, overlap - 5)
        elif key == ord('q'):
            f = max(50, f - 20)
        elif key == ord('w'):
            f += 20

        if overlap != last_overlap:
            #print(f"Overlap changed to: {overlap}px")
            last_overlap = overlap
        if f != last_f:
            #print(f"Focal length changed to: {f}")
            last_f = f
    cv2.destroyAllWindows()
