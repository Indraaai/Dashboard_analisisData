# E-Commerce Analytics Dashboard

Dashboard analisis data e-commerce menggunakan Streamlit untuk visualisasi interaktif.

## Setup Environment

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## Struktur Project

```
.
├── dashboard/
│   ├── dashboard.py          # File utama dashboard
│   └── main_data.csv         # Data yang sudah dibersihkan
├── Proyek_Analisis_Data.ipynb  # Notebook analisis
└── requirements.txt          # Library dependencies
```

## Fitur Dashboard

- Overview: KPI metrics dan top categories/cities
- Tren Penjualan: Analisis penjualan dari waktu ke waktu
- Distribusi Geografis: Analisis berdasarkan lokasi
- Kategori Produk: Produk terpopuler
- Kepuasan Pelanggan: Analisis rating dan delivery time
- Metode Pembayaran: Analisis metode pembayaran
