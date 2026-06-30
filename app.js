/**
 * Envanter Yönetimi JavaScript Mantığı
 * 
 * Bu dosya envanter verilerini yönetir, localStorage kullanarak verileri tarayıcıda
 * saklar ve DOM manipülasyonu ile arayüzü günceller.
 */

// Sayfa yüklendiğinde çalışacak başlangıç verileri
const varsayilanEnvanter = [
    { id: 1, ad: "Tabak Seti", kategori: "Mutfak Grubu", adet: 25, fiyat: 450.0 },
    { id: 2, ad: "Nevresim Takımı", kategori: "Ev Tekstili", adet: 15, fiyat: 750.0 },
    { id: 3, ad: "Cam Sürahi", kategori: "Züccaciye", adet: 40, fiyat: 120.0 }
];

// Verileri Yerel Depodan (localStorage) Çek veya Varsayılanları Yükle
let envanter = JSON.parse(localStorage.getItem('envanter')) || varsayilanEnvanter;

// DOM Elemanları
const form = document.getElementById('stok-form');
const editModeIdInput = document.getElementById('edit-mode-id');
const urunAdInput = document.getElementById('urun-ad');
const urunKategoriSelect = document.getElementById('urun-kategori');
const urunAdetInput = document.getElementById('urun-adet');
const urunFiyatInput = document.getElementById('urun-fiyat');
const btnSubmit = document.getElementById('btn-submit');
const btnClear = document.getElementById('btn-clear');

const tbody = document.getElementById('inventory-tbody');
const searchKategoriInput = document.getElementById('search-kategori');
const btnFilter = document.getElementById('btn-filter');
const btnReset = document.getElementById('btn-reset');

const statTotalTypes = document.getElementById('stat-total-types');
const statTotalQuantity = document.getElementById('stat-total-quantity');
const statTotalValue = document.getElementById('stat-total-value');

// Arayüzü Güncelleme / Tabloyu Çizdirme
function tabloyuCiz(filtreKategori = '') {
    tbody.innerHTML = '';
    let filteredList = envanter;
    
    if (filtreKategori.trim() !== '') {
        filteredList = envanter.filter(urun => 
            urun.kategori.toLowerCase().includes(filtreKategori.toLowerCase())
        );
    }

    filteredList.forEach(urun => {
        const tr = document.createElement('tr');
        
        // Satıra tıklandığında bilgileri forma yükleme
        tr.addEventListener('click', () => formuYukle(urun));
        
        const toplamDeger = urun.adet * urun.fiyat;
        
        tr.innerHTML = `
            <td><strong>${urun.ad}</strong></td>
            <td><span class="badge badge-kategori">${urun.kategori}</span></td>
            <td class="text-center">${urun.adet}</td>
            <td class="text-right">${urun.fiyat.toFixed(2)} TL</td>
            <td class="text-right">${toplamDeger.toFixed(2)} TL</td>
            <td class="text-center" onclick="event.stopPropagation()">
                <div class="action-buttons">
                    <button class="btn btn-secondary" onclick="formuYukleById(${urun.id})">Düzenle</button>
                    <button class="btn btn-danger" onclick="urunSil(${urun.id})">Sil</button>
                </div>
            </td>
        `;
        
        tbody.appendChild(tr);
    });

    istatistikleriGuncelle();
}

// İstatistikleri Güncelleme
function istatistikleriGuncelle() {
    const toplamTur = envanter.length;
    const toplamAdet = envanter.reduce((toplam, urun) => toplam + urun.adet, 0);
    const toplamDeger = envanter.reduce((toplam, urun) => toplam + (urun.adet * urun.fiyat), 0);

    statTotalTypes.textContent = toplamTur;
    statTotalQuantity.textContent = toplamAdet;
    statTotalValue.textContent = `${toplamDeger.toFixed(2)} TL`;
}

// Veriyi Kaydetme (Yerel Depolama)
function veriyiKaydet() {
    localStorage.setItem('envanter', JSON.stringify(envanter));
}

// Formu Temizleme
function formuTemizle() {
    form.reset();
    editModeIdInput.value = '';
    btnSubmit.textContent = 'Kaydet';
    btnSubmit.className = 'btn btn-success';
}

// Satıra Tıklayınca Formu Doldurma
function formuYukle(urun) {
    editModeIdInput.value = urun.id;
    urunAdInput.value = urun.ad;
    urunKategoriSelect.value = urun.kategori;
    urunAdetInput.value = urun.adet;
    urunFiyatInput.value = urun.fiyat;
    btnSubmit.textContent = 'Güncelle';
    btnSubmit.className = 'btn btn-primary';
}

function formuYukleById(id) {
    const urun = envanter.find(u => u.id === id);
    if (urun) {
        formuYukle(urun);
    }
}

// Ürün Silme
window.urunSil = function(id) {
    if (confirm("Bu ürünü silmek istediğinize emin misiniz?")) {
        envanter = envanter.filter(urun => urun.id !== id);
        veriyiKaydet();
        tabloyuCiz();
        formuTemizle();
    }
};

// Form Gönderimi (Ekle / Güncelle)
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const id = editModeIdInput.value;
    const ad = urunAdInput.value.trim();
    const kategori = urunKategoriSelect.value;
    const adet = parseInt(urunAdetInput.value);
    const fiyat = parseFloat(urunFiyatInput.value);

    if (id) {
        // Güncelleme Modu
        const urunIndex = envanter.findIndex(u => u.id == id);
        if (urunIndex !== -1) {
            envanter[urunIndex] = { id: parseInt(id), ad, kategori, adet, fiyat };
        }
    } else {
        // Ekleme Modu
        const yeniId = envanter.length > 0 ? Math.max(...envanter.map(u => u.id)) + 1 : 1;
        envanter.push({ id: yeniId, ad, kategori, adet, fiyat });
    }

    veriyiKaydet();
    tabloyuCiz();
    formuTemizle();
});

// Temizle Butonu
btnClear.addEventListener('click', formuTemizle);

// Filtreleme
btnFilter.addEventListener('click', () => {
    tabloyuCiz(searchKategoriInput.value);
});

btnReset.addEventListener('click', () => {
    searchKategoriInput.value = '';
    tabloyuCiz();
});

// Arama kutusuna yazarken anlık filtreleme desteği
searchKategoriInput.addEventListener('input', () => {
    tabloyuCiz(searchKategoriInput.value);
});

// İlk Başlangıç
tabloyuCiz();
