import os
from dotenv import load_dotenv # Kasayı açan kütüphane
import google.generativeai as genai
import chromadb
from chromadb.config import Settings

# 1. GİZLİ KASAYI AÇ (.env dosyasını yükle)
load_dotenv()

print("--- RAG ASİSTANI: Şirket Verileriyle Konuş ---")

# Anahtarı kasadan çek
API_KEY = os.getenv("GOOGLE_API_KEY")

# Eğer kasa boşsa uyarı ver
if not API_KEY:
    print("❌ HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")
    exit()

genai.configure(api_key=API_KEY)

# Modeller
EMBEDDING_MODEL = "models/text-embedding-004"
CHAT_MODEL = "models/gemini-2.5-flash" 

# 2. HAFIZAYI HAZIRLA (ChromaDB)
client = chromadb.Client(Settings(is_persistent=False))
try:
    client.delete_collection("rag_hafiza")
except:
    pass
collection = client.create_collection(name="rag_hafiza")

# Şirket Kuralları
veriler = [
    "Şirketimizde mesai saatleri sabah 09:00 ile 18:00 arasındadır.",
    "Tüm çalışanlara aylık 3000 TL Sodexo yemek kartı verilir.",
    "Evden çalışma (Remote) hakkı haftada 2 gündür (Pazartesi ve Cuma).",
    "Acil durumlarda İK departmanına 555-1234 numarasından ulaşabilirsiniz."
]
ids = ["mesai", "yemek", "remote", "iletisim"]

print("1. Veriler yükleniyor ve vektöre çevriliyor...")
vektorler = []
for veri in veriler:
    v = genai.embed_content(model=EMBEDDING_MODEL, content=veri, task_type="retrieval_document")['embedding']
    vektorler.append(v)

collection.add(documents=veriler, embeddings=vektorler, ids=ids)
print("✅ Hafıza hazır!")

# --- SOHBET DÖNGÜSÜ ---
while True:
    print("\n" + "-"*40)
    soru = input("SORU SOR (Çıkmak için 'q' bas): ")
    
    if soru.lower() == 'q':
        break
    
    print("🔍 Hafızada aranıyor...")
    
    try:
        soru_vektoru = genai.embed_content(model=EMBEDDING_MODEL, content=soru, task_type="retrieval_query")['embedding']
        
        arama_sonucu = collection.query(query_embeddings=[soru_vektoru], n_results=1)
        
        if arama_sonucu['documents'][0]:
            bulunan_bilgi = arama_sonucu['documents'][0][0]
            print(f"💡 Bulunan İpucu: {bulunan_bilgi}")
            
            print("🤖 Cevap hazırlanıyor...")
            
            prompt = f"""
            Sen yardımcı bir asistansın. Aşağıdaki şirket bilgisini kullanarak kullanıcının sorusunu cevapla.
            
            ŞİRKET BİLGİSİ: {bulunan_bilgi}
            
            KULLANICI SORUSU: {soru}
            """
            
            model = genai.GenerativeModel(CHAT_MODEL)
            cevap = model.generate_content(prompt)
            
            print(f"\n📢 ASİSTAN: {cevap.text}")
            
        else:
            print("❌ Üzgünüm, bununla ilgili bir bilgim yok.")
            
    except Exception as e:
        print(f"❌ HATA OLUŞTU: {e}")