import streamlit as st
import os
import tempfile

# Diğer dosyamızdaki fonksiyonu içeri aktarıyoruz.
from detect_movement import detect_camera_movement

st.title("Kamera Hareketi Tespit Uygulaması")
st.write("Bu uygulama, bir videodaki ani kamera hareketlerini (kaydırma, eğilme vb.) tespit eder.")

# Kullanıcının bir video dosyası yüklemesini sağlayan bileşen.
uploaded_file = st.file_uploader("Analiz için bir video yükleyin", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Analizi başlatmak için bir düğme ekliyoruz.
    if st.button("Hareketi Tespit Et"):

        # Geçici bir dosya oluşturup yüklenen videonun içeriğini oraya yazıyoruz.
        # Bu, OpenCV'nin dosyayı diskten okuyabilmesi için gereklidir.
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
            tfile.write(uploaded_file.read())
            temp_video_path = tfile.name

        # "İşleniyor..." mesajı gösteriyoruz.
        with st.spinner('Video analiz ediliyor, lütfen bekleyin... Bu işlem biraz zaman alabilir.'):
            # Ana fonksiyonumuzu, geçici videonun yolu ile çağırıyoruz.
            movements = detect_camera_movement(temp_video_path)

        st.success('Analiz tamamlandı!')

        # Sonuçları gösteriyoruz.
        if movements:
            st.subheader("Tespit Edilen Hareketler:")
            for movement in movements:
                st.warning(movement) # Sonuçları sarı bir kutuda göster
        else:
            st.info("Videoda önemli bir kamera hareketi tespit edilmedi.")

        # Geçici dosyayı temizliyoruz.
        os.remove(temp_video_path)