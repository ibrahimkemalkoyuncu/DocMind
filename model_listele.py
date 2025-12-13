import google.generativeai as genai

print("--- Google Yapay Zeka Model Listesi ---")

# API Anahtarını buraya yapıştır
genai.configure(api_key="AIzaSyCWnhF7ST5jH0xBEpZAOsm7XKd9NBaXwfQ")

try:
    print("Mevcut modeller taranıyor...\n")
    
    # Google'a soruyoruz: "Elimde hangi modeller var?"
    for model in genai.list_models():
        # Sadece "sohbet edebilen" (generateContent) modelleri filtrele
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ Bulunan Model: {model.name}")
            
except Exception as e:
    print(f"❌ Hata: {e}")