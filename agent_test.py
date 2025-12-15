import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from ddgs import DDGS # Yeni kütüphane ismi

# 1. Ayarlar
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

print("--- AGENT MODU v2: Stabil Sürüm ---")
print("UYARI: Dakikada en fazla 5 soru sorabilirsin (Bedava Google Kotası).")

# 2. Araçlar (Tools)

def internette_ara(sorgu):
    """Güncel olayları, döviz kurlarını veya bilinmeyen konuları internette arar."""
    print(f"\n⚙️ [ARAÇ]: DuckDuckGo (TR) aranıyor: '{sorgu}'...")
    try:
        with DDGS() as ddgs:
            # region='tr-tr' ile Türkiye sonuçlarını zorluyoruz
            results = list(ddgs.text(sorgu, region='tr-tr', max_results=3))
            if results:
                return str(results)
            return "İnternette sonuç bulunamadı."
    except Exception as e:
        return f"Arama hatası: {e}"

def hesap_makinesi(islem):
    """Matematiksel işlemleri yapar. Örn: '25 * 4', '100 / 5' """
    print(f"\n⚙️ [ARAÇ]: Hesap yapılıyor: '{islem}'...")
    try:
        # Sadece güvenli karakterlere izin verelim
        allowed = set("0123456789+-*/(). ")
        if not set(islem).issubset(allowed):
            return "Hatalı karakter içeren işlem."
        return str(eval(islem))
    except:
        return "Hesaplama hatası."

araclar = [internette_ara, hesap_makinesi]

# 3. Model Başlatma
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=araclar
)

# Sohbeti başlat
chat = model.start_chat(enable_automatic_function_calling=True)

# --- DÖNGÜ ---
while True:
    soru = input("\nMERAK ETTİĞİN ŞEY (Çıkış 'q'): ")
    if soru.lower() == 'q':
        break
    
    try:
        response = chat.send_message(soru)
        print(f"\n🤖 AGENT: {response.text}")
        
    except Exception as e:
        if "429" in str(e):
            print("\n🛑 HIZ LİMİTİ! Çok hızlı sordun.")
            print("Google: 'Dakikada 5 soru hakkın doldu. Biraz bekle...'")
            print("⏳ 10 saniye otomatik bekleniyor...")
            time.sleep(10)
            print("✅ Tekrar deneyebilirsin.")
        else:
            print(f"\n❌ HATA: {e}")