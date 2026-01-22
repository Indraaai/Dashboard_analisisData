# 📊 E-Commerce Analytics Dashboard

Dashboard analisis data e-commerce interaktif menggunakan **Streamlit** dengan fitur filtering lengkap untuk visualisasi data bisnis.

## 🚀 Setup Environment

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
cd dashboard
streamlit run app.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## 📁 Struktur Project

```
SubmisionDicoding/
├── dashboard/
│   ├── app.py                          # File utama dashboard Streamlit
│   ├── orders_df.csv                   # Data orders (sudah dibersihkan)
│   ├── order_items_df.csv              # Data order items
│   ├── order_payments_df.csv           # Data pembayaran
│   ├── products_df.csv                 # Data produk (sudah dibersihkan)
│   ├── category_names_df.csv           # Translasi kategori produk
│   ├── reviews_df.csv                  # Data review (sudah dibersihkan)
│   ├── customers_df.csv                # Data pelanggan
│   └── sellers_df.csv                  # Data penjual
├── E-Commerce Public Dataset/          # Dataset mentah (raw)
├── Proyek_Analisis_Data.ipynb          # Notebook analisis lengkap
├── requirements.txt                    # Library dependencies
├── README.md                           # Dokumentasi project
└── url.txt                             # URL deployment
```

## ✨ Fitur Dashboard

### 📈 Halaman & Visualisasi

1. **🏠 Overview**
   - Key Metrics: Total Orders, Total Revenue, Average Rating, Total Categories
   - Filter Status Indicator (menampilkan apakah data ter-filter atau full)
   - Quick insights: Top 5 kategori terlaris dan metode pembayaran populer

2. **📊 Q1: Tren Penjualan**
   - Visualisasi tren penjualan bulanan dengan line chart
   - Annotation pada periode dengan volume tertinggi
   - Tabel Top 10 bulan dengan volume transaksi tertinggi
   - Insight otomatis periode peak sales

3. **📦 Q2: Kategori Produk**
   - Top 10 kategori berdasarkan total revenue (horizontal bar chart - Purples colormap)
   - Top 10 kategori berdasarkan volume penjualan (horizontal bar chart - Greens colormap)
   - Insight kategori dengan performa terbaik

4. **⭐ Q3: Kepuasan Pelanggan**
   - Distribusi review score (bar chart)
   - Analisis korelasi delivery time vs review score (scatter plot + trendline)
   - Tabel rata-rata delivery time per rating
   - Insight faktor yang mempengaruhi kepuasan pelanggan

5. **💳 Q4: Metode Pembayaran**
   - Distribusi metode pembayaran (horizontal bar chart - RdYlGn_r colormap)
   - Rata-rata nilai transaksi per metode pembayaran (horizontal bar chart - Viridis colormap)
   - Insight metode pembayaran dominan dan korelasi dengan nilai transaksi

### 🔍 Filter Interaktif

Dashboard dilengkapi dengan **4 filter interaktif** di sidebar:

1. **📅 Filter Periode Transaksi**
   - Date range selector (dari - sampai)
   - Default: Seluruh periode data (2016-09-04 s/d 2018-10-17)
   - Menampilkan jumlah hari yang dipilih

2. **📦 Filter Kategori Produk**
   - Mode "Semua Kategori" (default - tanpa filter)
   - Mode "Pilih Kategori Tertentu" dengan fitur:
     - Search box untuk mencari kategori
     - Multiselect dengan max 10 kategori
     - Indikator jumlah kategori terpilih

3. **🗺️ Filter Provinsi Pelanggan**
   - Mode "Semua Provinsi" (default - tanpa filter)
   - Mode "Pilih Provinsi Tertentu" dengan opsi:
     - Top 10 provinsi terbanyak (otomatis)
     - Pilih manual dengan max 15 provinsi
     - Indikator jumlah provinsi terpilih

4. **💳 Filter Metode Pembayaran**
   - Mode "Semua Metode" (default - tanpa filter)
   - Mode "Pilih Metode Tertentu" untuk analisis spesifik
   - Indikator jumlah metode terpilih

### 🎨 Fitur Tambahan

- **Status Filter Real-time**: Banner di setiap halaman yang menunjukkan apakah data ter-filter atau tidak
- **Responsive Design**: Layout yang optimal untuk berbagai ukuran layar
- **Color-coded Indicators**:
  - ✅ Hijau = Menampilkan semua data (100%)
  - ⚠️ Kuning = Filter aktif (< 100% data)
- **Data Consistency**: Semua visualisasi menggunakan data hasil cleaning yang sama dengan notebook

## 📊 Analisis Data

### Data Cleaning (Notebook)

1. **Orders Dataset**
   - Mengatasi missing values dengan modus untuk `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`
   - Konversi tipe data datetime untuk semua kolom tanggal

2. **Products Dataset**
   - Menghapus produk tanpa kategori (dropna)
   - Mengisi missing values dimensi produk dengan median

3. **Reviews Dataset**
   - Mengisi missing values `review_comment_title` dengan "No Title"
   - Mengisi missing values `review_comment_message` dengan "No Comment"

### 4 Pertanyaan Bisnis

1. **Tren Penjualan**: Bagaimana tren penjualan e-commerce dari waktu ke waktu dan periode mana yang memiliki volume transaksi tertinggi?

2. **Kategori Produk**: Kategori produk apa yang paling populer dan menghasilkan revenue tertinggi?

3. **Kepuasan Pelanggan**: Bagaimana tingkat kepuasan pelanggan berdasarkan review score dan faktor apa yang mempengaruhinya?

4. **Metode Pembayaran**: Metode pembayaran apa yang paling sering digunakan pelanggan dan bagaimana hubungannya dengan nilai transaksi?

## 🛠️ Teknologi

- **Python 3.x**
- **Streamlit**: Framework dashboard interaktif
- **Pandas**: Data manipulation dan analysis
- **Matplotlib**: Visualisasi data
- **NumPy**: Komputasi numerik

## 📝 Requirements

Lihat file `requirements.txt` untuk daftar lengkap library yang dibutuhkan:

- streamlit
- pandas
- matplotlib
- numpy

## 🎯 Cara Penggunaan

1. **Tanpa Filter (Default)**
   - Semua filter di mode "Semua" → Menampilkan 100% data
   - Visualisasi akan sama persis dengan hasil di notebook

2. **Dengan Filter**
   - Pilih mode "Pilih ... Tertentu" pada filter yang diinginkan
   - Dashboard akan otomatis update semua visualisasi
   - Banner kuning akan muncul menunjukkan persentase data yang ditampilkan

3. **Reset Filter**
   - Kembalikan semua filter ke mode "Semua"
   - Atau refresh halaman browser (Ctrl+R / Cmd+R)

## 📌 Catatan Penting

- Data yang digunakan di dashboard adalah hasil cleaning dari notebook
- Semua visualisasi konsisten dengan notebook (figsize, colormap, styling)
- Filter tidak mengubah data mentah, hanya memfilter tampilan
- Ketika tidak ada filter, dashboard menampilkan seluruh dataset (99,441 orders)
