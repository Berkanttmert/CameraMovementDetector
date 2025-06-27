import streamlit as st
import os
import tempfile

# Diğer dosyamızdaki güncellenmiş fonksiyonu içeri aktarıyoruz.
from detect_movement import detect_camera_movement

st.set_page_config(page_title="Kamera Hareketi Tespiti", layout="wide")

st.title("📷 Kamera Hareketi Tespit Uygulaması")
st.write("""
Bu uygulama, bir videodaki kamera hareketlerini (kaydırma, eğilme vb.) sahne içindeki nesne hareketlerinden ayırt etmeye çalışır. 
Bunu, kareler arasındaki 'özellik noktalarını' (feature points) takip ederek ve bu noktaların ne kadarının tutarlı bir şekilde hareket ettiğini (homografi) analiz ederek yapar.
""")

st.sidebar.header("⚙️ Ayarlar")
inlier_ratio_threshold = st.sidebar.slider(
    "Hassasiyet Eşiği (Inlier Ratio)", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.7, 
    step=0.05,
    help="Bir hareketin 'kamera hareketi' sayılması için özellik noktalarının ne kadarının (% olarak) aynı kurala uyması gerektiğini belirler. Düşük değerler daha hassas, yüksek değerler daha seçicidir."
)

min_match_count = st.sidebar.slider(
    "Minimum Eşleşme Sayısı", 
    min_value=5, 
    max_value=50, 
    value=10, 
    step=1,
    help="Analiz yapmak için gereken minimum özellik noktası eşleşme sayısı. Gürültülü veya düşük kaliteli videolar için bu değeri artırmak gerekebilir."
)


# Kullanıcının bir video dosyası yüklemesini sağlayan bileşen.
uploaded_file = st.file_uploader("Analiz için bir video yükleyin", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    if st.button("Hareketi Tespit Et", key="detect_button"):

        # Geçici bir dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
            tfile.write(uploaded_file.read())
            temp_video_path = tfile.name

        # Analiz başlıyor...
        with st.spinner('Video analiz ediliyor, özellikler çıkarılıyor ve homografi hesaplanıyor... Lütfen bekleyin.'):
            # Güncellenmiş fonksiyonumuzu yeni parametrelerle çağırıyoruz.
            movements = detect_camera_movement(
                video_path=temp_video_path,
                min_match_count=min_match_count,
                inlier_ratio_threshold=inlier_ratio_threshold
            )

        st.success('Analiz tamamlandı!')

        # Sonuçları gösteriyoruz.
        if movements and "Hata" not in movements[0]:
            st.subheader("✅ Tespit Edilen Kamera Hareketleri:")
            for movement in movements:
                st.info(movement)
        else:
            st.warning("ℹ️ Videoda, belirtilen hassasiyet ayarlarıyla önemli bir kamera hareketi tespit edilmedi.")

        # Geçici dosyayı temizliyoruz.
        os.remove(temp_video_path)