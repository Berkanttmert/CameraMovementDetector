import streamlit as st
import os
import tempfile

from detect_movement import detect_camera_movement

# Sayfa yapılandırması
st.set_page_config(page_title="Kamera Hareketi Tespiti", layout="wide")

# --- Başlık Alanı ---
st.title("📷 Akıllı Kamera Hareketi Tespiti")
st.markdown("""
Bu uygulama, bir videodaki kamera hareketlerini (kaydırma, eğilme vb.) sahne içindeki nesne hareketlerinden ayırt etmeye çalışır. 
Bunu, kareler arasındaki 'özellik noktalarını' (feature points) takip ederek ve bu noktaların ne kadarının tutarlı bir şekilde hareket ettiğini (homografi) analiz ederek yapar.
""")
st.divider()

# --- İki Sütunlu Ana Alan ---
col1, col2 = st.columns([1, 2])

# --- SÜTUN 1: Ayarlar ve Kontroller ---
with col1:
    st.header("⚙️ Kontrol Paneli")
    
    uploaded_file = st.file_uploader("1. Bir video yükleyin", type=["mp4", "mov", "avi"])
    
    st.subheader("Hassasiyet Ayarları")
    
    inlier_ratio_threshold = st.slider(
        "Hassasiyet Eşiği (Inlier Ratio)", 
        min_value=0.1, max_value=1.0, value=0.7, step=0.05,
        help="Bir hareketin 'kamera hareketi' sayılması için özellik noktalarının ne kadarının (% olarak) aynı kurala uyması gerektiğini belirler. Düşük değerler daha hassas, yüksek değerler daha seçicidir."
    )

    min_match_count = st.slider(
        "Minimum Eşleşme Sayısı", 
        min_value=5, max_value=50, value=10, step=1,
        help="Analiz yapmak için gereken minimum özellik noktası eşleşme sayısı. Gürültülü veya düşük kaliteli videolar için bu değeri artırmak gerekebilir."
    )
    
    analyze_button = st.button("2. Analizi Başlat", type="primary", use_container_width=True)

# --- SÜTUN 2: Sonuçlar ---
with col2:
    st.header("📊 Analiz Sonuçları")

    # Düğmeye basıldığında ve dosya yüklendiğinde analiz başlar
    if analyze_button:
        if uploaded_file is not None:
            # Analiz süresince bir "bekle" animasyonu göster
            with st.spinner('Video analiz ediliyor... Lütfen bekleyin.'):
                # Geçici dosya oluştur ve videoyu yaz
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                    tfile.write(uploaded_file.read())
                    temp_video_path = tfile.name
                
                # Çekirdek analiz fonksiyonunu çağır
                movements = detect_camera_movement(
                    video_path=temp_video_path,
                    min_match_count=min_match_count,
                    inlier_ratio_threshold=inlier_ratio_threshold
                )
                
                # Geçici dosyayı sistemden sil
                os.remove(temp_video_path)

            st.success('Analiz tamamlandı!')

            # Gelen sonuca göre mesaj göster
            # Fonksiyonun döndürdüğü 'bulunamadı' veya 'hata' mesajlarını da yakalıyoruz
            if movements and "Hata" not in movements[0] and "bulunamadı" not in movements[0]:
                st.subheader("✅ Tespit Edilen Kamera Hareketleri:")
                # Sonuçları kaydırılabilir bir kutu içinde göster
                result_text = "\n".join(movements)
                st.text_area("Detaylar", result_text, height=300)
            else:
                # Eğer hareket bulunamadıysa, fonksiyondan gelen mesajı göster
                st.warning(f"ℹ️ {movements[0]}")
        else:
            # Eğer düğmeye basıldı ama dosya yoksa hata göster
            st.error("Lütfen önce bir video dosyası yükleyin!")
    else:
        # Sayfa ilk açıldığında veya düğmeye basılmadığında görünen varsayılan mesaj
        st.info("Analizi başlatmak için lütfen bir video yükleyin ve soldaki butona tıklayın.")