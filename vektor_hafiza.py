import google.generativeai as genai
import chromadb
from chromadb.config import Settings

print("--- Akıllı Hafıza Sistemi (RAG Başlangıcı) ---")

# 1. Google Ayarları (Çalışan Modelin: text-embedding-004)
API_KEY = "AIzaSyC7WgK-O9sBMGukrqx59wHXD1b-06AvSos"
genai.configure(api_key=API_KEY)

# 2. ChromaDB Deposu Oluştur (Bilgisayarında geçici hafıza)
db_istemcisi = chromadb.Client(Settings(is_persistent=False))
koleksiyon = db_istemcisi.create_collection(name="sirket_bilgileri")

# 3. Örnek Veriler (Şirket Kuralları gibi düşün)
dokumanlar = [
    "Şirketimizde mesai saatleri sabah 9 ile akşam 6 arasındadır.",
    "Yemekhanede her gün vegan menü seçeneği bulunmaktadır.",
    "Yıllık izinlerinizi en az 2 hafta önceden sisteme girmelisiniz."
]
id_ler = ["kural1", "kural2", "kural3"]

print("1. Dokümanlar vektöre (sayıya) çevriliyor...")

# Google'a verileri gönderip sayılarını (vektörlerini) alıyoruz
vektorler = []
for dokuman in dokumanlar:
    sonuc = genai.embed_content(
        model="models/text-embedding-004",
        content=dokuman,
        task_type="retrieval_document"
    )
    vektorler.append(sonuc['embedding'])

print("2. Vektörler veritabanına kaydediliyor...")
# ChromaDB'ye hem yazıyı hem de onun matematiksel karşılığını ekliyoruz
koleksiyon.add(
    documents=dokumanlar,
    embeddings=vektorler,
    ids=id_ler
)

# --- TEST ZAMANI ---
soru = "Öğlen yemeğinde etsiz yemek var mı?"
print(f"\nSoru: '{soru}'")
print("Cevap aranıyor (Anlam eşleştirmesi yapılıyor)...")

# Soruyu da vektöre çevir (Çünkü elma ile elmayı kıyaslamalıyız)
soru_vektoru = genai.embed_content(
    model="models/text-embedding-004",
    content=soru,
    task_type="retrieval_query"
)['embedding']

# Veritabanında bu vektöre en yakın olan bilgiyi bul
sonuc = koleksiyon.query(
    query_embeddings=[soru_vektoru],
    n_results=1 # En alakalı 1 sonucu getir
)

print("\n✅ BULUNAN CEVAP:")
print(sonuc['documents'][0][0])