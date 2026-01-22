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
    h1 {
        color: #0e1117;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data dengan caching
@st.cache_data
def load_data():
    try:
        # Coba beberapa path untuk support local dan deployment
        possible_paths = [
            os.path.dirname(os.path.abspath(__file__)),  # Same directory as app.py
            os.getcwd(),  # Current working directory
            '.',  # Relative current directory
        ]
        
        csv_files = [
            'orders_df.csv', 'order_items_df.csv', 'order_payments_df.csv',
            'products_df.csv', 'category_names_df.csv', 'reviews_df.csv', 'customers_df.csv'
        ]
        
        # Find the correct path
        data_path = None
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'orders_df.csv')):
                data_path = path
                break
        
        if data_path is None:
            raise FileNotFoundError("CSV files tidak ditemukan. Pastikan file CSV ada di folder yang sama dengan app.py")
        
        # Load semua file CSV
        orders_df = pd.read_csv(os.path.join(data_path, 'orders_df.csv'))
        order_items_df = pd.read_csv(os.path.join(data_path, 'order_items_df.csv'))
        order_payments_df = pd.read_csv(os.path.join(data_path, 'order_payments_df.csv'))
        products_df = pd.read_csv(os.path.join(data_path, 'products_df.csv'))
        category_names_df = pd.read_csv(os.path.join(data_path, 'category_names_df.csv'))
        reviews_df = pd.read_csv(os.path.join(data_path, 'reviews_df.csv'))
        customers_df = pd.read_csv(os.path.join(data_path, 'customers_df.csv'))
        
        # Convert datetime columns untuk orders_df
        datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                         'order_delivered_carrier_date', 'order_delivered_customer_date',
                         'order_estimated_delivery_date']
        for col in datetime_cols:
            if col in orders_df.columns:
                orders_df[col] = pd.to_datetime(orders_df[col], errors='coerce')
        
        return orders_df, order_items_df, order_payments_df, products_df, category_names_df, reviews_df, customers_df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info(f"📂 Current working directory: {os.getcwd()}")
        st.info(f"📂 Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        return None, None, None, None, None, None, None

# Load data
orders_df, order_items_df, order_payments_df, products_df, category_names_df, reviews_df, customers_df = load_data()

if orders_df is not None:
    
    # Header
    st.title("🛒 E-Commerce Analytics Dashboard")
    st.markdown("**Analisis Data E-Commerce**")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📊 Menu Navigasi")
    st.sidebar.markdown("Pilih analisis yang ingin ditampilkan:")
    
    menu = st.sidebar.radio(
        "Pilih Pertanyaan Bisnis:",
        ["🏠 Overview", 
         "📈 Q1: Tren Penjualan", 
         "📦 Q2: Kategori Produk", 
         "⭐ Q3: Kepuasan Pelanggan", 
         "💳 Q4: Metode Pembayaran"]
    )
    
    # ===========================
    # FITUR INTERAKTIF - FILTERS
    # ===========================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filter Data")
    
    # Filter tanggal
    with st.sidebar.expander("📅 **Periode Transaksi**", expanded=True):
        min_date = orders_df['order_purchase_timestamp'].min().date()
        max_date = orders_df['order_purchase_timestamp'].max().date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Dari:",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="start_date"
            )
        with col2:
            end_date = st.date_input(
                "Sampai:",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="end_date"
            )
        
        if start_date > end_date:
            st.error("⚠️ Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
            start_date = min_date
            end_date = max_date
        
        st.caption(f"📊 **{(end_date - start_date).days}** hari dipilih")
    
    # Filter kategori dengan pilihan yang lebih simple
    with st.sidebar.expander("📦 **Kategori Produk**", expanded=False):
        products_with_category = products_df.merge(category_names_df, on='product_category_name', how='left')
        all_categories = sorted(products_with_category['product_category_name_english'].dropna().unique().tolist())
        
        filter_category_option = st.radio(
            "Mode filter:",
            ["Semua Kategori", "Pilih Kategori Tertentu"],
            horizontal=True,
            key="category_radio",
            help="Semua Kategori = menampilkan semua data tanpa filter"
        )
        
        if filter_category_option == "Semua Kategori":
            selected_categories = all_categories
            st.success(f"✅ Menampilkan **SEMUA {len(all_categories)}** kategori (tidak ada filter)")
        else:
            # Search box untuk filter kategori
            search_cat = st.text_input("🔍 Cari kategori:", placeholder="Ketik nama kategori...")
            
            if search_cat:
                filtered_cats = [cat for cat in all_categories if search_cat.lower() in cat.lower()]
            else:
                filtered_cats = all_categories[:20]  # Show top 20 by default
            
            selected_categories = st.multiselect(
                "Pilih kategori:",
                options=all_categories,
                default=filtered_cats[:5] if not search_cat else filtered_cats,
                help="Gunakan search box untuk menemukan kategori",
                max_selections=10
            )
            
            if len(selected_categories) == 0:
                st.warning("⚠️ Minimal pilih 1 kategori")
                selected_categories = all_categories[:5]
            else:
                st.warning(f"⚠️ FILTER AKTIF: **{len(selected_categories)}/{len(all_categories)}** kategori dipilih")
    
    # Filter provinsi dengan pilihan yang lebih simple
    with st.sidebar.expander("🗺️ **Provinsi Pelanggan**", expanded=False):
        all_states = sorted(customers_df['customer_state'].dropna().unique().tolist())
        
        filter_state_option = st.radio(
            "Mode filter:",
            ["Semua Provinsi", "Pilih Provinsi Tertentu"],
            horizontal=True,
            key="state_radio",
            help="Semua Provinsi = menampilkan semua data tanpa filter"
        )
        
        if filter_state_option == "Semua Provinsi":
            selected_states = all_states
            st.success(f"✅ Menampilkan **SEMUA {len(all_states)}** provinsi (tidak ada filter)")
        else:
            # Top N states atau custom selection
            filter_method = st.selectbox(
                "Pilih metode:",
                ["Top 10 Provinsi Terbanyak", "Pilih Manual"]
            )
            
            if filter_method == "Top 10 Provinsi Terbanyak":
                # Get top 10 states by order count
                state_counts = orders_df.merge(customers_df[['customer_id', 'customer_state']], on='customer_id')
                top_states = state_counts['customer_state'].value_counts().head(10).index.tolist()
                selected_states = st.multiselect(
                    "Top 10 provinsi:",
                    options=top_states,
                    default=top_states,
                    help="Provinsi dengan jumlah order terbanyak"
                )
            else:
                selected_states = st.multiselect(
                    "Pilih provinsi:",
                    options=all_states,
                    default=all_states[:5],
                    help="Pilih provinsi secara manual",
                    max_selections=15
                )
            
            if len(selected_states) == 0:
                st.warning("⚠️ Minimal pilih 1 provinsi")
                selected_states = all_states[:5]
            else:
                st.warning(f"⚠️ FILTER AKTIF: **{len(selected_states)}/{len(all_states)}** provinsi dipilih")
    
    # Filter metode pembayaran
    with st.sidebar.expander("💳 **Metode Pembayaran**", expanded=False):
        all_payment_methods = sorted(order_payments_df['payment_type'].dropna().unique().tolist())
        
        filter_payment_option = st.radio(
            "Mode filter:",
            ["Semua Metode", "Pilih Metode Tertentu"],
            horizontal=True,
            key="payment_radio",
            help="Semua Metode = menampilkan semua data tanpa filter"
        )
        
        if filter_payment_option == "Semua Metode":
            selected_payment_methods = all_payment_methods
            st.success(f"✅ Menampilkan **SEMUA {len(all_payment_methods)}** metode pembayaran (tidak ada filter)")
        else:
            selected_payment_methods = st.multiselect(
                "Pilih metode pembayaran:",
                options=all_payment_methods,
                default=all_payment_methods,
                help="Pilih satu atau lebih metode pembayaran"
            )
            
            if len(selected_payment_methods) == 0:
                st.warning("⚠️ Minimal pilih 1 metode pembayaran")
                selected_payment_methods = all_payment_methods
            else:
                st.warning(f"⚠️ FILTER AKTIF: **{len(selected_payment_methods)}/{len(all_payment_methods)}** metode dipilih")
    
    # Apply filters
    filtered_orders = orders_df[
        (orders_df['order_purchase_timestamp'].dt.date >= start_date) &
        (orders_df['order_purchase_timestamp'].dt.date <= end_date)
    ].copy()
    
    # Filter by customer state - HANYA jika bukan semua provinsi
    if selected_states and len(selected_states) < len(all_states):
        filtered_customers = customers_df[customers_df['customer_state'].isin(selected_states)]
        filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(filtered_customers['customer_id'])]
    
    # Get filtered order IDs
    filtered_order_ids = filtered_orders['order_id'].unique()
    
    # Apply to other dataframes
    filtered_order_items = order_items_df[order_items_df['order_id'].isin(filtered_order_ids)].copy()
    filtered_order_payments = order_payments_df[order_payments_df['order_id'].isin(filtered_order_ids)].copy()
    filtered_reviews = reviews_df[reviews_df['order_id'].isin(filtered_order_ids)].copy()
    
    # Filter by payment method - HANYA jika bukan semua metode
    if selected_payment_methods and len(selected_payment_methods) < len(all_payment_methods):
        filtered_order_payments = filtered_order_payments[
            filtered_order_payments['payment_type'].isin(selected_payment_methods)
        ].copy()
        # Update filtered_order_ids based on payment filter
        payment_order_ids = filtered_order_payments['order_id'].unique()
        filtered_orders = filtered_orders[filtered_orders['order_id'].isin(payment_order_ids)].copy()
        filtered_order_items = filtered_order_items[filtered_order_items['order_id'].isin(payment_order_ids)].copy()
        filtered_reviews = filtered_reviews[filtered_reviews['order_id'].isin(payment_order_ids)].copy()
        filtered_order_ids = payment_order_ids
    
    # Filter by category - HANYA jika bukan semua kategori
    if selected_categories and len(selected_categories) < len(all_categories):
        products_with_category_filtered = products_with_category[
            products_with_category['product_category_name_english'].isin(selected_categories)
        ]
        filtered_product_ids = products_with_category_filtered['product_id'].unique()
        filtered_order_items = filtered_order_items[filtered_order_items['product_id'].isin(filtered_product_ids)].copy()
        
        # Update filtered_order_ids based on category filter
        filtered_order_ids = filtered_order_items['order_id'].unique()
        filtered_orders = filtered_orders[filtered_orders['order_id'].isin(filtered_order_ids)].copy()
        filtered_order_payments = filtered_order_payments[filtered_order_payments['order_id'].isin(filtered_order_ids)].copy()
        filtered_reviews = filtered_reviews[filtered_reviews['order_id'].isin(filtered_order_ids)].copy()
    
    # ===========================
    # HALAMAN OVERVIEW
    # ===========================
    if menu == "🏠 Overview":
        st.header("📊 Overview Bisnis E-Commerce")
        
        # Filter status indicator
        total_orders_full = orders_df['order_id'].nunique()
        total_orders_filtered = filtered_orders['order_id'].nunique()
        
        if total_orders_filtered < total_orders_full:
            filter_pct = (total_orders_filtered / total_orders_full * 100)
            st.warning(f"""
            ⚠️ **FILTER AKTIF**: Menampilkan **{total_orders_filtered:,}** dari **{total_orders_full:,}** total orders 
            ({filter_pct:.1f}% data) | Periode: **{start_date}** s/d **{end_date}**
            """)
        else:
            st.success(f"""
            ✅ **MENAMPILKAN SEMUA DATA**: **{total_orders_full:,}** total orders 
            | Periode: **{start_date}** s/d **{end_date}**
            """)
        
        st.markdown("---")
        
        # Key Metrics
        st.subheader("📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_orders = filtered_orders['order_id'].nunique()
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: #666; margin: 0; font-size: 16px;'>Total Orders</h3>
                    <h1 style='color: #1f77b4; margin: 10px 0; font-size: 36px; font-weight: bold;'>{total_orders:,}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_revenue = filtered_order_items['price'].sum()
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: #666; margin: 0; font-size: 16px;'> Total Revenue</h3>
                    <h1 style='color: #2ca02c; margin: 10px 0; font-size: 36px; font-weight: bold;'>R$ {total_revenue/1000000:.2f}M</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_rating = filtered_reviews['review_score'].mean() if len(filtered_reviews) > 0 else 0
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: #666; margin: 0; font-size: 16px;'> Avg Rating</h3>
                    <h1 style='color: #ff7f0e; margin: 10px 0; font-size: 36px; font-weight: bold;'>{avg_rating:.2f} / 5.0</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            products_in_filtered = products_df[products_df['product_id'].isin(filtered_order_items['product_id'])]
            total_categories = products_in_filtered['product_category_name'].nunique()
            st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h3 style='color: #666; margin: 0; font-size: 16px;'> Total Categories</h3>
                    <h1 style='color: #d62728; margin: 10px 0; font-size: 36px; font-weight: bold;'>{total_categories}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Top 5 Kategori Terlaris")
            # Merge untuk mendapatkan kategori
            products_with_category_show = products_df.merge(category_names_df, on='product_category_name', how='left')
            product_sales = filtered_order_items.merge(products_with_category_show[['product_id', 'product_category_name_english']], on='product_id', how='left')
            if len(product_sales) > 0:
                top_cat = product_sales['product_category_name_english'].value_counts().head(5).reset_index()
                top_cat.columns = ['Kategori', 'Jumlah Terjual']
                st.dataframe(top_cat, use_container_width=True, hide_index=True)
            else:
                st.info("Tidak ada data untuk filter yang dipilih")
        
        with col2:
            st.subheader(" Distribusi Rating")
            if len(filtered_reviews) > 0:
                rating_dist = filtered_reviews['review_score'].value_counts().sort_index()
                rating_pct = (rating_dist / rating_dist.sum() * 100).round(1)
                rating_df = pd.DataFrame({
                    'Rating': [f"{i} ⭐" for i in rating_dist.index],
                    'Jumlah': rating_dist.values,
                    'Persentase': [f"{p}%" for p in rating_pct.values]
                })
                st.dataframe(rating_df, use_container_width=True, hide_index=True)
            else:
                st.info("Tidak ada data untuk filter yang dipilih")
    
    # ===========================
    # Q1: TREN PENJUALAN
    # ===========================
    elif menu == "📈 Q1: Tren Penjualan":
        st.header(" Pertanyaan 1: Tren Penjualan dari Waktu ke Waktu")
        st.markdown("**Bagaimana tren penjualan e-commerce dari waktu ke waktu dan periode waktu mana yang memiliki volume transaksi tertinggi?**")
        st.markdown("---")
        
        if len(filtered_orders) == 0:
            st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.")
        else:
            # Prepare data
            filtered_orders['year_month'] = filtered_orders['order_purchase_timestamp'].dt.to_period('M')
            monthly_sales = filtered_orders.groupby('year_month').agg({
                'order_id': 'count'
            }).rename(columns={'order_id': 'total_orders'}).reset_index()
            monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
        
            # Visualisasi Tren Penjualan Bulanan
            st.subheader(" Tren Penjualan Bulanan E-Commerce")
            
            fig, ax = plt.subplots(figsize=(16, 7))
            ax.plot(range(len(monthly_sales)), monthly_sales['total_orders'], 
                    marker='o', linewidth=2.5, markersize=8, color='#2E86AB', markerfacecolor='#A23B72')
            ax.set_title('Tren Penjualan Bulanan E-Commerce', fontsize=18, fontweight='bold', pad=20)
            ax.set_xlabel('Periode (Bulan)', fontsize=14, fontweight='bold')
            ax.set_ylabel('Jumlah Pesanan', fontsize=14, fontweight='bold')
            ax.set_xticks(range(0, len(monthly_sales), max(1, len(monthly_sales)//10)))
            ax.set_xticklabels(monthly_sales['year_month'][::max(1, len(monthly_sales)//10)], rotation=45, ha='right', fontsize=11)
            ax.tick_params(axis='y', labelsize=11)
            
            # Highlight max
            max_idx = monthly_sales['total_orders'].idxmax()
            ax.annotate(f"{monthly_sales.loc[max_idx, 'total_orders']:,.0f} orders", 
                        xy=(max_idx, monthly_sales.loc[max_idx, 'total_orders']),
                        xytext=(10, 10), textcoords='offset points', fontsize=11,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Top 10 Bulan
            st.markdown("---")
            st.subheader(" Top 10 Bulan dengan Volume Transaksi Tertinggi")
            top_months = monthly_sales.sort_values('total_orders', ascending=False).head(10)
            top_months.columns = ['Periode', 'Total Orders']
            st.dataframe(top_months, use_container_width=True, hide_index=True)
            
            # Insight
            st.markdown("---")
            st.subheader("💡 Insight Utama")
            max_period = monthly_sales.loc[monthly_sales['total_orders'].idxmax(), 'year_month']
            st.info(f"""
            - **{max_period}** mencatat volume transaksi **tertinggi** dengan **{monthly_sales['total_orders'].max():,} pesanan**
            - Data menunjukkan tren penjualan berdasarkan filter yang dipilih
            - Gunakan filter tanggal untuk melihat tren periode tertentu
            """)
    
    # ===========================
    # Q2: KATEGORI PRODUK
    # ===========================
    elif menu == "📦 Q2: Kategori Produk":
        st.header(" Pertanyaan 2: Kategori Produk Terpopuler")
        st.markdown("**Kategori produk apa yang paling populer dan menghasilkan revenue tertinggi?**")
        st.markdown("---")
        
        if len(filtered_order_items) == 0:
            st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.")
        else:
            # Prepare data
            products_with_category_q2 = products_df.merge(category_names_df, on='product_category_name', how='left')
            product_sales = filtered_order_items.merge(
                products_with_category_q2[['product_id', 'product_category_name_english']], 
                on='product_id', how='left'
            )
            
            category_popularity = product_sales.groupby('product_category_name_english').agg({
                'order_id': 'count',
                'price': 'sum'
            }).rename(columns={'order_id': 'total_items_sold', 'price': 'total_revenue'}).sort_values('total_items_sold', ascending=False).reset_index()
            category_popularity['avg_price'] = category_popularity['total_revenue'] / category_popularity['total_items_sold']
            
            # Top 10 by Revenue
            st.subheader(" Top 10 Kategori Produk Terlaris (Berdasarkan Revenue)")
            
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
            st.markdown("---")
            st.subheader(" Top 10 Kategori Produk Terlaris (Berdasarkan Volume)")
            
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
            
            # Insight
            st.markdown("---")
            st.subheader("💡 Insight Utama")
            top1_rev = top_category_rev.iloc[0]
            top1_vol = top_category_vol.iloc[0]
            st.info(f"""
            - **{top1_rev['product_category_name_english']}** menghasilkan revenue tertinggi: **R$ {top1_rev['total_revenue']:,.0f}**
            - **{top1_vol['product_category_name_english']}** memiliki volume penjualan tertinggi: **{top1_vol['total_items_sold']:,.0f} items**
            - Top 3 kategori berkontribusi signifikan terhadap total revenue
            """)
    
        # ===========================
        # Q3: KEPUASAN PELANGGAN
        # ===========================
    elif menu == "⭐ Q3: Kepuasan Pelanggan":
            st.header(" Pertanyaan 3: Tingkat Kepuasan Pelanggan")
            st.markdown("**Bagaimana tingkat kepuasan pelanggan berdasarkan review score dan faktor apa yang mempengaruhinya?**")
            st.markdown("---")
            
            if len(filtered_reviews) == 0:
                st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.")
            else:
                # Distribusi Review Score
                st.subheader(" Distribusi Rating Kepuasan Pelanggan")
                
                review_dist = filtered_reviews['review_score'].value_counts().sort_index()
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
                st.markdown("---")
                st.subheader(" Pengaruh Waktu Pengiriman terhadap Rating")
                
                # Merge orders with reviews
                orders_reviews = filtered_orders.merge(filtered_reviews[['order_id', 'review_score']], on='order_id', how='inner')
                orders_reviews['delivery_time'] = (
                    orders_reviews['order_delivered_customer_date'] - orders_reviews['order_purchase_timestamp']
                ).dt.days
                
                delivery_by_score = orders_reviews.groupby('review_score')['delivery_time'].agg(['mean', 'median', 'count']).round(2)
                
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
                
                # Insight
                st.markdown("---")
                st.subheader("💡 Insight Utama")
                rating_5_pct = review_pct.loc[5] if 5 in review_pct.index else 0
                rating_45_pct = review_pct.loc[[4,5]].sum() if 4 in review_pct.index and 5 in review_pct.index else 0
                delivery_1 = delivery_means[0] if len(delivery_means) > 0 else 0
                delivery_5 = delivery_means[-1] if len(delivery_means) > 0 else 0
                st.info(f"""
                - **{rating_45_pct:.1f}%** pelanggan memberikan rating 4-5 bintang (sangat puas)
                - **{rating_5_pct:.1f}%** pelanggan memberikan rating 5 bintang
                - **Faktor Utama: Waktu Pengiriman**
                  - Rating 1 bintang: {delivery_1:.1f} hari
                  - Rating 5 bintang: {delivery_5:.1f} hari
                  - **Korelasi negatif kuat**: Semakin cepat pengiriman = semakin tinggi kepuasan
                """)
    
    # ===========================
    # Q4: METODE PEMBAYARAN
    # ===========================
    elif menu == "💳 Q4: Metode Pembayaran":
        st.header(" Pertanyaan 4: Metode Pembayaran dan Nilai Transaksi")
        st.markdown("**Metode pembayaran apa yang paling sering digunakan pelanggan dan bagaimana hubungannya dengan nilai transaksi?**")
        st.markdown("---")
        
        if len(filtered_order_payments) == 0:
            st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.")
        else:
            # Distribusi Metode Pembayaran
            st.subheader(" Distribusi Metode Pembayaran")
            
            payment_dist = filtered_order_payments['payment_type'].value_counts()
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
            st.markdown("---")
            st.subheader(" Rata-rata Nilai Transaksi per Metode Pembayaran")
            
            payment_analysis = filtered_order_payments.groupby('payment_type').agg({
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
            
            # Insight
            st.markdown("---")
            st.subheader("💡 Insight Utama")
            top_method = payment_dist.index[0]
            top_method_pct = payment_pct.iloc[0]
            top_value_method = payment_avg.index[0]
            top_avg_value = payment_avg['avg_value'].iloc[0]
            st.info(f"""
            - **{top_method.upper()}** mendominasi dengan **{top_method_pct}%** dari total transaksi
            - **{top_value_method.upper()}** memiliki average transaction value tertinggi: **R$ {top_avg_value:,.2f}**
            - Terdapat korelasi antara metode pembayaran dan ukuran transaksi
            - Gunakan filter untuk melihat tren pembayaran per periode atau kategori
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("**📊 E-Commerce Analytics Dashboard**")
    
else:
    st.error("❌ File CSV tidak ditemukan!")
    st.info("📁 Pastikan semua file CSV ada di folder dashboard/")
    st.markdown("""
    File yang diperlukan:
    - orders_df.csv
    - order_items_df.csv
    - order_payments_df.csv
    - products_df.csv
    - category_names_df.csv
    - reviews_df.csv
    - customers_df.csv
    """)
