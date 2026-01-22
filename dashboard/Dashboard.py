import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data dengan caching
@st.cache_data
def load_data():
    # Gunakan path relatif
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'main_data.csv')
    df = pd.read_csv(data_path)
    # Convert datetime columns
    datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                     'order_delivered_carrier_date', 'order_delivered_customer_date',
                     'order_estimated_delivery_date', 'review_creation_date',
                     'review_answer_timestamp']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

# Load data
try:
    df = load_data()
    
    # Header
    st.title("🛒 E-Commerce Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Menu Navigasi")
    st.sidebar.markdown("Pilih analisis yang ingin ditampilkan:")
    
    menu = st.sidebar.radio(
        "Pilih Halaman:",
        ["🏠 Overview", "📈 Tren Penjualan", "🗺️ Distribusi Geografis", 
         "📦 Kategori Produk", "⭐ Kepuasan Pelanggan", "💳 Metode Pembayaran"]
    )
    
    # ===========================
    # FITUR INTERAKTIF - FILTERS
    # ===========================
    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Filter Data Interaktif")
    
    # Filter Date Range
    st.sidebar.subheader("📅 Filter Rentang Tanggal")
    min_date = df['order_purchase_timestamp'].min().date()
    max_date = df['order_purchase_timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter data berdasarkan tanggal pembelian"
    )
    
    # Filter Kategori Produk
    st.sidebar.subheader("📦 Filter Kategori Produk")
    all_categories = ['Semua Kategori'] + sorted(df['product_category_name_english'].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Pilih Kategori:",
        options=all_categories,
        help="Filter data berdasarkan kategori produk"
    )
    
    # Filter State/Provinsi
    st.sidebar.subheader("🗺️ Filter Provinsi")
    all_states = ['Semua Provinsi'] + sorted(df['customer_state'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox(
        "Pilih Provinsi:",
        options=all_states,
        help="Filter data berdasarkan provinsi pelanggan"
    )
    
    # Apply Filters
    df_filtered = df.copy()
    
    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered['order_purchase_timestamp'].dt.date >= start_date) & 
            (df_filtered['order_purchase_timestamp'].dt.date <= end_date)
        ]
    
    # Apply category filter
    if selected_category != 'Semua Kategori':
        df_filtered = df_filtered[df_filtered['product_category_name_english'] == selected_category]
    
    # Apply state filter
    if selected_state != 'Semua Provinsi':
        df_filtered = df_filtered[df_filtered['customer_state'] == selected_state]
    
    # Display filter info
    if len(df_filtered) < len(df):
        st.sidebar.markdown("---")
        st.sidebar.success(f"✅ Filter Aktif: {len(df_filtered):,} dari {len(df):,} data")
        
        # Reset filter button
        if st.sidebar.button("🔄 Reset Semua Filter"):
            st.rerun()
    
    # Use filtered data for all visualizations
    df = df_filtered
    
    # ===========================
    # HALAMAN OVERVIEW
    # ===========================
    if menu == "🏠 Overview":
        st.header("Overview Bisnis E-Commerce")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = df['order_id'].nunique()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Total Orders</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>{total_orders:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_customers = df['customer_unique_id'].nunique()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Total Customers</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>{total_customers:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_revenue = df['price'].sum()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Total Revenue</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>R$ {total_revenue/1000000:.2f}M</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_rating = df['review_score'].mean()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Avg Rating</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>{avg_rating:.2f} / 5.0</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Additional Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_products = df['product_id'].nunique()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Total Produk</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>{total_products:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_categories = df['product_category_name_english'].nunique()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Total Kategori</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>{total_categories}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_order_value = df.groupby('order_id')['price'].sum().mean()
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: #0e1117; margin: 0;'>Avg Order Value</h4>
                <h2 style='color: #0e1117; margin: 10px 0;'>R$ {avg_order_value:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Overview insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 5 Kategori Produk Terlaris")
            top_categories = df.groupby('product_category_name_english').agg({
                'order_id': 'count'
            }).rename(columns={'order_id': 'Total Orders'}).sort_values('Total Orders', ascending=False).head(5).reset_index()
            top_categories.columns = ['Kategori Produk', 'Total Orders']
            st.dataframe(top_categories, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Top 5 Kota dengan Pesanan Terbanyak")
            top_cities = df.groupby('customer_city').agg({
                'order_id': 'count'
            }).rename(columns={'order_id': 'Total Orders'}).sort_values('Total Orders', ascending=False).head(5).reset_index()
            top_cities.columns = ['Kota', 'Total Orders']
            st.dataframe(top_cities, use_container_width=True, hide_index=True)
    
    # ===========================
    # HALAMAN TREN PENJUALAN
    # ===========================
    elif menu == "📈 Tren Penjualan":
        st.header("📈 Tren Penjualan dari Waktu ke Waktu")
        
        # Prepare data
        df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M')
        monthly_sales = df.groupby('year_month').agg({
            'order_id': 'count'
        }).rename(columns={'order_id': 'total_orders'}).reset_index()
        monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
        
        # Visualisasi Tren Penjualan Bulanan
        st.subheader("📊 Tren Penjualan Bulanan")
        
        fig, ax = plt.subplots(figsize=(16, 7))
        ax.plot(range(len(monthly_sales)), monthly_sales['total_orders'], 
                marker='o', linewidth=2.5, markersize=8, color='#2E86AB', markerfacecolor='#A23B72')
        ax.set_title('Tren Penjualan Bulanan E-Commerce', fontsize=18, fontweight='bold', pad=20)
        ax.set_xlabel('Periode (Bulan)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Jumlah Pesanan', fontsize=14, fontweight='bold')
        ax.set_xticks(range(0, len(monthly_sales), 2))
        ax.set_xticklabels(monthly_sales['year_month'][::2], rotation=45, ha='right', fontsize=11)
        
        # Highlight max and min
        max_idx = monthly_sales['total_orders'].idxmax()
        min_idx = monthly_sales['total_orders'].idxmin()
        ax.annotate(f"{monthly_sales.loc[max_idx, 'total_orders']:,.0f} orders", 
                    xy=(max_idx, monthly_sales.loc[max_idx, 'total_orders']),
                    xytext=(10, 10), textcoords='offset points', fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Top 10 Bulan
        st.subheader("🏆 Top 10 Bulan dengan Volume Transaksi Tertinggi")
        top_months = monthly_sales.sort_values('total_orders', ascending=False).head(10)
        st.dataframe(top_months, use_container_width=True)
    
    # ===========================
    # HALAMAN DISTRIBUSI GEOGRAFIS
    # ===========================
    elif menu == "🗺️ Distribusi Geografis":
        st.header("🗺️ Distribusi Geografis Pelanggan dan Penjualan")
        
        # Prepare data
        sales_by_city = df.groupby('customer_city').agg({
            'order_id': 'count',
            'price': 'sum'
        }).rename(columns={'order_id': 'total_orders', 'price': 'total_revenue'}).sort_values('total_revenue', ascending=False).reset_index()
        
        sales_by_state = df.groupby('customer_state').agg({
            'order_id': 'count',
            'price': 'sum'
        }).rename(columns={'order_id': 'total_orders', 'price': 'total_revenue'}).sort_values('total_revenue', ascending=False).reset_index()
        
        # Top 10 Kota
        st.subheader("🏙️ Top 10 Kota Berdasarkan Pendapatan")
        
        fig, ax = plt.subplots(figsize=(12, 7))
        top_cities_revenue = sales_by_city.head(10)
        bars = ax.barh(range(len(top_cities_revenue)), top_cities_revenue['total_revenue'], 
                      color='steelblue', edgecolor='navy', linewidth=1.2)
        ax.set_yticks(range(len(top_cities_revenue)))
        ax.set_yticklabels(top_cities_revenue['customer_city'], fontsize=11, fontweight='bold')
        ax.set_xlabel('Total Pendapatan (R$)', fontsize=13, fontweight='bold')
        ax.set_title('Top 10 Kota Berdasarkan Pendapatan', fontsize=15, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (idx, row) in enumerate(top_cities_revenue.iterrows()):
            ax.text(row['total_revenue'], i, f" R$ {row['total_revenue']:,.0f}", 
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Top 10 State
        st.subheader("🗺️ Top 10 Provinsi Berdasarkan Pendapatan")
        
        fig, ax = plt.subplots(figsize=(12, 7))
        top_states_revenue = sales_by_state.head(10)
        bars = ax.barh(range(len(top_states_revenue)), top_states_revenue['total_revenue'], 
                      color='coral', edgecolor='darkred', linewidth=1.2)
        ax.set_yticks(range(len(top_states_revenue)))
        ax.set_yticklabels(top_states_revenue['customer_state'], fontsize=11, fontweight='bold')
        ax.set_xlabel('Total Pendapatan (R$)', fontsize=13, fontweight='bold')
        ax.set_title('Top 10 Provinsi Berdasarkan Pendapatan', fontsize=15, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (idx, row) in enumerate(top_states_revenue.iterrows()):
            ax.text(row['total_revenue'], i, f" R$ {row['total_revenue']:,.0f}", 
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # ===========================
    # HALAMAN KATEGORI PRODUK
    # ===========================
    elif menu == "📦 Kategori Produk":
        st.header("📦 Analisis Kategori Produk Terpopuler")
        
        # Prepare data
        category_popularity = df.groupby('product_category_name_english').agg({
            'order_id': 'count',
            'price': 'sum'
        }).rename(columns={'order_id': 'total_items_sold', 'price': 'total_revenue'}).sort_values('total_items_sold', ascending=False).reset_index()
        category_popularity['avg_price'] = category_popularity['total_revenue'] / category_popularity['total_items_sold']
        
        # Top 10 by Revenue
        st.subheader("💰 Top 10 Kategori Berdasarkan Pendapatan")
        
        fig, ax = plt.subplots(figsize=(12, 7))
        category_by_revenue = category_popularity.sort_values('total_revenue', ascending=False)
        top_category_rev = category_by_revenue.head(10)
        colors_rev = plt.cm.Purples(np.linspace(0.4, 0.8, len(top_category_rev)))
        bars = ax.barh(range(len(top_category_rev)), top_category_rev['total_revenue'], 
                      color=colors_rev, edgecolor='indigo', linewidth=1.2)
        ax.set_yticks(range(len(top_category_rev)))
        ax.set_yticklabels(top_category_rev['product_category_name_english'], fontsize=10, fontweight='bold')
        ax.set_xlabel('Total Pendapatan (R$)', fontsize=13, fontweight='bold')
        ax.set_title('Top 10 Kategori Produk Terlaris (Berdasarkan Pendapatan)', fontsize=14, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (idx, row) in enumerate(top_category_rev.iterrows()):
            ax.text(row['total_revenue'], i, f" R$ {row['total_revenue']:,.0f}", 
                   va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Top 10 by Volume
        st.subheader("📊 Top 10 Kategori Berdasarkan Volume Penjualan")
        
        fig, ax = plt.subplots(figsize=(12, 7))
        top_category_vol = category_popularity.head(10)
        colors_vol = plt.cm.Greens(np.linspace(0.4, 0.8, len(top_category_vol)))
        bars = ax.barh(range(len(top_category_vol)), top_category_vol['total_items_sold'], 
                      color=colors_vol, edgecolor='darkgreen', linewidth=1.2)
        ax.set_yticks(range(len(top_category_vol)))
        ax.set_yticklabels(top_category_vol['product_category_name_english'], fontsize=10, fontweight='bold')
        ax.set_xlabel('Jumlah Produk Terjual', fontsize=13, fontweight='bold')
        ax.set_title('Top 10 Kategori Produk Terlaris (Berdasarkan Volume)', fontsize=14, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (idx, row) in enumerate(top_category_vol.iterrows()):
            ax.text(row['total_items_sold'], i, f" {row['total_items_sold']:,.0f}", 
                   va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # ===========================
    # HALAMAN KEPUASAN PELANGGAN
    # ===========================
    elif menu == "⭐ Kepuasan Pelanggan":
        st.header("⭐ Tingkat Kepuasan Pelanggan")
        
        # Distribusi Review Score
        st.subheader("📊 Distribusi Rating Kepuasan Pelanggan")
        
        review_dist = df['review_score'].value_counts().sort_index()
        review_pct = (review_dist / review_dist.sum() * 100).round(1)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = ['#d62728', '#ff7f0e', '#ffdd57', '#90ee90', '#2ca02c']
        bars = ax.bar(review_dist.index, review_dist.values, color=colors, 
                     edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_xlabel('Rating Kepuasan (1=Sangat Buruk, 5=Sangat Baik)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Jumlah Ulasan', fontsize=12, fontweight='bold')
        ax.set_title('Distribusi Rating Kepuasan Pelanggan', fontsize=15, fontweight='bold', pad=15)
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(['⭐\n1', '⭐⭐\n2', '⭐⭐⭐\n3', '⭐⭐⭐⭐\n4', '⭐⭐⭐⭐⭐\n5'], fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}\n({review_pct.iloc[i]}%)',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Delivery Time vs Rating
        st.subheader("🚚 Pengaruh Waktu Pengiriman terhadap Rating")
        
        df_delivery = df.dropna(subset=['order_delivered_customer_date', 'order_purchase_timestamp', 'review_score'])
        df_delivery['delivery_time'] = (df_delivery['order_delivered_customer_date'] - df_delivery['order_purchase_timestamp']).dt.days
        
        delivery_by_score = df_delivery.groupby('review_score')['delivery_time'].agg(['mean', 'median', 'count']).round(2)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        delivery_means = delivery_by_score['mean'].values
        review_scores = delivery_by_score.index.values
        ax.plot(review_scores, delivery_means, marker='o', linewidth=3, markersize=12, 
               color='steelblue', markerfacecolor='orange', markeredgewidth=2, markeredgecolor='darkblue')
        ax.set_xlabel('Rating Kepuasan', fontsize=12, fontweight='bold')
        ax.set_ylabel('Rata-rata Waktu Pengiriman (hari)', fontsize=12, fontweight='bold')
        ax.set_title('Pengaruh Waktu Pengiriman terhadap Rating\n(Semakin Cepat = Semakin Puas)', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(['⭐\n1', '⭐⭐\n2', '⭐⭐⭐\n3', '⭐⭐⭐⭐\n4', '⭐⭐⭐⭐⭐\n5'], fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        for score, days in zip(review_scores, delivery_means):
            ax.annotate(f'{days:.1f} hari', xy=(score, days), 
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # ===========================
    # HALAMAN METODE PEMBAYARAN
    # ===========================
    elif menu == "💳 Metode Pembayaran":
        st.header("💳 Analisis Metode Pembayaran dan Nilai Transaksi")
        
        # Distribusi Metode Pembayaran
        st.subheader("📊 Distribusi Metode Pembayaran")
        
        payment_dist = df['payment_type'].value_counts()
        payment_pct = (payment_dist / payment_dist.sum() * 100).round(1)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        colors_gradient = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(payment_dist)))
        bars = ax.barh(range(len(payment_dist)), payment_dist.values, 
                      color=colors_gradient, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax.set_yticks(range(len(payment_dist)))
        ax.set_yticklabels([x.upper() for x in payment_dist.index], fontsize=12, fontweight='bold')
        ax.set_xlabel('Jumlah Transaksi', fontsize=13, fontweight='bold')
        ax.set_title('Distribusi Metode Pembayaran\n(Berdasarkan Jumlah Transaksi)', 
                    fontsize=15, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (method, count) in enumerate(payment_dist.items()):
            pct = payment_pct.iloc[i]
            ax.text(count, i, f'  {count:,} ({pct}%)', 
                   va='center', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Nilai Transaksi per Metode
        st.subheader("💰 Rata-rata Nilai Transaksi per Metode Pembayaran")
        
        payment_analysis = df.groupby('payment_type').agg({
            'payment_value': ['sum', 'mean', 'median', 'count']
        }).round(2)
        payment_analysis.columns = ['total_value', 'avg_value', 'median_value', 'total_transactions']
        payment_analysis = payment_analysis.sort_values('avg_value', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        payment_avg = payment_analysis.sort_values('avg_value', ascending=False)
        colors_bar = plt.cm.viridis(np.linspace(0.2, 0.8, len(payment_avg)))
        bars = ax.barh(range(len(payment_avg)), payment_avg['avg_value'], 
                      color=colors_bar, edgecolor='black', linewidth=1.2)
        ax.set_yticks(range(len(payment_avg)))
        ax.set_yticklabels([x.upper() for x in payment_avg.index], fontsize=11, fontweight='bold')
        ax.set_xlabel('Nilai Transaksi Rata-rata (R$)', fontsize=13, fontweight='bold')
        ax.set_title('Rata-rata Nilai Transaksi per Metode Pembayaran\n(Semakin Tinggi = Nilai Pembelian Lebih Besar)', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (idx, value) in enumerate(payment_avg['avg_value'].items()):
            ax.text(value, i, f'  R$ {value:,.2f}', 
                   va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Footer
    st.markdown("---")
    st.markdown(" **E-Commerce Analytics Dashboard** | Data Analysis Project")
    
except FileNotFoundError:
    st.error(" File main_data.csv tidak ditemukan!")
    st.info(" Pastikan file main_data.csv ada di folder yang sama dengan dashboard.py")
except Exception as e:
    st.error(f" Terjadi kesalahan: {str(e)}")
    st.info(" Silakan periksa format data dan coba lagi")
