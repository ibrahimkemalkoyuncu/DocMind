# import requests # İnternete çıkış kapımız
# import time

# print("--- Finans Botu Başlatılıyor ---")

# def fiyat_getir():
#     # 1. Adres Belirle (URL)
#     adres = "https://api.coindesk.com/v1/bpi/currentprice.json"
    
#     # 2. İsteği Gönder (Telefon açmak gibi)
#     print("Sunucuya bağlanılıyor...")
#     cevap = requests.get(adres)
    
#     # 3. Cevabı Kontrol Et (200 = Başarılı, 404 = Bulunamadı)
#     if cevap.status_code == 200:
#         # Gelen veriyi JSON formatına (Sözlüğe) çevir
#         veri = cevap.json()
        
#         # JSON'ın içindeki veriyi ayıkla (Veri Madenciliği)
#         fiyat = veri["bpi"]["USD"]["rate"]
#         zaman = veri["time"]["updated"]
        
#         print(f"✅ BAŞARILI!")
#         print(f"⏰ Zaman: {zaman}")
#         print(f"💰 Güncel Bitcoin Fiyatı: ${fiyat}")
#     else:
#         print("❌ Hata oluştu! Sunucu cevap vermiyor.")

# # Fonksiyonu çalıştır
# fiyat_getir()


import requests
import time

print("--- Bağlantı Test Botu (v2) ---")

def baglanti_testi():
    # 1. YENİ ADRES (Her yerde çalışan güvenli test adresi)
    # Bu site bize basit bir "Yapılacaklar Listesi" maddesi verir.
    adres = "https://jsonplaceholder.typicode.com/todos/1"
    
    print(f"Sunucuya bağlanılıyor: {adres} ...")
    
    try:
        # İsteği gönder
        cevap = requests.get(adres)
        
        if cevap.status_code == 200:
            veri = cevap.json()
            
            # Gelen veriyi ekrana basalım
            print("\n✅ BAŞARILI! İnternete çıkış var.")
            print("-" * 30)
            print(f"📄 Gelen Başlık: {veri['title']}")
            print(f"🆔 ID Numarası: {veri['id']}")
            print(f"Is Completed: {veri['completed']}")
            print("-" * 30)
        else:
            print(f"❌ Sunucu hatası: {cevap.status_code}")
            
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")

# Çalıştır
baglanti_testi()