import cv2
import numpy as np

def detect_camera_movement(video_path, min_match_count=10, inlier_ratio_threshold=0.7):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return [], [], None

    orb = cv2.ORB_create(nfeatures=1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    prev_keypoints = None
    prev_descriptors = None
    prev_frame_for_display = None

    frame_number = 0
    detected_movements = []
    all_frame_scores = [] # GRAFİK İÇİN YENİ LİSTE

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = orb.detectAndCompute(gray, None)

        score_data = {"frame": frame_number, "score": 0.0, "detected": False}

        if prev_descriptors is not None and descriptors is not None:
            matches = bf.match(prev_descriptors, descriptors)
            
            if len(matches) > min_match_count:
                src_pts = np.float32([prev_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                if M is not None:
                    inlier_count = np.sum(mask)
                    inlier_ratio = inlier_count / len(matches)
                    score_data["score"] = inlier_ratio # Skoru güncelle

                    if inlier_ratio > inlier_ratio_threshold:
                        score_data["detected"] = True # Hareketi işaretle
                        movement_event = {
                            "frame_number": frame_number,
                            "message": f"Kamera Hareketi! (Kare: {frame_number}, Güven: {inlier_ratio:.2%})",
                            "prev_frame": prev_frame_for_display,
                            "current_frame": frame.copy()
                        }
                        detected_movements.append(movement_event)
        
        all_frame_scores.append(score_data) # Her karenin skorunu listeye ekle
        
        prev_keypoints = keypoints
        prev_descriptors = descriptors
        prev_frame_for_display = frame.copy()
    
    last_frame = prev_frame_for_display
    cap.release()
        
    return detected_movements, all_frame_scores, last_frame