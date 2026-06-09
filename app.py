import streamlit as st
import pandas as pd
import re
import base64

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def parse_angka(teks):
    return int(re.sub(r'\D', '', teks)) if teks else 0

# 1. Konfigurasi Halaman (Harus di baris paling atas)
st.set_page_config(layout="wide")

# 2. Fungsi untuk memuat logo dari folder lokal
def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

#Menampilkan Logo WeddMate
try:
    logo_base64 = get_image_base64("WeddMate LOGO.png")
    st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 10px 0px 20px 0px;">
            <img src="data:image/png;base64,{logo_base64}" width="180" style="margin-right: -40px;">
            <div style="font-family: 'Playfair Display', serif; font-size: 30px; color: #6D3528; font-weight:600; letter-spacing: 0.5px; font-style:italic,">
                WeddMate
            </div>
        </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.error("File 'WeddMate LOGO.png' tidak ditemukan.")

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Rekomendasi WO - Rafel", layout="wide")

# CSS
st.markdown(f"""
    <style>
        /* Impor Font: Great Vibes (Signature) & Crimson Pro */
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Great+Vibes&display=swap');

        /* 1. Menghilangkan Sidebar */
        [data-testid="stSidebar"] {{ 
            display: none !important; 
        }}
        
        /* 2. Backdrop Utama Aplikasi - GAMBAR DIHAPUS */
        .stApp {{
            background-color: #F7E4D3 !important; /* Murni warna krem pastel tanpa bayangan gambar */
            font-family: 'Crimson Pro', serif !important;
        }}
        
        /* Gaya Judul Signature (Plan Your Dream Wedding) - Tetap Bold Alami */
        .wedding-title {{
            font-family: 'Great Vibes', cursive !important;
            font-size: 80px !important; 
            font-weight: 400 !important;
            color: #6D3528 !important; 
            line-height: 1.1 !important;
            margin-bottom: 5px !important;
        }}
        
        /* Gaya Sub-Judul (Sistem Rekomendasi...) - Tanpa Bold */
        .wedding-subtitle {{
            font-family: 'Crimson Pro', serif !important;
            font-size: 20px !important;
            font-style: italic !important; 
            font-weight: 400 !important; /* Regular/Tidak Bold */
            color: #6D3528 !important;
            letter-spacing: 0.5px !important;
            margin-top: 0px !important;
        }}

        /* 3. Kustomisasi Semua Label (Budget Maksimal, Jumlah Tamu, dll) - TIDAK BOLD */
        label[data-testid="stWidgetLabel"] p, .stRadio p {{
            font-family: 'Crimson Pro', serif !important;
            color: #6D3528 !important; 
            font-style: italic !important; 
            font-weight: 400 !important; 
            font-size: 18px !important;
        }}
        
        /* 4. Kolom Input & Dropdown - DIUBAH JADI TIDAK BOLD */
        div[data-baseweb="select"], div[data-baseweb="input"], .stNumberInput input {{
            background-color: #FFFFFF !important;
            border: none !important; 
            border-radius: 6px !important;
            color: #6D3528 !important; 
            font-family: 'Crimson Pro', serif !important;
            font-size: 16px !important;
            font-weight: 400 !important; /* Menggunakan bobot regular agar tulisan inputan tipis elegan */
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }}
        
        /* 5. Custom Teks Radio Button - DIUBAH JADI TIDAK BOLD */
        div[data-testid="stMarkdownContainer"] p {{
            font-family: 'Crimson Pro', serif !important;
            color: #6D3528 !important;
            font-weight: 400 !important; /* Memastikan teks pilihan radio tidak tebal */
        }}
        
        /* 6. Mengatur Gaya Tab Navigasi Atas */
        .stTabs [data-baseweb="tab-list"] {{ 
            gap: 24px; 
            border-bottom: 1px solid #FCD1C6; 
            background-color: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{ 
            font-family: 'Crimson Pro', serif !important;
            font-weight: 400 !important; /* Tab tidak bold */
            font-size: 16px;
            color: #AF675B;
        }}
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            color: #6D3528 !important; 
            font-weight: 600 !important; /* Hanya tab aktif yang sedikit tegas agar user tahu posisi tab */
            border-bottom-color: #6D3528 !important;
        }}
        
        /* 7. Menghilangkan Box Kontainer Tebal (Seamless) */
        div[data-testid="stDataframeCard"], div.stElementContainer div[data-is-border="true"] {{
            border: none !important; 
            background-color: transparent !important; 
            box-shadow: none !important;
            padding: 10px 0px !important;
        }}
        /* 6. FORCE FIX: CHECKBOX & FONT CRIMSON PRO */
        div[data-testid="stCheckbox"] [role="checkbox"] {{
            border-color: #6D3528 !important; /* Warna garis tepi (border) kotak saat belum dicentang */
        }}
        div[data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] div {{
            background-color: #6D3528 !important; /* Warna latar belakang kotak saat dicentang (Mauve) */
            border-color: #6D3528 !important;     /* Warna border kotak saat dicentang */
        }}
        div[data-testid="stCheckbox"] [role="checkbox"][aria-checked="true"] svg {{
            color: #FFFFFF !important;             /* Warna ikon tanda centang (✓) di dalam kotak */
        }}
        
        /* KAPSUL MULTISELECT & FONT CRIMSON PRO */
        div[data-baseweb="tag"], span[data-baseweb="tag"], .stMultiSelect span[data-baseweb="tag"] {{
            background-color: #FCD1C6 !important; /* Warna latar belakang kapsul (Blush Lembut, bukan merah) */
            border: 1px solid #AF675B !important; /* Warna garis tepi (border) kapsul (Dusty Rose) */
            border-radius: 4px !important;
        }}

        /* Mengubah warna tulisan fasilitas di dalam border (Bridal, Catering, Groom Suit, dll) */
        div[data-baseweb="tag"] span, span[data-baseweb="tag"] span, .stMultiSelect span[data-baseweb="tag"] span {{
            color: #6D3528 !important;            /* Warna teks pilihan menjadi Mauve (tidak merah) */
            font-family: 'Crimson Pro', serif !important; /* Memaksa font menggunakan Crimson Pro */
            font-weight: 400 !important;          /* Bobot font regular (tidak bold) */
            font-size: 15px !important;
        }}

        /* Mengubah warna tombol silang (x) penghapus pilihan di dalam kapsul */
        div[data-baseweb="tag"] button, span[data-baseweb="tag"] button, div[data-baseweb="tag"] svg, span[data-baseweb="tag"] svg {{
            color: #6D3528 !important;            /* Warna tombol (x) mengikuti teks Mauve */
            fill: #6D3528 !important;             /* Memastikan warna ikon (x) terisi penuh */
        }}
        
        /* =====================================================================
        🎯 BAGIAN KODE: TOMBOL UTAMA "CARI REKOMENDASI" MENJADI WARNA PUTIH
        ===================================================================== */
        div.stButton > button[kind="primary"] {{
            background-color: #FFFFFF !important; /* Mengubah total warna tombol menjadi putih bersih */
            border: 1px solid #FCD1C6 !important; /* Garis tepi tipis warna Blush agar tombol tidak mati */
            color: #6D3528 !important;            /* Mengubah warna teks di dalam tombol menjadi Mauve (Crimson Pro) */
            font-family: 'Crimson Pro', serif !important; /* Memastikan font tombol menggunakan Crimson Pro */
            font-weight: 500 !important;          /* Ketebalan teks sedang (Medium) agar rapi */
            font-size: 18px !important;           /* Ukuran teks seimbang */
            border-radius: 6px !important;         /* Lengkungan sudut tombol yang halus */
            padding: 12px 30px !important;
            transition: all 0.3s ease;            /* Efek transisi halus saat disentuh kursor */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important; /* Bayangan tipis yang elegan */
        }}

        /* Efek saat kursor diletakkan di atas tombol (Hover) */
        div.stButton > button[kind="primary"]:hover {{
            background-color: #FCD1C6 !important; /* Berubah menjadi Blush lembut saat di-hover */
            color: #6D3528 !important;            /* Teks tetap berwarna Mauve */
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08) !important; /* Bayangan sedikit menebal */
        }}

        /* Kustomisasi Tabel */
        .stTable table {{
            font-family: 'Crimson Pro', serif !important;
        }}
        .stTable table thead tr th {{
            background-color: #6D3528 !important;
            color: #F7E4D3 !important;
            font-weight: 500 !important; /* Header tabel disesuaikan */
        }}
        .stTable table tbody tr td {{
            font-weight: 400 !important; /* Isi data tabel regular */
        }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # 1. Load Data Vendor
        df_v = pd.read_excel("Data Skripsi Rafel BrideStory.xlsx")
        df_v.columns = df_v.columns.str.strip()
        df_v['Nama Vendor'] = df_v['Nama Vendor'].ffill()
        
        df_v['Price'] = pd.to_numeric(df_v['Price'], errors='coerce').fillna(0)
        df_v['Pax'] = pd.to_numeric(df_v['Pax'], errors='coerce').fillna(0)
        df_v['Number Review'] = pd.to_numeric(df_v['Number Review'], errors='coerce').fillna(0)

        # 2. Load Data Sentimen
        df_s = pd.read_excel("Hasil_Sentimen_Final.xlsx")
        sentimen_stats = df_s.groupby('Vendor')['Sentimen'].apply(
            lambda x: (x == 'Positif').sum() / len(x) if len(x) > 0 else 0.5
        ).reset_index()
        sentimen_stats.columns = ['Nama Vendor', 'Skor_Sentimen']

        # 3. Gabungkan Data
        df_final = pd.merge(df_v, sentimen_stats, on='Nama Vendor', how='left')
        df_final['Skor_Sentimen'] = df_final['Skor_Sentimen'].fillna(0.5)
        
        return df_final, df_s
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Load Data
df_merged, df_raw_sentimen = load_data()

# NAVIGASI TAB
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Cari Rekomendasi", "📊 Dashboard Analisis", "📈 System Metrics", "ℹ️ About"])


# TAB 1: CARI REKOMENDASI
with tab1:
    # 100% MATCH HEADER TEXT STYLE
    st.markdown("""
        <div style='text-align: center; padding-top: 25px; padding-bottom: 25px;'>
            <div class='wedding-title'>Plan Your Dream Wedding</div>
            <div class='wedding-subtitle'>Sistem Rekomendasi Vendor Wedding Organizer</div>
        </div>
        <br>
    """, unsafe_allow_html=True)

    # INPUT SECTION
    with st.container(border=True):
        st.write(" ") 
        col1, col2 = st.columns(2, gap="large")
        with col1:
            budget = st.number_input("Budget Maksimal", min_value=0, step=1000000, value=0, format="%d", key="tab1_budget")
            # Mengubah teks terbilang ke warna hijau sage gelap agar kontras dan terbaca jelas di background krem
            st.markdown(f"<p style='color: #2E6F40; font-weight: bold;'>Terbilang: {format_rupiah(budget)}</p>", unsafe_allow_html=True)

        with col2:
            pax_options = ["<100 pax", "200 pax", "300 pax", "400 pax", "500 pax", "800 pax", ">=1000 pax", "Lainnya"]
            pax_choice = st.selectbox("Jumlah Tamu (pax)", options=pax_options, key="tab1_pax")
            if pax_choice == "Lainnya":
                pax_req = st.number_input("Masukkan jumlah tamu spesifik", min_value=1, value=100)
            else:
                angka_pax = re.findall(r'\d+', pax_choice)
                pax_req = int(angka_pax[0]) if angka_pax else 100

        st.write(" ") 
        col3, col4 = st.columns(2, gap="large")
        with col3:
            kota = st.selectbox("Lokasi Acara", options=df_merged['Lokasi'].dropna().unique() if not df_merged.empty else ["Data Tidak Tersedia"])
        
        with col4:
            st.write("Prioritas Utama:")
            prioritas = st.radio("Pilih satu:", ["Hemat Budget", "Kualitas Terbaik", "Ulasan Terbanyak"], horizontal=True, label_visibility="collapsed")

        st.write(" ") 
        st.write("Fasilitas Wajib yang Harus Tersedia:")
        list_fasilitas = ["Wedding Planner", "Wedding Organizer", "Catering", "Dekorasi", "Bridal", "Groom Suit", "Make Up", "Cake", "Entertainment", "Wedding Car", "Hand Bouquet", "Documentation"]
        
        select_all = st.checkbox("Pilih Semua Fasilitas")
        if select_all:
            selected_fasilitas = st.multiselect("Pilih Fasilitas:", options=list_fasilitas, default=list_fasilitas, label_visibility="collapsed")
        else:
            selected_fasilitas = st.multiselect("Pilih Fasilitas:", options=list_fasilitas, label_visibility="collapsed")
        
        st.write(" ") 
        cari_btn = st.button("🚀 Cari Rekomendasi Terbaik untuk Weddingmu Sekarang", use_container_width=True, type="primary")

# LOGIKA FILTERING (TAB1)
    if cari_btn:
        if budget <= 0:
            st.warning("Silakan Tentukan Budget Maksimal Anda.")
        else:
            # 1. Copy data
            df_proc = df_merged.copy()
            
            # 2. Filter Lokasi
            mask = (
                (df_proc['Lokasi'].astype(str).str.contains(kota, case=False, na=False)) | 
                (df_proc['Venue'].astype(str).str.contains(kota, case=False, na=False))
            )

            # 3. Filter harga & pax
            mask = mask & (df_proc['Price'] <= float(budget)) & (df_proc['Price'] > 0)
            
            if pax_choice == "<100 pax":
                mask = mask & (df_proc['Pax'] <= 200)
            elif pax_choice == ">=1000 pax":
                mask = mask & (df_proc['Pax'] >= 1000)
            elif pax_choice == "Lainnya":
                mask = mask & (df_proc['Pax'] >= float(pax_req))
            else:
                # Mengambil angka dari pilihan (misal 300 dari "300 pax")
                angka_pax_val = int(re.findall(r'\d+', pax_choice)[0])
                # Vendor harus punya kapasitas minimal sesuai input user
                mask = mask & (df_proc['Pax'] >= angka_pax_val)

            # 4. Filter fasilitas
            for f in selected_fasilitas:
            # Pastiin filter cek nilai 1 (integer) atau True (boolean)
                mask = mask & ((df_proc[f] == 1) | (df_proc[f] == True))
            # Filter akhir
            hasil = df_proc[mask].copy()

            # 5. (OUTPUT) IMPLEMENTASI WSM
            if not hasil.empty:
                st.success(f"✅ Ditemukan {len(hasil)} Vendor Terbaik untukmu!")
                
                # Normalisasi WSM
                max_p, min_p = hasil['Price'].max(), hasil['Price'].min()
                range_p = (max_p - min_p) if (max_p - min_p) > 0 else 1
                hasil['n_price'] = (max_p - hasil['Price']) / range_p 

                max_r, min_r = hasil['Number Review'].max(), hasil['Number Review'].min()
                range_r = (max_r - min_r) if (max_r - min_r) > 0 else 1
                hasil['n_review'] = (hasil['Number Review'] - min_r) / range_r

                # Skor Akhir
                if prioritas == "Hemat Budget":
                    hasil['Skor_Akhir'] = (hasil['n_price'] * 0.7) + (hasil['Skor_Sentimen'] * 0.2) + (hasil['n_review'] * 0.1)
                elif prioritas == "Kualitas Terbaik":
                    hasil['Skor_Akhir'] = (hasil['Skor_Sentimen'] * 0.7) + (hasil['n_price'] * 0.2) + (hasil['n_review'] * 0.1)
                else:
                    hasil['Skor_Akhir'] = (hasil['n_review'] * 0.7) + (hasil['Skor_Sentimen'] * 0.2) + (hasil['n_price'] * 0.1)

                rekomendasi = hasil.sort_values('Skor_Akhir', ascending=False).reset_index(drop=True)
                rekomendasi.index += 1

                # Looping Card (OUTPUT)
                for rank, row in rekomendasi.iterrows():
                    if rank == 1: medal, badge_text, color = "🥇", "BEST MATCH", "#FFD700"
                    elif rank == 2: medal, badge_text, color = "🥈", "RECOMMENDED", "#C0C0C0"
                    else: medal, badge_text, color = "🥉", f"RANK {rank}", "#E0E0E0"

                    with st.container(border=True):
                        # CARD INTERFACE
                        h1, h2 = st.columns([3, 1])
                        h1.markdown(f"{medal} {row['Nama Vendor']}")
                        h2.markdown(f"<div style='text-align:right;'><span style='background-color:{color}; padding:5px 12px; border-radius:15px; font-weight:bold; color:black; font-size:12px;'>{badge_text}</span></div>", unsafe_allow_html=True)
                        
                        col_info, col_action = st.columns([3, 1.5])
                        with col_info:
                            # Menyelaraskan teks warna harga menjadi Rose Gold agar senada dengan UI Baru
                            st.markdown(f"💰 Harga: <span style='color:#B85C5C; font-weight:bold; font-size:18px;'>{format_rupiah(row['Price'])}</span>", unsafe_allow_html=True)
                            st.markdown(f"👥 Kapasitas: {int(row['Pax'])} Pax")
                            venue_info = row['Venue'] if pd.notnull(row.get('Venue')) else row['Lokasi']
                            st.markdown(f"📍 Venue: {venue_info}")
                            
                            st.write("") # Memberikan nafas jarak vertikal tipis sebelum tag fasilitas
                            tersedia = [f for f in list_fasilitas if row.get(f) == True]
                            if tersedia:
                                # Mengubah gaya kapsul tag agar memiliki background pink pastel lembut dengan border krem tipis yang mewah
                                tags = "".join([f'<span style="background-color: #FDF6F6; padding: 4px 10px; margin: 4px; border-radius: 6px; font-size: 12px; border: 1px solid #EAE0DA; display: inline-block; color: #B85C5C; font-weight:500;">{f}</span>' for f in tersedia])
                                st.markdown(f"Fasilitas:<br>{tags}", unsafe_allow_html=True)
                            else:
                                st.markdown("Fasilitas: -")

                        with col_action:
                            st.write("Presentase Kepuasan")
                            sentimen_persen = row['Skor_Sentimen'] * 100
                            st.markdown(f"<h2 style='margin:0; color:#28A745;'>{sentimen_persen:.1f}%</h2><p style='font-size:12px; color:gray;'>Ulasan Positif</p>", unsafe_allow_html=True)
                            st.progress(float(row['Skor_Sentimen']))
                            url_final = row['URL'] if pd.notnull(row['URL']) else "https://www.bridestory.com"
                            st.link_button("Detail Bridestory", url_final, use_container_width=True)
            else:
                st.error("Maaf, tidak ada vendor yang sesuai dengan kriteria tersebut.")


# TAB 2: DASHBOARD SENTIMEN
with tab2:
    st.title("📊 Dashboard Analisis Sentimen")
    
    if not df_raw_sentimen.empty:
        total_vendor = df_merged['Nama Vendor'].nunique()
        total_ulasan = len(df_raw_sentimen)
        avg_positif = (df_raw_sentimen['Sentimen'] == 'Positif').mean() * 100

        # KPI Cards
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.info("🏷️Total Vendor")
            st.subheader(f"{total_vendor} Vendor")
        with kpi2:
            st.success("💬 Total Ulasan")
            st.subheader(f"{total_ulasan:,}".replace(",", "."))
        with kpi3:
            st.warning("✅ Rata-rata Positif")
            st.subheader(f"{avg_positif:.1f}%")

        st.divider()

        # Grid Analysis
        st.write("🏢 Daftar Analisis per Vendor")
        stats_per_vendor = df_raw_sentimen.groupby('Vendor')['Sentimen'].value_counts(normalize=True).unstack(fill_value=0)
        vendor_list = stats_per_vendor.index.tolist()

        for i in range(0, len(vendor_list), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(vendor_list):
                    v_name = vendor_list[i + j]
                    with cols[j]:
                        with st.container(border=True):
                            p_pos = stats_per_vendor.loc[v_name, 'Positif'] * 100 if 'Positif' in stats_per_vendor.columns else 0
                            c1, c2 = st.columns([2, 1])
                            c1.markdown(f"{v_name}")
                            c2.markdown(f"{p_pos:.1f}% Positif")
                            st.progress(p_pos / 100)
                            
                            p_count = (df_raw_sentimen[df_raw_sentimen['Vendor'] == v_name]['Sentimen'] == 'Positif').sum()
                            n_count = (df_raw_sentimen[df_raw_sentimen['Vendor'] == v_name]['Sentimen'] == 'Negatif').sum()
                            st.markdown(f"🟢 {p_count} positif  |  🔴 {n_count} negatif")
    else:
        st.info("Data sentimen belum tersedia.")


# TAB 3: SYSTEM METRICS
with tab3:
    st.markdown("📄 System Metrics & Technical Logs")
    st.caption("Spesifikasi arsitektur model, parameter hyper-tuning, dan log evaluasi klasifikasi.")

    with st.container(border=True):
        st.markdown("📉 Laporan Klasifikasi (Classification Report)")
        st.caption("Diuji dengan populasi testing sebesar 50 sampel (Manual Ground Truth)")
        
        col_metrics, col_cm = st.columns([1, 1])
        
        with col_metrics:
            st.write("ACCURACY")
            st.progress(0.58, text="58.00%")
            st.write("PRECISION")
            st.progress(0.58, text="58.12%")
            st.write("RECALL")
            st.progress(0.57, text="57.80%")
            st.write("F1-SCORE")
            st.progress(0.57, text="57.50%")

        with col_cm:
            st.write("CONFUSION MATRIX")
            cm_data = {
                "Prediksi: Negatif": ["16 (True Neg)", "10 (False Neg)"],
                "Prediksi: Positif": ["7 (False Pos)", "17 (True Pos)"]
            }
            cm_df = pd.DataFrame(cm_data, index=["Actual: Negatif", "Actual: Positif"])
            st.table(cm_df)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("⚙️ Konfigurasi Algoritma")
            st.write("Model: IndoBERT Base")
            st.code("Optimizer: AdamW\nLearning Rate: 2e-5\nEpochs: 3\nBatch Size: 16", language="text")
    with c2:
        with st.container(border=True):
            st.markdown("📊 Spesifikasi Dataset Induk")
            st.write("Total Data: 1.380 Ulasan")
            st.write("Metode Rekomendasi: Weighted Sum Model (WSM)")

    st.divider()
    st.write("📈 Visualisasi Distribusi Sentimen (1.380 Data)")
    if not df_merged.empty:
        def get_label(x):
            if x > 0.6: return "Positif"
            elif x < 0.4: return "Negatif"
            else: return "Netral"
        dist_data = df_merged['Skor_Sentimen'].apply(get_label).value_counts()
        st.bar_chart(dist_data, color="#0083B8")

# TAB 4: ABOUT SYSTEM
with tab4:
    st.markdown("ℹ️ Tentang Sistem Rekomendasi")
    
    col_desc, col_dev = st.columns([2, 1])
    
    with col_desc:
        with st.container(border=True):
            st.markdown("📝 Deskripsi Program")
            st.write("""
            Sistem ini dirancang untuk membantu calon pengantin dalam menemukan Vendor Wedding Organizer (WO) terbaik 
            yang sesuai dengan kriteria budget, kapasitas tamu (pax), lokasi, serta kebutuhan fasilitas tertentu.
            
            Fitur Utama:
            - Filtering Cerdas: Menyaring data vendor berdasarkan input spesifik pengguna.
            - Analisis Sentimen: Mengintegrasikan ulasan asli dari platform Bridestory menggunakan model **IndoBERT** untuk mengetahui tingkat kepuasan pelanggan secara otomatis.
            - Metode WSM (Weighted Sum Model): Melakukan perankingan vendor secara objektif berdasarkan bobot prioritas (Budget, Kualitas/Sentimen, atau Popularitas).
            """)
            
            st.markdown("⚖️ Kelebihan & Kekurangan")
            col_plus, col_minus = st.columns(2)
            with col_plus:
                st.success("Kelebihan:\n- Rekomendasi berbasis data asli.\n- Objektif (menggunakan perhitungan matematika WSM).\n- Visualisasi sentimen yang mudah dipahami.")
            with col_minus:
                st.warning("Kekurangan:\n- Terbatas pada data vendor yang tersedia di dataset.\n- Hasil klasifikasi sentimen sangat bergantung pada kualitas teks ulasan.")

    with col_dev:
        with st.container(border=True):
            st.markdown("🎓 Profil Pengembang")
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
            st.markdown("Nama: Rafel")
            st.markdown("Program Studi: Teknik Informatika")
            st.markdown("Judul Skripsi: Sistem Rekomendasi Vendor Wedding Organizer Berbasis Web Menggunakan Metode Weighted Sum Model (WSM) dan Analisis Sentimen (IndoBERT)")
            st.divider()
