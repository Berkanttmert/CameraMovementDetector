import streamlit as st
import os
import tempfile
import cv2
import matplotlib.pyplot as plt

from detect_movement import detect_camera_movement

st.set_page_config(page_title="Kamera Hareketi Tespiti", layout="wide", initial_sidebar_state="expanded")

st.title("📈 Kamera Hareketi Analiz Raporu")
st.markdown("Bu uygulama, homografi analizi kullanarak kamera hareketlerini tespit eder ve zaman çizelgesi üzerinde görselleştirir.")
st.divider()

with st.sidebar:
    # ... (Kenar çubuğu kodu aynı, değişiklik yok) ...
    st.header("⚙️ Kontrol Paneli")
    use_sample_video = st.checkbox("Örnek Videoyu Kullan", value=True)
    sample_video_path = "videos/ornekvideo.mp4"
    uploaded_file = st.file_uploader("Veya Kendi Videonuzu Yükleyin", type=["mp4", "mov", "avi"], disabled=use_sample_video)
    st.subheader("Hassasiyet Ayarları")
    inlier_ratio_threshold = st.slider("Hassasiyet Eşiği", 0.1, 1.0, 0.7, 0.05)
    min_match_count = st.slider("Minimum Eşleşme Sayısı", 5, 50, 10, 1)
    analyze_button = st.button("Analizi Başlat", type="primary", use_container_width=True)


st.header("📊 Analiz Sonuçları")

video_path_to_analyze = None
if use_sample_video:
    video_path_to_analyze = sample_video_path
elif uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_file.read())
        video_path_to_analyze = tfile.name
else:
    st.info("Lütfen bir video yükleyin veya örnek videoyu kullanma seçeneğini işaretleyerek analizi başlatın.")

if analyze_button and video_path_to_analyze:
    with st.spinner('Video analiz ediliyor... Lütfen bekleyin.'):
        movements, scores, last_frame = detect_camera_movement(
            video_path=video_path_to_analyze,
            min_match_count=min_match_count,
            inlier_ratio_threshold=inlier_ratio_threshold
        )

    st.success('Analiz tamamlandı!')

    # --- GRAFİK ÇİZİMİ ---
    if scores:
        st.subheader("Hareket Zaman Çizelgesi Grafiği")
        
        frame_numbers = [s['frame'] for s in scores]
        confidence_scores = [s['score'] for s in scores]
        
        detected_frames = [s['frame'] for s in scores if s['detected']]
        detected_scores = [s['score'] for s in scores if s['detected']]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(frame_numbers, confidence_scores, label='Güven Skoru (Inlier Ratio)', color='dodgerblue', linewidth=2)
        ax.plot(detected_frames, detected_scores, 'D', label='Hareket Tespit Edildi', color='orangered', markersize=8)
        
        ax.axhline(y=inlier_ratio_threshold, color='gray', linestyle='--', label=f'Hassasiyet Eşiği ({inlier_ratio_threshold})')
        
        ax.set_title("Kare Bazında Kamera Hareketi Güven Skoru", fontsize=16)
        ax.set_xlabel("Kare Numarası", fontsize=12)
        ax.set_ylabel("Güven Skoru", fontsize=12)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        st.pyplot(fig)

    # --- HAREKET DETAYLARI ---
    if movements:
        st.subheader(f"✅ {len(movements)} adet önemli kamera hareketi detayı:")
        for event in movements:
            with st.expander(event["message"]):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(cv2.cvtColor(event["prev_frame"], cv2.COLOR_BGR2RGB), caption=f"Kare {event['frame_number']-1}")
                with col2:
                    st.image(cv2.cvtColor(event["current_frame"], cv2.COLOR_BGR2RGB), caption=f"Kare {event['frame_number']}")
    else:
        st.warning("ℹ️ Videoda, belirtilen ayarlarla önemli bir kamera hareketi tespit edilmedi.")

    if uploaded_file is not None:
        os.remove(video_path_to_analyze)