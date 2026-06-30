# -*- coding: utf-8 -*-

"""
Ana Takip Programı

Bu dosya, kullanıcıyla etkileşime geçen konsol tabanlı arayüzü barındırır.
`envanter_yoneticisi.py` modülündeki fonksiyonları içe aktararak (import) kullanır.
"""

import envanter_yoneticisi

def menu_goster():
    print("\n==================================")
    print("      STOK TAKİP SİSTEMİ          ")
    print("==================================")
    print("1. Tüm Envanteri Listele")
    print("2. Yeni Ürün Ekle")
    print("3. Ürün Güncelle (Adet/Fiyat)")
    print("4. Ürün Sil")
    print("5. Kategoriye Göre Ürünleri Listele")
    print("6. Çıkış")
    print("==================================")

def ana_akis():
    # Program başlangıcında örnek verilerle dolu bir envanter sözlüğü oluşturuyoruz.
    # Böylece programı test etmek çok daha kolay olacaktır.
    envanter = {
        "Tabak Seti": {"kategori": "Mutfak Grubu", "adet": 25, "fiyat": 450.0},
        "Nevresim Takımı": {"kategori": "Ev Tekstili", "adet": 15, "fiyat": 750.0},
        "Cam Sürahi": {"kategori": "Züccaciye", "adet": 40, "fiyat": 120.0}
    }
    
    while True:
        menu_goster()
        secim = input("Lütfen yapmak istediğiniz işlemi seçin (1-6): ").strip()
        
        if secim == "1":
            envanter_yoneticisi.envanteri_listele(envanter)
            
        elif secim == "2":
            print("\n--- Yeni Ürün Ekle ---")
            ad = input("Ürün Adı: ")
            kategori = input("Kategori (Züccaciye / Mutfak Grubu / Ev Tekstili vb.): ")
            try:
                adet = int(input("Adet: "))
                fiyat = float(input("Fiyat (TL): "))
                envanter_yoneticisi.urun_ekle(envanter, ad, kategori, adet, fiyat)
            except ValueError:
                print("\n[HATA] Adet tam sayı, fiyat ise sayısal bir değer olmalıdır!")
                
        elif secim == "3":
            print("\n--- Ürün Güncelle ---")
            ad = input("Güncellenecek Ürün Adı: ")
            try:
                yeni_adet = int(input("Yeni Adet: "))
                yeni_fiyat = float(input("Yeni Fiyat (TL): "))
                envanter_yoneticisi.urun_guncelle(envanter, ad, yeni_adet, yeni_fiyat)
            except ValueError:
                print("\n[HATA] Adet tam sayı, fiyat ise sayısal bir değer olmalıdır!")
                
        elif secim == "4":
            print("\n--- Ürün Sil ---")
            ad = input("Silinecek Ürün Adı: ")
            envanter_yoneticisi.urun_sil(envanter, ad)
            
        elif secim == "5":
            print("\n--- Kategoriye Göre Listele ---")
            kategori = input("Filtrelenecek Kategori: ")
            envanter_yoneticisi.kategoriye_gore_listele(envanter, kategori)
            
        elif secim == "6":
            print("\nStok Takip Sisteminden çıkılıyor. İyi günler!")
            break
        else:
            print("\n[HATA] Geçersiz seçim! Lütfen 1 ile 6 arasında bir sayı girin.")

if __name__ == "__main__":
    ana_akis()
