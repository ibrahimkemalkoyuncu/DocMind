# 📄 DocMind: PDF ile Konuşan Yapay Zeka Asistanı

Bu proje, Google Gemini Pro ve ChromaDB kullanarak geliştirilmiş, RAG (Retrieval-Augmented Generation) mimarisiyle çalışan bir yapay zeka asistanıdır. Kullanıcıların yüklediği PDF dosyalarını analiz eder ve dosya içeriğiyle ilgili soruları anında cevaplar.

🔗 **Canlı Demo:** [Buraya Streamlit Uygulama Linkini Yapıştır]

## 🚀 Özellikler

* **PDF Analizi:** Yüklenen belgeleri saniyeler içinde okur ve vektör verisine dönüştürür.
* **Akıllı Hafıza:** ChromaDB kullanarak anlamsal arama (Semantic Search) yapar.
* **Google Gemini Entegrasyonu:** En güncel Gemini 2.5 Flash modeli ile doğal dilde cevaplar üretir.
* **Kaynak Gösterimi:** Yapay zekanın cevabı belgenin hangi kısmından aldığını gösterir.

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.10+
* **LLM & Embedding:** Google Gemini API (gemini-1.5-flash / text-embedding-004)
* **Vektör Veritabanı:** ChromaDB
* **Arayüz:** Streamlit
* **PDF İşleme:** PyPDF

## 💻 Kurulum (Local)

Projeyi kendi bilgisayarınızda çalıştırmak için:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/pdf-chat-ai.git](https://github.com/KULLANICI_ADINIZ/pdf-chat-ai.git)
    cd pdf-chat-ai
    ```

2.  **Sanal ortamı kurun:**
    ```bash
    python -m venv .venv
    # Windows için:
    .venv\Scripts\activate
    # Mac/Linux için:
    source .venv/bin/activate
    ```

3.  **Gereksinimleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Anahtarını ayarlayın:**
    `.env` adında bir dosya oluşturun ve içine şunları yazın:
    ```
    GOOGLE_API_KEY="AIzaSy....."
    ```

5.  **Uygulamayı başlatın:**
    ```bash
    streamlit run app.py
    ```

## 🤝 Katkıda Bulunma

Pull request'ler kabul edilir. Büyük değişiklikler için önce tartışma başlatmanızı rica ederim.

## 📜 Lisans

[MIT](https://choosealicense.com/licenses/mit/)