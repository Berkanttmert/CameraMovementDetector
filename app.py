import streamlit as st
import os
import tempfile
import cv2

from detect_movement import detect_camera_movement

# Sayfa yapılandırması
st.set_page_config(page_title="Kamera Hareketi Tespiti", layout="wide", initial_sidebar_state="expanded")

# --- Başlık Alanı ---
st.title("📷 Akıllı Kamera Hareketi Tespiti v2.0")
st.markdown("Bu uygulama, homografi analizi kullanarak kamera hareketlerini nesne hareketlerinden ayırt eder.")
st.divider()

# --- KENAR ÇUBUĞU (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    
    # Örnek Video Kullanma Seçeneği
    use_sample_video = st.checkbox("Örnek Videoyu Kullan", value=True)
    sample_video_path = "videos/videoo.mp4" # GitHub reponuzdaki video adıyla eşleşmeli
    
    uploaded_file = st.file_uploader("Veya Kendi Videonuzu Yükleyin", type=["mp4", "mov", "avi"], disabled=use_sample_video)
    
    st.subheader("Hassasiyet Ayarları")
    inlier_ratio_threshold = st.slider("Hassasiyet Eşiği", 0.1, 1.0, 0.7, 0.05, help="...")
    min_match_count = st.slider("Minimum Eşleşme Sayısı", 5, 50, 10, 1, help="...")
    
    analyze_button = st.button("Analizi Başlat", type="primary", use_container_width=True)

# --- ANA İÇERİK ---
st.header("📊 Analiz Sonuçları")

video_path_to_analyze = None
if use_sample_video:
    video_path_to_analyze = sample_video_path
elif uploaded_file is not None:
    # Yüklenen dosyayı geçici olarak kaydet
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(uploaded_file.read())
        video_path_to_analyze = tfile.name
else:
    st.info("Lütfen bir video yükleyin veya örnek videoyu kullanma seçeneğini işaretleyerek analizi başlatın.")


if analyze_button and video_path_to_analyze:
    with st.spinner('Video analiz ediliyor... Bu işlem biraz zaman alabilir.'):
        movements, last_frame = detect_camera_movement(
            video_path=video_path_to_analyze,
            min_match_count=min_match_count,
            inlier_ratio_threshold=inlier_ratio_threshold
        )

    st.success('Analiz tamamlandı!')

    if movements:
        st.subheader(f"✅ {len(movements)} adet önemli kamera hareketi tespit edildi:")
        for event in movements:
            with st.expander(event["message"]):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(cv2.cvtColor(event["prev_frame"], cv2.COLOR_BGR2RGB), caption=f"Kare {event['frame_number']-1} (Hareket Öncesi)")
                with col2:
                    st.image(cv2.cvtColor(event["current_frame"], cv2.COLOR_BGR2RGB), caption=f"Kare {event['frame_number']} (Hareket Anı)")
    else:
        st.warning("ℹ️ Videoda, belirtilen ayarlarla önemli bir kamera hareketi tespit edilmedi.")
        if last_frame is not None:
            st.image(cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB), caption="Videonun Son Karesi (Analiz Başarılı)")
            
    # Eğer geçici dosya oluşturulduysa, onu temizle
    if uploaded_file is not None:
        os.remove(video_path_to_analyze)