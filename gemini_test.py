import google.generativeai as genai

print("--- Google Gemini OTO-PİLOT Modu ---")

# 1. Anahtarını Buraya Yapıştır
API_KEY = "AIzaSyC7WgK-O9sBMGukrqx59wHXD1b-06AvSos"
genai.configure(api_key=API_KEY)

try:
    print("1. Google'ın sunucusundaki model listesi çekiliyor...")
    
    # Tüm modelleri iste
    tum_modeller = genai.list_models()
    
    secilen_model_adi = None

    # 2. Listeden "sohbet edebilen" İLK modeli bul
    for m in tum_modeller:
        if 'generateContent' in m.supported_generation_methods:
            secilen_model_adi = m.name
            print(f"✅ BULUNDU! Kullanılacak Model: {secilen_model_adi}")
            break # İlk bulduğunu al ve döngüden çık
    
    if secilen_model_adi:
        # 3. Bulunan modeli hemen test et
        print(f"\n2. {secilen_model_adi} ile bağlantı kuruluyor...")
        model = genai.GenerativeModel(secilen_model_adi)
        
        cevap = model.generate_content("Bana yazılım öğrenmekle ilgili kısa, gaza getirici bir cümle söyle.")
        
        print("\n" + "="*40)
        print("🤖 GEMINI CEVABI:")
        print(cevap.text)
        print("="*40)
        print("🎉 TEBRİKLER! BAĞLANTI BAŞARILI.")
        
    else:
        print("❌ HATA: Listenin içi boş geldi veya uygun model bulunamadı.")

except Exception as e:
    print(f"\n❌ BEKLENMEYEN HATA: {e}")