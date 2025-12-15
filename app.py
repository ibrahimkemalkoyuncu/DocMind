import streamlit as st
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
from ddgs import DDGS

# --- 1. AYARLAR ---
st.set_page_config(page_title="DocMind v2.0: Agent", layout="wide")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ API Key eksik! .env dosyasını kontrol et.")
    st.stop()

genai.configure(api_key=API_KEY)

# Senin hesabında çalışan VIP model
EMBEDDING_MODEL = "models/text-embedding-004"
CHAT_MODEL = "models/gemini-2.5-flash"

# --- 2. ARAÇLAR (TOOLS) ---

def internette_ara(sorgu):
    """PDF'te bilgi yoksa Google/DuckDuckGo'da arama yapar."""
    print(f"⚙️ [ARAÇ]: İnternette aranıyor: {sorgu}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(sorgu, region='tr-tr', max_results=2))
            if results:
                return f"İNTERNET SONUÇLARI: {str(results)}"
            return "İnternette sonuç bulunamadı."
    except Exception as e:
        return f"Arama hatası: {e}"

def hesap_makinesi(islem):
    """Matematiksel hesaplama yapar. Örn: '450 * 1.20'"""
    print(f"⚙️ [ARAÇ]: Hesap yapılıyor: {islem}")
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(islem).issubset(allowed):
            return "Hatalı karakter."
        return str(eval(islem))
    except:
        return "Hesaplama hatası."

# Araç listesi
araclar = [internette_ara, hesap_makinesi]

# --- 3. FONKSİYONLAR ---

def get_chroma_client():
    return chromadb.Client(Settings(is_persistent=False))

def pdf_to_text(uploaded_file):
    text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=2000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += end - overlap
    return chunks

# --- 4. ARAYÜZ (UI) ---

st.title("🧠 DocMind v2.0: Otonom Agent")
st.markdown("Bu yapay zeka sadece okumaz; **İnternette arar** ve **Hesap yapar**.")

# Sidebar
with st.sidebar:
    st.header("📁 Doküman Yükle")
    uploaded_file = st.file_uploader("PDF Seç", type="pdf")
    
    if uploaded_file and st.button("Analiz Et"):
        with st.spinner("PDF işleniyor..."):
            try:
                raw_text = pdf_to_text(uploaded_file)
                chunks = chunk_text(raw_text)
                
                client = get_chroma_client()
                try: client.delete_collection("agent_hafiza")
                except: pass
                collection = client.create_collection(name="agent_hafiza")
                
                ids = [str(i) for i in range(len(chunks))]
                embeddings = []
                
                prog = st.progress(0)
                for i, chunk in enumerate(chunks):
                    emb = genai.embed_content(model=EMBEDDING_MODEL, content=chunk, task_type="retrieval_document")['embedding']
                    embeddings.append(emb)
                    prog.progress((i+1)/len(chunks))
                    time.sleep(0.5) # Hız limitine takılmamak için fren
                
                collection.add(documents=chunks, embeddings=embeddings, ids=ids)
                st.session_state['collection'] = collection
                st.session_state['db_ready'] = True
                st.success("✅ Hafıza Hazır!")
                
            except Exception as e:
                st.error(f"Hata: {e}")

# Sohbet Alanı
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! PDF yükleyebilir veya genel sorular sorabilirsin."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sorunu yaz..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Düşünüyorum...")
        
        try:
            # A. Önce PDF Hafızasına Bak (RAG)
            context_text = ""
            if 'db_ready' in st.session_state:
                collection = st.session_state['collection']
                q_emb = genai.embed_content(model=EMBEDDING_MODEL, content=prompt, task_type="retrieval_query")['embedding']
                results = collection.query(query_embeddings=[q_emb], n_results=2)
                context_text = "\n".join(results['documents'][0])
            
            # B. Hepsini Modele Gönder (Agent Karar Versin)
            # Model: "Elimde PDF bilgisi var, gerekirse interneti de kullanabilirim."
            
            full_prompt = f"""
            Sen akıllı bir asistansın. Elinde şu araçlar var: [internette_ara, hesap_makinesi].
            
            KULLANICI SORUSU: {prompt}
            
            ELİMİZDEKİ PDF BİLGİSİ (Varsa):
            {context_text}
            
            YÖNERGE:
            1. Önce PDF bilgisini kontrol et. Cevap oradaysa oradan ver.
            2. PDF'te bilgi yoksa veya güncel bilgi gerekiyorsa 'internette_ara' aracını kullan.
            3. Matematik işlemi gerekiyorsa 'hesap_makinesi' aracını kullan.
            4. Cevabı Türkçe ver.
            """
            
            # Modeli araçlarla başlat
            model = genai.GenerativeModel(model_name=CHAT_MODEL, tools=araclar)
            chat = model.start_chat(enable_automatic_function_calling=True)
            
            response = chat.send_message(full_prompt)
            
            # Cevabı Göster
            final_text = response.text
            message_placeholder.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
            
            # Debug: Nereden buldu?
            with st.expander("Arka Plan Bilgisi"):
                st.write(f"PDF Bağlamı: {context_text[:200]}...")
                
        except Exception as e:
            if "429" in str(e):
                message_placeholder.error("🛑 Hız limiti! Lütfen 30 saniye bekleyip tekrar dene.")
            else:
                message_placeholder.error(f"Bir hata oluştu: {e}")