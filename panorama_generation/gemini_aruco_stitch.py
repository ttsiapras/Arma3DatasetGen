import cv2
import numpy as np
import os
import glob

def find_aruco_homography(img1, img2, aruco_dict, aruco_params):
    """
    Finds the homography that maps points from img2 to img1.
    (This function remains the same as before)
    """
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    corners1, ids1, _ = detector.detectMarkers(gray1)
    corners2, ids2, _ = detector.detectMarkers(gray2)

    if ids1 is None or ids2 is None:
        print("Warning: No ArUco markers detected in one or both images.")
        return None

    ids1_flat = ids1.flatten()
    ids2_flat = ids2.flatten()
    common_ids = np.intersect1d(ids1_flat, ids2_flat)
    
    if len(common_ids) < 1:
        print("Warning: No common ArUco markers found.")
        return None

    print(f"Found {len(common_ids)} common markers between the pair.")
    
    points1 = []
    points2 = []
    for marker_id in common_ids:
        idx1 = np.where(ids1_flat == marker_id)[0][0]
        idx2 = np.where(ids2_flat == marker_id)[0][0]
        for corner_idx in range(4):
            points1.append(corners1[idx1][0][corner_idx])
            points2.append(corners2[idx2][0][corner_idx])

    points1 = np.array(points1, dtype=np.float32)
    points2 = np.array(points2, dtype=np.float32)

    H, _ = cv2.findHomography(points2, points1, cv2.RANSAC, 5.0)
    return H

def crop_black_borders(image):
    """
    Crops the black borders from a stitched image.
    (This function remains the same as before)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image
    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    return image[y:y+h, x:x+w]


def main():
    # --- Configuration ---
    IMAGE_DIR = './images'
    ARUCO_TYPE = "DICT_6X6_50"
    OUTPUT_FILENAME = "panorama_global_output.jpg"

    aruco_dictionary_name = getattr(cv2.aruco, ARUCO_TYPE)
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dictionary_name)
    aruco_params = cv2.aruco.DetectorParameters()

    image_paths = glob.glob(os.path.join(IMAGE_DIR, '*.png'))
    if len(image_paths) < 2:
        print("Error: Need at least two images to stitch.")
        return
        
    print(image_paths)
    # Load all images into memory
    images = [cv2.imread(path) for path in image_paths]
    print(f"Loaded {len(images)} images.")

    # --- PASS 1: Find all pairwise homographies ---
    print("\n--- Pass 1: Finding pairwise homographies ---")
    pairwise_homographies = []
    for i in range(len(images) - 1):
        print(f"Calculating homography for pair ({i}, {i+1})...")
        H = find_aruco_homography(images[i], images[i+1], aruco_dict, aruco_params)
        if H is None:
            print(f"Error: Could not find homography for pair ({i}, {i}). Aborting.")
            return
        pairwise_homographies.append(H)

    # --- PASS 2: Calculate global transformations relative to the first image ---
    print("\n--- Pass 2: Calculating global transformations ---")
    # The first image is our anchor, its transformation is the identity matrix
    global_homographies = [np.eye(3)] 
    H_cumulative = np.eye(3)
    for H_pair in pairwise_homographies:
        # Chain the homographies: H_global_i = H_global_(i-1) @ H_pair_i
        H_cumulative = H_cumulative @ H_pair
        global_homographies.append(H_cumulative)

    # --- Determine the dimensions of the final panorama canvas ---
    print("Determining final canvas size...")
    all_corners = []
    for i, img in enumerate(images):
        h, w = img.shape[:2]
        # Define the corners of the current image
        corners = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
        # Reshape for cv2.perspectiveTransform
        corners = corners.reshape(1, -1, 2)
        # Transform corners to the global coordinate system
        transformed_corners = cv2.perspectiveTransform(corners, global_homographies[i])
        all_corners.append(transformed_corners[0])

    # Find the bounding box of all transformed corners
    all_corners = np.concatenate(all_corners, axis=0)
    x_min, y_min = np.min(all_corners, axis=0)
    x_max, y_max = np.max(all_corners, axis=0)
    
    # Calculate the size of the output canvas
    canvas_width = int(np.ceil(x_max - x_min))
    canvas_height = int(np.ceil(y_max - y_min))

    # Create a translation matrix to shift all images to fit on the canvas
    T = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])

    # --- Warp all images to the global canvas ---
    print(f"Creating final canvas of size {canvas_width}x{canvas_height}...")
    panorama = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    for i, img in enumerate(images):
        print(f"Warping and blending image {i+1}/{len(images)}...")
        # Final transformation for this image is Translation @ GlobalHomography
        H_final = T @ global_homographies[i]
        
        # Warp the image onto the final canvas
        warped_img = cv2.warpPerspective(img, H_final, (canvas_width, canvas_height))
        
        # Create a mask and combine
        mask = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
        
        # Use the mask to copy the warped image onto the panorama
        # This will overlay images, with later images (right) appearing on top in overlaps
        panorama = cv2.copyTo(warped_img, mask, panorama)
        
    # --- Finalization ---
    print("Cropping final panorama...")
    final_panorama = crop_black_borders(panorama)

    print(f"\nStitching complete. Saving final panorama to {OUTPUT_FILENAME}")
    cv2.imwrite(OUTPUT_FILENAME, final_panorama)

    cv2.imshow("Final Panorama (Global Alignment)", cv2.resize(final_panorama, (0,0), fx=0.3, fy=0.3))
    print("Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()