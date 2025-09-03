import cv2
import numpy as np
import os
import sys
from collections import deque
from time import sleep

def interpolate_frames(prev_bgr, next_bgr):
    """Bidirectional Farnebäck flow: half-warp each way, then 50/50 blend."""
    if prev_bgr.shape != next_bgr.shape:
        raise ValueError("prev and next frames must have same shape")

    prev_gray = cv2.cvtColor(prev_bgr, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.cvtColor(next_bgr, cv2.COLOR_BGR2GRAY)

    flow_fwd = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None,
                                            pyr_scale=0.5, levels=3, winsize=21,
                                            iterations=5, poly_n=7, poly_sigma=1.5, flags=0)
    flow_bwd = cv2.calcOpticalFlowFarneback(next_gray, prev_gray, None,
                                            pyr_scale=0.5, levels=3, winsize=21,
                                            iterations=5, poly_n=7, poly_sigma=1.5, flags=0)

    h, w = prev_gray.shape
    grid_x, grid_y = np.meshgrid(np.arange(w, dtype=np.float32),
                                 np.arange(h, dtype=np.float32))

    map_x_prev = grid_x + 0.5 * flow_fwd[..., 0]
    map_y_prev = grid_y + 0.5 * flow_fwd[..., 1]
    map_x_next = grid_x + 0.5 * flow_bwd[..., 0]
    map_y_next = grid_y + 0.5 * flow_bwd[..., 1]

    prev_half = cv2.remap(prev_bgr, map_x_prev, map_y_prev, interpolation=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)
    next_half = cv2.remap(next_bgr, map_x_next, map_y_next, interpolation=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)

    mid = cv2.addWeighted(prev_half, 0.5, next_half, 0.5, 0.0)
    return mid

def draw_overlay(img, text, org=(12, 28)):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)

def main(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: cannot open '{input_path}'")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    if fps <= 1e-3: fps = 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    base, ext = os.path.splitext(output_path)
    if ext == "": output_path = base + ".mp4"

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        print(f"Error: cannot open writer for '{output_path}'")
        sys.exit(1)

    # Read first current frame
    ret, curr = cap.read()
    if not ret:
        print("Error: empty input video.")
        cap.release(); out.release(); sys.exit(1)

    # Lookahead buffer: ahead[0] = next, ahead[9] = +10
    ahead = deque()
    # Pre-fill up to 10 frames ahead
    while len(ahead) < 10:
        ret, f = cap.read()
        if not ret: break
        ahead.append(f)

    prev_written = None
    black = np.zeros_like(curr)
    cv2.namedWindow("Preview [Prev | Curr | Next | +10]", cv2.WINDOW_NORMAL)

    frame_idx = 0
    while curr is not None:
        nextf = ahead[0] if len(ahead) >= 1 else None
        plus10 = ahead[9] if len(ahead) >= 10 else None

        left = prev_written if prev_written is not None else black
        center = curr
        right1 = nextf if nextf is not None else black
        right2 = plus10 if plus10 is not None else black

        preview = cv2.hconcat([left, center, right1, right2])

        draw_overlay(preview, f"Frame {frame_idx}")
        draw_overlay(preview, "[I]=interpolate  [D]=duplicate prev  [Any]=keep  [Q]=quit", (12, height - 16))
        draw_overlay(preview, "Panels: Prev | Curr | Next | +10", (12, height - 48))

        cv2.imshow("Preview [Prev | Curr | Next | +10]", preview)
        #sleep(0.05)
        key = cv2.waitKey(0) & 0xFF

        if key in (ord('q'), ord('Q')):
            print("Quitting early.")
            break

        # Decide what to write for current frame
        if key in (ord('i'), ord('I')) and (prev_written is not None) and (nextf is not None):
            try:
                decided = interpolate_frames(prev_written, nextf)
            except Exception as e:
                print(f"Interpolation failed on frame {frame_idx}: {e}")
                decided = curr
        elif key in (ord('d'), ord('D')) and (prev_written is not None):
            # Duplicate the previous written frame (no interpolation)
            decided = prev_written.copy()
        else:
            # Keep original current frame
            decided = curr

        out.write(decided)

        # Advance: prev becomes what we actually wrote
        prev_written = decided

        # Shift window forward by one frame:
        # - new current becomes ahead[0] (was 'next')
        # - pop from ahead and push one new frame from cap
        if len(ahead) >= 1:
            curr = ahead.popleft()
        else:
            curr = None

        if curr is not None:
            ret, f = cap.read()
            if ret:
                ahead.append(f)

        frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n  python triptych_interpolator.py input_video.mp4 [output_video.mp4]")
        sys.exit(0)
    inp = sys.argv[1]
    outp = sys.argv[2] if len(sys.argv) > 2 else "output_interpolated.mp4"
    main(inp, outp)
