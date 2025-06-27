import cv2
import numpy as np

def detect_camera_movement(video_path, min_match_count=10, inlier_ratio_threshold=0.7):
    """
    Özellik eşleştirme ve homografi kullanarak kamera hareketini nesne hareketinden ayırt eder.
    
    Args:
        video_path (str): Analiz edilecek video dosyası.
        min_match_count (int): Homografi hesaplamak için gereken minimum eşleşme sayısı.
        inlier_ratio_threshold (float): Bir hareketin kamera hareketi olarak kabul edilmesi için
                                        gereken minimum inlier oranı (0.0 ile 1.0 arası).
    Returns:
        list: Tespit edilen kamera hareketlerini içeren mesajların listesi.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return ["Hata: Video dosyası açılamadı."]

    orb = cv2.ORB_create(nfeatures=1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    prev_keypoints = None
    prev_descriptors = None

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
            continue
            
        if prev_descriptors is not None and descriptors is not None:
            matches = bf.match(prev_descriptors, descriptors)
            matches = sorted(matches, key=lambda x: x.distance)

            # --- HOMOGRAFİ MANTIĞI BAŞLANGICI ---
            
            # 1. Eğer yeterli sayıda eşleşme varsa homografi hesaplamayı dene.
            if len(matches) > min_match_count:
                # Eşleşen noktaların koordinatlarını al.
                src_pts = np.float32([prev_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

                # Homografi matrisini ve maskeyi (inlier/outlier) bul.
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                # 2. Eğer matris başarıyla bulunduysa...
                if M is not None:
                    # Inlier'ların (kurala uyan noktaların) sayısını ve oranını hesapla.
                    inlier_count = np.sum(mask)
                    inlier_ratio = inlier_count / len(matches)

                    # 3. Eğer inlier oranı belirlediğimiz eşikten yüksekse, bu kamera hareketidir!
                    if inlier_ratio > inlier_ratio_threshold:
                        message = f"Kamera Hareketi Tespit Edildi! (Kare: {frame_number}, Inlier Oranı: {inlier_ratio:.2%})"
                        detected_movements.append(message)

            # --- HOMOGRAFİ MANTIĞI SONU ---

        prev_keypoints = keypoints
        prev_descriptors = descriptors
        
    cap.release()
    
    if not detected_movements:
        return ["Analiz tamamlandı, önemli bir kamera hareketi bulunamadı."]
        
    return detected_movements