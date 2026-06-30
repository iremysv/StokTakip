# -*- coding: utf-8 -*-

"""
Envanter Yönetim Modülü

Bu dosya, stok takip sistemimizin verilerini yöneten fonksiyonları içerir.
Veri Yapısı Tercihi:
- Envanter bilgisini tutmak için Python'daki Sözlük (Dictionary) veri yapısını tercih ettik.
- Sözlükler, anahtar-değer (key-value) mantığıyla çalışır ve bir ürüne ismi (anahtar) üzerinden 
  çok hızlı bir şekilde erişmemizi sağlar.
"""

def urun_ekle(envanter, ad, kategori, adet, fiyat):
    """
    Envantere yeni bir ürün ekler veya ürün zaten varsa adet ve fiyatını günceller.
    """
    # Ürün adını standart hale getirmek için baş harflerini büyük yapıyoruz (örn: "ütü" -> "Ütü")
    urun_adi = ad.strip().title()
    
    if urun_adi in envanter:
        # Ürün zaten varsa sadece adedini artırıp yeni fiyatını güncelleyebiliriz
        envanter[urun_adi]['adet'] += adet
        envanter[urun_adi]['fiyat'] = fiyat
        print(f"\n[BİLGİ] {urun_adi} zaten envanterde vardı. Adedi artırıldı, fiyatı güncellendi.")
    else:
        # Yeni ürünü sözlük olarak envantere ekliyoruz
        envanter[urun_adi] = {
            'kategori': kategori.strip().title(),
            'adet': adet,
            'fiyat': fiyat
        }
        print(f"\n[BAŞARILI] {urun_adi} envantere başarıyla eklendi.")

def urun_sil(envanter, ad):
    """
    Belirtilen ürünü envanterden siler.
    """
    urun_adi = ad.strip().title()
    if urun_adi in envanter:
        del envanter[urun_adi]
        print(f"\n[BAŞARILI] {urun_adi} envanterden silindi.")
        return True
    else:
        print(f"\n[HATA] {urun_adi} adında bir ürün bulunamadı.")
        return False

def urun_guncelle(envanter, ad, adet, fiyat):
    """
    Belirtilen ürünün adet ve fiyat bilgilerini günceller.
    """
    urun_adi = ad.strip().title()
    if urun_adi in envanter:
        envanter[urun_adi]['adet'] = adet
        envanter[urun_adi]['fiyat'] = fiyat
        print(f"\n[BAŞARILI] {urun_adi} bilgileri güncellendi.")
        return True
    else:
        print(f"\n[HATA] {urun_adi} adında bir ürün bulunamadı.")
        return False

def envanteri_listele(envanter):
    """
    Envanterdeki tüm ürünleri listeler.
    """
    if not envanter:
        print("\n[BİLGİ] Envanteriniz şu anda boş.")
        return
    
    print("\n--- Güncel Envanter Listesi ---")
    for urun_adi, detaylar in envanter.items():
        print(f"Ürün: {urun_adi} | Kategori: {detaylar['kategori']} | Adet: {detaylar['adet']} | Fiyat: {detaylar['fiyat']} TL")
    print("--------------------------------")

def kategoriye_gore_listele(envanter, kategori):
    """
    Sadece belirtilen kategoriye ait ürünleri listeler.
    """
    hedef_kategori = kategori.strip().title()
    bulunanlar = {ad: detay for ad, detay in envanter.items() if detay['kategori'] == hedef_kategori}
    
    if not bulunanlar:
        print(f"\n[BİLGİ] '{hedef_kategori}' kategorisinde ürün bulunamadı.")
        return
    
    print(f"\n--- {hedef_kategori} Kategorisindeki Ürünler ---")
    for urun_adi, detaylar in bulunanlar.items():
        print(f"Ürün: {urun_adi} | Adet: {detaylar['adet']} | Fiyat: {detaylar['fiyat']} TL")
    print("--------------------------------")
