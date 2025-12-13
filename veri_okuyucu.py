import json
import pandas as pd # Pandas kütüphanesini 'pd' kısaltmasıyla çağırdık

print("--- Şirket Veri Sistemi Başlatılıyor ---")

# 1. JSON Dosyasını Yükle
# Bilgisayara "personel.json dosyasını aç" diyoruz
with open('personel.json', 'r', encoding='utf-8') as f:
    ham_veri = json.load(f)

# 2. Veriyi Pandas ile Tabloya Çevir
# Veriyi Excel gibi satır-sütun formatına sokuyoruz
tablo = pd.DataFrame(ham_veri)

print("\n--- Tüm Personel Listesi ---")
print(tablo)

print("\n--- IT Departmanı Analizi ---")
# Sadece departmanı 'IT' olanları filtrele
it_calisanlari = tablo[tablo['departman'] == 'IT']
print(it_calisanlari[['isim', 'maas']]) # Sadece isim ve maaşı göster

print("\n--- Yapay Zeka Hazırlığı ---")
# İleride bu bilgiyi ChatGPT'ye "Context" olarak vereceğiz
en_yuksek_maas = tablo['maas'].max()
print(f"En yüksek maaş bilgisi ({en_yuksek_maas} TL) hafızaya alındı.")