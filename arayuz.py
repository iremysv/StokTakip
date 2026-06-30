# -*- coding: utf-8 -*-

"""
Görsel Kullanıcı Arayüzü (GUI) Modülü

Bu dosya, Tkinter kütüphanesini kullanarak stok takip sistemi için masaüstü arayüzü sunar.
`envanter_yoneticisi.py` modülü ile entegre çalışarak verileri görsel tablo üzerinde yönetir.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import envanter_yoneticisi

class StokArayuzu:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Stok Yönetim Sistemi")
        self.pencere.geometry("800x550")
        self.pencere.configure(bg="#f4f6f9")
        
        # Örnek başlangıç verileri
        self.envanter = {
            "Tabak Seti": {"kategori": "Mutfak Grubu", "adet": 25, "fiyat": 450.0},
            "Nevresim Takımı": {"kategori": "Ev Tekstili", "adet": 15, "fiyat": 750.0},
            "Cam Sürahi": {"kategori": "Züccaciye", "adet": 40, "fiyat": 120.0}
        }
        
        self.bilesenleri_olustur()
        self.tabloyu_guncelle()
        
    def bilesenleri_olustur(self):
        # Başlık Etiketi
        baslik = tk.Label(
            self.pencere, 
            text="STOK YÖNETİM SİSTEMİ", 
            font=("Helvetica", 18, "bold"), 
            bg="#2c3e50", 
            fg="white", 
            pady=10
        )
        baslik.pack(fill=tk.X)
        
        # Ana Çerçeve (Frame)
        ana_cerceve = tk.Frame(self.pencere, bg="#f4f6f9", padx=20, pady=15)
        ana_cerceve.pack(fill=tk.BOTH, expand=True)
        
        # Sol Taraf: Giriş Formu ve Butonlar
        sol_panel = tk.LabelFrame(
            ana_cerceve, 
            text=" Ürün Bilgileri ", 
            font=("Helvetica", 10, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50", 
            padx=15, 
            pady=15
        )
        sol_panel.place(x=0, y=0, width=280, height=450)
        
        # Form Alanları
        tk.Label(sol_panel, text="Ürün Adı:", bg="#f4f6f9", fg="#34495e").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_ad = tk.Entry(sol_panel, font=("Helvetica", 10))
        self.ent_ad.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(sol_panel, text="Kategori:", bg="#f4f6f9", fg="#34495e").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_kategori = ttk.Combobox(sol_panel, values=["Mutfak Grubu", "Ev Tekstili", "Züccaciye"], font=("Helvetica", 10))
        self.combo_kategori.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(sol_panel, text="Adet:", bg="#f4f6f9", fg="#34495e").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_adet = tk.Entry(sol_panel, font=("Helvetica", 10))
        self.ent_adet.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        
        tk.Label(sol_panel, text="Fiyat (TL):", bg="#f4f6f9", fg="#34495e").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_fiyat = tk.Entry(sol_panel, font=("Helvetica", 10))
        self.ent_fiyat.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        
        # Butonlar
        btn_ekle = tk.Button(sol_panel, text="Ürün Ekle / Güncelle", bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), command=self.ekle_veya_guncelle)
        btn_ekle.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")
        
        btn_sil = tk.Button(sol_panel, text="Seçili Ürünü Sil", bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"), command=self.seciliyi_sil)
        btn_sil.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
        
        btn_temizle = tk.Button(sol_panel, text="Formu Temizle", bg="#95a5a6", fg="white", font=("Helvetica", 10), command=self.formu_temizle)
        btn_temizle.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Sağ Taraf: Tablo Listesi ve Arama
        sag_panel = tk.Frame(ana_cerceve, bg="#f4f6f9")
        sag_panel.place(x=300, y=0, width=460, height=450)
        
        # Kategori Arama Paneli
        arama_cerceve = tk.Frame(sag_panel, bg="#f4f6f9")
        arama_cerceve.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(arama_cerceve, text="Kategori Ara:", bg="#f4f6f9", fg="#34495e").pack(side=tk.LEFT, padx=5)
        self.ent_arama = tk.Entry(arama_cerceve, font=("Helvetica", 10), width=15)
        self.ent_arama.pack(side=tk.LEFT, padx=5)
        
        btn_ara = tk.Button(arama_cerceve, text="Filtrele", bg="#3498db", fg="white", command=self.kategori_filtrele)
        btn_ara.pack(side=tk.LEFT, padx=5)
        
        btn_hepsi = tk.Button(arama_cerceve, text="Temizle", bg="#95a5a6", fg="white", command=self.tabloyu_guncelle)
        btn_hepsi.pack(side=tk.LEFT, padx=5)
        
        # Tablo Tasarımı (Treeview)
        sutunlar = ("ad", "kategori", "adet", "fiyat")
        self.tablo = ttk.Treeview(sag_panel, columns=sutunlar, show="headings")
        
        self.tablo.heading("ad", text="Ürün Adı")
        self.tablo.heading("kategori", text="Kategori")
        self.tablo.heading("adet", text="Adet")
        self.tablo.heading("fiyat", text="Fiyat (TL)")
        
        self.tablo.column("ad", width=120, anchor="w")
        self.tablo.column("kategori", width=120, anchor="center")
        self.tablo.column("adet", width=80, anchor="center")
        self.tablo.column("fiyat", width=100, anchor="e")
        
        self.tablo.pack(fill=tk.BOTH, expand=True)
        self.tablo.bind("<<TreeviewSelect>>", self.tablodan_sec)
        
    def tabloyu_guncelle(self, filtre_kategori=None):
        # Önce tablodaki tüm eski verileri temizliyoruz
        for row in self.tablo.get_children():
            self.tablo.delete(row)
            
        for urun_adi, detaylar in self.envanter.items():
            if filtre_kategori:
                if detaylar['kategori'].lower() != filtre_kategori.lower():
                    continue
            self.tablo.insert("", tk.END, values=(urun_adi, detaylar['kategori'], detaylar['adet'], f"{detaylar['fiyat']:.2f}"))
            
    def ekle_veya_guncelle(self):
        ad = self.ent_ad.get().strip()
        kategori = self.combo_kategori.get().strip()
        adet_str = self.ent_adet.get().strip()
        fiyat_str = self.ent_fiyat.get().strip()
        
        if not ad or not kategori or not adet_str or not fiyat_str:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
            
        try:
            adet = int(adet_str)
            fiyat = float(fiyat_str.replace(",", "."))
            if adet < 0 or fiyat < 0:
                raise ValueError("Değerler sıfırdan küçük olamaz.")
        except ValueError:
            messagebox.showerror("Hata", "Adet tam sayı, Fiyat sayısal bir değer (örn: 10.5) olmalıdır!")
            return
            
        # Logic katmanındaki fonksiyonumuzu çağırarak verimizi yönetiyoruz
        envanter_yoneticisi.urun_ekle(self.envanter, ad, kategori, adet, fiyat)
        self.tabloyu_guncelle()
        self.formu_temizle()
        messagebox.showinfo("Başarılı", f"'{ad}' envantere kaydedildi / güncellendi.")
        
    def seciliyi_sil(self):
        secili_item = self.tablo.selection()
        if not secili_item:
            messagebox.showwarning("Seçim Yapılmadı", "Lütfen silmek istediğiniz ürünü tablodan seçin.")
            return
            
        degerler = self.tablo.item(secili_item[0], "values")
        urun_adi = degerler[0]
        
        cevap = messagebox.askyesno("Silme Onayı", f"'{urun_adi}' ürününü silmek istediğinize emin misiniz?")
        if cevap:
            envanter_yoneticisi.urun_sil(self.envanter, urun_adi)
            self.tabloyu_guncelle()
            self.formu_temizle()
            
    def kategori_filtrele(self):
        kategori = self.ent_arama.get().strip()
        if not kategori:
            self.tabloyu_guncelle()
        else:
            self.tabloyu_guncelle(filtre_kategori=kategori)
            
    def tablodan_sec(self, event):
        secili_item = self.tablo.selection()
        if secili_item:
            degerler = self.tablo.item(secili_item[0], "values")
            self.formu_temizle()
            self.ent_ad.insert(0, degerler[0])
            self.combo_kategori.set(degerler[1])
            self.ent_adet.insert(0, degerler[2])
            self.ent_fiyat.insert(0, degerler[3])
            
    def formu_temizle(self):
        self.ent_ad.delete(0, tk.END)
        self.combo_kategori.set("")
        self.ent_adet.delete(0, tk.END)
        self.ent_fiyat.delete(0, tk.END)

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = StokArayuzu(pencere)
    pencere.mainloop()
