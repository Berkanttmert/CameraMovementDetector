# Kamera Hareketi Tespit Projesi (Camera Movement Detection)

Bu proje, "Core Talent AI Coder Challenge" kapsamında geliştirilmiştir. Amacı, bir video dosyasındaki önemli kamera hareketlerini (kaydırma, eğilme, sarsılma gibi) tespit eden bir web uygulaması oluşturmaktır.

## 🚀 Canlı Uygulama

Uygulamanın canlı ve çalışan versiyonuna aşağıdaki linkten ulaşabilirsiniz:

**[Uygulamayı Görüntüle](https://cameramovementdetector-berkant.streamlit.app/)**

## 🛠️ Kullandığım Yaklaşım ve Mantık

Uygulamanın çekirdek algoritması, **"Frame Differencing" (Kare Farklılaştırma)** yöntemine dayanmaktadır. Bu yöntem aşağıdaki adımları izler:

1.  **Video Okuma:** Video kare kare okunur.
2.  **Gri Tonlama:** Karşılaştırma yaparken renklerden kaynaklanabilecek yanılgıları (örneğin ışık değişimleri) en aza indirmek için her kare siyah-beyaz (gri tonlamalı) formata çevrilir.
3.  **Fark Hesaplama:** Mevcut kare ile bir önceki kare arasındaki piksel bazında mutlak fark alınır. Eğer iki kare arasında hiç değişiklik yoksa, sonuç tamamen siyah bir görüntü olur.
4.  **Eşikleme (Thresholding):** Fark görüntüsündeki küçük, anlamsız gürültüleri (örneğin video sıkıştırmasından kaynaklanan minik değişimler) temizlemek için bir eşik değeri uygulanır. Bu eşiğin üzerindeki farklar beyaz, altındakiler siyah olarak işaretlenir.
5.  **Puanlama:** Eşiklenmiş görüntüdeki beyaz piksel sayısı (yani toplam değişiklik miktarı) hesaplanır. Bu, bir "hareket puanı" oluşturur.
6.  **Karar Verme:** Eğer bu hareket puanı önceden belirlenmiş bir hassasiyet eşiğini geçerse, o karede "önemli bir kamera hareketi" olduğu kabul edilir ve kullanıcıya bildirilir.

## ⚙️ Projeyi Yerel (Lokal) Bilgisayarda Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **Projeyi Klonlayın veya İndirin:**
    ```bash
    git clone https://github.com/SENIN-KULLANICI-ADIN/CameraMovementDetector.git
    cd CameraMovementDetector
    ```

2.  **Sanal Ortam Oluşturun ve Aktive Edin:**
    ```bash
    # Windows için
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Streamlit Uygulamasını Başlatın:**
    ```bash
    streamlit run app.py
    ```

## ⚠️ Zorluklar ve Varsayımlar (Challenges and Assumptions)

*   **Yayınlama Hatası:** Projeyi Streamlit Cloud'a yüklerken, standart `opencv-python` kütüphanesi bir `ImportError` hatasına neden oldu. Bunun sebebi, sunucu ortamlarının "ekransız" (headless) olmasıdır. Sorun, `requirements.txt` dosyasında `opencv-python-headless` versiyonu kullanılarak çözülmüştür.
*   **Sabit Eşik Değeri:** Algoritma, hareket tespiti için sabit bir hassasiyet eşiği kullanmaktadır. Bu eşik değeri, farklı ışık koşullarına veya video kalitelerine sahip videolar için ideal olmayabilir. Daha dinamik bir eşik belirleme yöntemi, projenin doğruluğunu artırabilir.
*   **Nesne Hareketi vs. Kamera Hareketi:** Kullanılan temel "frame differencing" yöntemi, sahne içinde hareket eden büyük bir nesne ile kameranın kendisinin hareket etmesini ayırt edemeyebilir. Proje tanımındaki "Bonus" kısmını gerçekleştirmek için (nesne ve kamera hareketini ayırt etmek), ORB/SIFT gibi özellik eşleştirme (feature matching) ve homografi matrisi hesaplama gibi daha gelişmiş teknikler kullanılmalıdır.
