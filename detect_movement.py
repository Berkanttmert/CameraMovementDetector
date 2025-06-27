import cv2

def detect_camera_movement(video_path, sensitivity_threshold=10000):
    """
    Verilen bir video yolundaki kamera hareketini tespit eder.

    Args:
        video_path (str): Analiz edilecek video dosyasının yolu.
        sensitivity_threshold (int): Hareketi "önemli" olarak kabul etmek için gereken
                                     minimum fark puanı.

    Returns:
        list: Hareketin tespit edildiği karelerle ilgili bilgi mesajlarının listesi.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return ["Hata: Video dosyası açılamadı."]

    previous_frame = None
    frame_number = 0
    detected_movements = []  # Sonuçları saklamak için boş bir liste

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        diff_score = cv2.countNonZero(thresh)

        if diff_score > sensitivity_threshold:
            message = f"Hareket Tespit Edildi! (Kare: {frame_number}, Puan: {diff_score})"
            detected_movements.append(message) # Mesajı ekrana yazdırmak yerine listeye ekle

        previous_frame = gray

    cap.release()
    return detected_movements