import cv2
import os
import sys

def process_video(input_path, output_dir=None):
    if not os.path.isfile(input_path):
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: cannot open video: {input_path}")
        sys.exit(1)

    # Read input properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Try to keep the original codec (may fall back depending on container)
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    # Build FOURCC code from int (works cross-platform enough for most cases)
    fourcc_chars = "".join([chr((fourcc_int >> 8*i) & 0xFF) for i in range(4)])
    # If FOURCC looks weird, use a common safe default
    if not fourcc_chars.strip() or any(ord(c) < 32 for c in fourcc_chars):
        fourcc_chars = "mp4v"  # good default for .mp4

    basename = os.path.splitext(os.path.basename(input_path))[0]
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(input_path)) or "."
    os.makedirs(output_dir, exist_ok=True)

    # Filepaths
    left_cropped_path  = os.path.join(output_dir, f"{basename}_left_cropped.mp4")
    right_cropped_path = os.path.join(output_dir, f"{basename}_right_cropped.mp4")
    left_padded_path   = os.path.join(output_dir, f"{basename}_left_padded.mp4")
    right_padded_path  = os.path.join(output_dir, f"{basename}_right_padded.mp4")

    # Sizes
    mid = width // 2
    # Handle odd widths: left gets floor half, right gets the rest
    left_size  = (mid, height)
    right_size = (width - mid, height)
    full_size  = (width, height)

    # Writers
    fourcc = cv2.VideoWriter_fourcc(*fourcc_chars)

    left_cropped_writer  = cv2.VideoWriter(left_cropped_path,  fourcc, fps, left_size)
    right_cropped_writer = cv2.VideoWriter(right_cropped_path, fourcc, fps, right_size)
    left_padded_writer   = cv2.VideoWriter(left_padded_path,   fourcc, fps, full_size)
    right_padded_writer  = cv2.VideoWriter(right_padded_path,  fourcc, fps, full_size)

    if not (left_cropped_writer.isOpened() and right_cropped_writer.isOpened() and
            left_padded_writer.isOpened() and right_padded_writer.isOpened()):
        print("Error: could not open one or more VideoWriters. "
              "Try changing the extension to .avi with 'XVID' or using 'mp4v' codec.")
        cap.release()
        sys.exit(1)

    print(f"Input: {input_path}")
    print(f"Resolution: {width}x{height}, FPS: {fps:.3f}, Frames: {frame_count}, FOURCC: {fourcc_chars}")
    print(f"Writing:\n  {left_cropped_path}\n  {right_cropped_path}\n  {left_padded_path}\n  {right_padded_path}")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Split
        left  = frame[:, :mid]
        right = frame[:, mid:]

        # Cropped outputs (same fps/codec; half widths)
        left_cropped_writer.write(left)
        right_cropped_writer.write(right)

        # Padded outputs (full size, black fill)
        # Left padded: left half content, right half zeros
        left_pad = frame.copy()
        left_pad[:, mid:] = 0
        # Right padded: right half content, left half zeros
        right_pad = frame.copy()
        right_pad[:, :mid] = 0

        left_padded_writer.write(left_pad)
        right_padded_writer.write(right_pad)

        frame_idx += 1
        if frame_idx % 200 == 0:
            print(f"Processed {frame_idx} frames...")

    # Cleanup
    cap.release()
    left_cropped_writer.release()
    right_cropped_writer.release()
    left_padded_writer.release()
    right_padded_writer.release()

    print("Done.")

if __name__ == "__main__":
    # Usage:
    #   python split_vertical_video.py input_video.mp4 [output_dir]
    if len(sys.argv) < 2:
        print("Usage: python split_vertical_video.py <input_video> [output_dir]")
        sys.exit(1)

    input_video = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    process_video(input_video, out_dir)
