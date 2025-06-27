import cv2
import numpy as np

def detect_camera_movement(video_path, min_match_count=10, inlier_ratio_threshold=0.7):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return [], None # Artık bir tuple döndürüyoruz: (hareketler, son_kare)

    orb = cv2.ORB_create(nfeatures=1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    prev_keypoints = None
    prev_descriptors = None
    prev_frame_for_display = None # Görsel kanıt için önceki kareyi saklayacağız

    frame_number = 0
    detected_movements = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints, descriptors = orb.detectAndCompute(gray, None)

        if prev_descriptors is None:
            prev_keypoints = keypoints
            prev_descriptors = descriptors
            prev_frame_for_display = frame.copy() # İlk kareyi kopyala
            continue
            
        if prev_descriptors is not None and descriptors is not None:
            matches = bf.match(prev_descriptors, descriptors)
            matches = sorted(matches, key=lambda x: x.distance)

            if len(matches) > min_match_count:
                src_pts = np.float32([prev_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                if M is not None:
                    inlier_count = np.sum(mask)
                    inlier_ratio = inlier_count / len(matches)

                    if inlier_ratio > inlier_ratio_threshold:
                        # --- DEĞİŞİKLİK BURADA ---
                        # Sadece mesaj değil, bir sözlük ekliyoruz
                        movement_event = {
                            "frame_number": frame_number,
                            "message": f"Kamera Hareketi! (Kare: {frame_number}, Inlier Oranı: {inlier_ratio:.2%})",
                            "prev_frame": prev_frame_for_display,
                            "current_frame": frame.copy()
                        }
                        detected_movements.append(movement_event)

        prev_keypoints = keypoints
        prev_descriptors = descriptors
        prev_frame_for_display = frame.copy() # Her döngüde bir sonraki "önceki" kareyi güncelle
    
    last_frame = prev_frame_for_display # Döngü bittiğindeki son kareyi al
    cap.release()
        
    return detected_movements, last_frame