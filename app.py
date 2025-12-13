import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader # PDF okumak için yeni kütüphanemiz

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="PDF Asistanı", layout="wide")

# .env dosyasını yükle
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Anahtar kontrolü
if not API_KEY:
    st.error("❌ Lütfen .env dosyasına GOOGLE_API_KEY ekleyin!")
    st.stop()

genai.configure(api_key=API_KEY)

# Modeller
EMBEDDING_MODEL = "models/text-embedding-004"
CHAT_MODEL = "models/gemini-2.5-flash"

# --- FONKSİYONLAR ---

def get_chroma_client():
    # ChromaDB'yi önbelleğe almadan her seferinde taze çağırıyoruz
    return chromadb.Client(Settings(is_persistent=False))

def pdf_to_text(uploaded_file):
    """PDF dosyasından metinleri çıkarır"""
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    """Metni yapay zekanın yiyebileceği küçük parçalara böler"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += end - overlap # Bağlam kopmasın diye biraz geriden al
    return chunks

# --- ARAYÜZ ---

st.title("📄 PDF Dosyasıyla Konuş")
st.markdown("Yanda bir PDF yükleyin ve yapay zekanın onu öğrenmesini izleyin!")

# Sol Menü (Sidebar)
with st.sidebar:
    st.header("📁 Doküman Yükle")
    uploaded_file = st.file_uploader("Bir PDF dosyası seçin", type="pdf")
    
    if uploaded_file:
        if st.button("🧠 Yapay Zekaya Öğret"):
            with st.spinner("PDF okunuyor ve analiz ediliyor..."):
                try:
                    # 1. Metni Oku
                    raw_text = pdf_to_text(uploaded_file)
                    st.info(f"PDF Okundu! Toplam {len(raw_text)} karakter.")
                    
                    # 2. Parçalara Böl
                    text_chunks = chunk_text(raw_text)
                    st.write(f"🧩 Metin {len(text_chunks)} parçaya bölündü.")
                    
                    # 3. Veritabanını Hazırla
                    client = get_chroma_client()
                    try:
                        client.delete_collection("pdf_hafiza")
                    except:
                        pass
                    collection = client.create_collection(name="pdf_hafiza")
                    
                    # 4. Embedding (Vektöre Çevir) ve Kaydet
                    ids = [str(i) for i in range(len(text_chunks))]
                    
                    embeddings = []
                    # İlerleme çubuğu
                    progress_bar = st.progress(0)
                    
                    for i, chunk in enumerate(text_chunks):
                        emb = genai.embed_content(
                            model=EMBEDDING_MODEL,
                            content=chunk,
                            task_type="retrieval_document"
                        )['embedding']
                        embeddings.append(emb)
                        progress_bar.progress((i + 1) / len(text_chunks))
                    
                    collection.add(documents=text_chunks, embeddings=embeddings, ids=ids)
                    
                    st.session_state['db_ready'] = True
                    st.session_state['collection'] = collection
                    st.success("✅ Öğrenme Tamamlandı! Artık soru sorabilirsin.")
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")

# --- SOHBET ALANI ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı soru sorarsa
if prompt := st.chat_input("PDF hakkında ne bilmek istersin?"):
    # Eğer dosya yüklenmediyse uyar
    if 'db_ready' not in st.session_state:
        st.error("⚠️ Önce soldan bir PDF yükleyip 'Öğret' butonuna basmalısın!")
    else:
        # Mesajı göster
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Araştırıyorum...")
            
            try:
                # 1. Vektör Arama
                collection = st.session_state['collection']
                
                soru_vektoru = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=prompt,
                    task_type="retrieval_query"
                )['embedding']
                
                # En alakalı 3 parçayı getir (Daha kapsamlı cevap için)
                arama_sonucu = collection.query(query_embeddings=[soru_vektoru], n_results=3)
                
                # Bulunan parçaları birleştir
                context_text = "\n\n".join(arama_sonucu['documents'][0])
                
                # 2. Gemini'ye Gönder
                full_prompt = f"""
                Sen uzman bir doküman analistisin. Aşağıdaki PDF içeriğini kullanarak soruyu cevapla.
                
                PDF İÇERİĞİNDEN PARÇALAR:
                {context_text}
                
                SORU: {prompt}
                
                Cevabı verirken sadece PDF'teki bilgileri kullan. Bilgi yoksa "Dokümanda bu bilgi geçmiyor" de.
                """
                
                model = genai.GenerativeModel(CHAT_MODEL)
                response = model.generate_content(full_prompt)
                
                # Cevabı yaz
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
                # Kaynakları göster (Opsiyonel)
                with st.expander("Hangi parçalara baktım?"):
                    st.write(context_text)
                    
            except Exception as e:
                message_placeholder.error(f"Hata: {e}")