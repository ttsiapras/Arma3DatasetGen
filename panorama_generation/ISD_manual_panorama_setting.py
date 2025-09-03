"""
This Script performs a culindrical projection anf offset to mulilple images that are part of a panorama.
Ther images must be in the correct order for the script to create a consise panorama.
The user can use 'q' and 'w' to change the "Focal length" for the cylindrical projection
and then the 'a' and 's' to change the offset between the images.

This works only for images that only exibit a rotation around a vertical axis intercepting the optical center.

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
    target_height = 1024
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
runfor = "PHOTOS"

# PHOTOS

if __name__ == "__main__" and runfor == 'PHOTOS':
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
            overlap += 3
        elif key == ord('s'):
            overlap = max(0, overlap - 3)
        elif key == ord('q'):
            f = max(50, f - 20)
        elif key == ord('w'):
            f += 20
        elif key == ord('k'):
            cv2.imwrite(f"panorama_f{f}_overlap{overlap}.png",frame)
            

        if overlap != last_overlap:
            #print(f"Overlap changed to: {overlap}px")
            last_overlap = overlap
        if f != last_f:
            #print(f"Focal length changed to: {f}")
            last_f = f
    cv2.destroyAllWindows()

if __name__ == "__main__" and runfor == 'VIDEOS':
    import sys
    import glob
    import os
    import cv2
    import numpy as np

    # === CONFIG ===
    VIDEO_DIR = r'D:\panorama_video\fixed'
    SCALE = 1           # same spirit as your image resize
    screen_width = 1920   # for display scaling

    # Collect videos (add more extensions if needed)
    exts = ("*.mp4", "*.avi", "*.mkv", "*.mov", "*.m4v")
    video_paths = []
    for ext in exts:
        video_paths.extend(glob.glob(os.path.join(VIDEO_DIR, ext)))
    video_paths = sorted(video_paths)

    if len(video_paths) < 2:
        print("Error: Need at least two videos in ./videos")
        sys.exit(1)

    # Open captures and gather metadata
    caps = []
    meta = []  # (frame_count, fps, width, height)
    for p in video_paths:
        cap = cv2.VideoCapture(p)
        if not cap.isOpened():
            print(f"Error: Failed to open {p}")
            sys.exit(1)

        # Some containers don’t report these properly; fallback handled below
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Basic sanity checks
        if frame_count <= 0:
            # We’ll treat it as an endless stream; we’ll loop by seeking when needed.
            # To make modulo work, we need a length. Probe by reading once.
            ok, fr = cap.read()
            if not ok or fr is None:
                print(f"Error: Cannot read first frame of {p}")
                sys.exit(1)
            # Put the cursor back to start
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # Fake a large frame_count to allow modulo; we’ll still guard with seeks.
            frame_count = 10**9  # “infinite” stream fallback

        caps.append(cap)
        meta.append((frame_count, fps, width, height))

    # Use the minimum frame count across videos for a clean loop (if real counts exist)
    # If any is “infinite”, this still works fine with modulo.
    real_counts = [m[0] for m in meta]
    has_true_counts = all(c < 10**8 for c in real_counts)
    loop_len = min(real_counts) if has_true_counts else None

    # Initial parameters (yours)
    overlap = 125
    f = 800
    last_overlap = overlap
    last_f = f

    print(f"Loaded {len(video_paths)} videos:")
    for i, p in enumerate(video_paths):
        fc, fps, w, h = meta[i]
        fc_str = fc if fc < 10**8 else "unknown/stream"
        print(f"  [{i}] {os.path.basename(p)}  {w}x{h}  {fps:.2f} fps  frames: {fc_str}")
    print(f"Initial overlap: {overlap} px")
    print(f"Initial focal length (radius): {f}")

    # To keep streams aligned, drive them with a single global frame index.
    frame_idx = 0
    paused = False

    def read_frame_at(cap, idx, frame_count):
        """
        Random access to frame idx (modulo frame_count) with robust fallback.
        """
        # Handle “infinite”/unknown case
        if frame_count >= 10**8:
            # Sequential read; if it fails, rewind to start and read again
            ok, fr = cap.read()
            if not ok or fr is None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, fr = cap.read()
            return fr

        # Known length: use modulo and seek for perfect looping
        pos = idx % frame_count
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ok, fr = cap.read()
        if not ok or fr is None:
            # Rare backends need a second poke after set()
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ok, fr = cap.read()
            if not ok or fr is None:
                # As a last resort, restart
                cap.release()
                return None
        return fr

    while True:
        # Build the current frame list from each video
        frames = []
        valid = True
        for i, cap in enumerate(caps):
            fc, fps, w, h = meta[i]
            fr = read_frame_at(cap, frame_idx, fc)
            if fr is None:
                print(f"Stream error on {video_paths[i]}")
                valid = False
                break
            # Resize to common scale (like your image pipeline)
            if SCALE != 1.0:
                fr = cv2.resize(fr, (0, 0), fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
            frames.append(fr)

        if not valid:
            break

        # Create stitched panorama (your function)
        frame = create_global_frame(frames, overlap, f)
        display = frame.copy()

        # HUD
        cv2.putText(display, f"Overlap: {overlap}px | Focal Length: {f} | Frame: {frame_idx}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Fit to screen width
        display_h, display_w = display.shape[:2]
        scale_factor = screen_width / max(1, display_w)
        new_height = int(display_h * scale_factor)
        cv2.imshow("Cylindrical Panorama Viewer", cv2.resize(display, (screen_width, new_height)))

        # Timing: use a fixed small delay; videos remain sync’d by frame_idx
        key = cv2.waitKey(1 if not paused else 30) & 0xFF

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
        elif key == ord('k'):
            cv2.imwrite(f"panorama_f{f}_overlap{overlap}_frame{frame_idx}.png", frame)
        elif key == ord(' '):  # space to pause/play
            paused = not paused
        elif key == ord('r'):  # reset to start
            frame_idx = 0

        if overlap != last_overlap:
            last_overlap = overlap
        if f != last_f:
            last_f = f

        if not paused:
            frame_idx += 1
            # If all have real counts, you can optionally hard-loop at the shortest
            if loop_len is not None and frame_idx >= loop_len:
                frame_idx = 0

    # Cleanup
    for cap in caps:
        try:
            cap.release()
        except:
            pass
    cv2.destroyAllWindows()
