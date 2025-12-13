# Bu bizim ilk "Yapay Zeka" simülasyonumuz

# 1. DEĞİŞKENLER (Veri Saklama Kutuları)
bot_name = "Robo-Junior"
version = 1.0

# 2. FONKSİYON (İş Yapan Makine)
# Bu fonksiyon, ileride OpenAI'a bağlanacak olan yerdir.
# Şimdilik "taklit" yapıyoruz.
def yapay_zeka_cevap_ver(soru):
    print(f"--- {bot_name} (v{version}) Düşünüyor... ---")
    
    # Basit bir mantık (If-Else)
    if "merhaba" in soru.lower():
        return "Merhaba insan! Bugün sana nasıl yardım edebilirim?"
    elif "saat" in soru.lower():
        return "Benim zaman kavramım yok ama senin için şu an kod yazma saati!"
    else:
        return "Bunu henüz anlamadım, ama öğreniyorum..."

# 3. KODU ÇALIŞTIRMA KISMI
# Kullanıcıdan (Senden) veri alalım
kullanici_sorusu = input("Sen: ")

# Fonksiyonu çağır ve cevabı al
bot_cevabi = yapay_zeka_cevap_ver(kullanici_sorusu)

# Cevabı ekrana yaz
print(f"AI: {bot_cevabi}")