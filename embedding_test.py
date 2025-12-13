import google.generativeai as genai

print("--- Embedding (Vektör) Testi v2 ---")

# 1. Anahtarını Yapıştır
API_KEY = "AIzaSyC7WgK-O9sBMGukrqx59wHXD1b-06AvSos"
genai.configure(api_key=API_KEY)

try:
    print("1. 'text-embedding-004' modeline bağlanılıyor...")
    
    kelime = "Yapay Zeka Mühendisliği"
    
    # 2. Direkt yeni nesil modeli iste
    sonuc = genai.embed_content(
        model="models/text-embedding-004",
        content=kelime,
        task_type="retrieval_document"
    )
    
    # 3. Sonucu Göster
    vektor = sonuc['embedding']
    print(f"\n✅ BAŞARILI!")
    print(f"🔢 Vektör Uzunluğu: {len(vektor)} boyutlu")
    print(f"Örnek Sayılar: {vektor[:5]}...")
    print("\n🎉 Bu sayılar, yapay zekanın kelimeyi nasıl 'anladığının' kanıtıdır.")

except Exception as e:
    print(f"\n❌ HATA: {e}")
    print("\n⚠️ EĞER YİNE 'QUOTA' HATASI ALIRSAN:")
    print("Google senin hesabına Embedding (Gömme) işlemini tamamen kapatmış demektir.")
    print("Merak etme, B PLANI hazır: Kendi bilgisayarımızda çalışan bedava modeli kuracağız.")