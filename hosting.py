# import streamlit as st
# import pandas as pd
# import datetime
# from PIL import Image
# import plotly.express as px
# import plotly.graph_objects as go
# from sqlalchemy import create_engine, text
# import time
# import hashlib
# import io

# # ===================== PAGE CONFIG =====================
# st.set_page_config(page_title="Server Inventory Dashboard", layout="wide", initial_sidebar_state="collapsed")

# # ===================== CUSTOM CSS =====================
# st.markdown("""
# <style>
#     /* Hide sidebar completely */
#     [data-testid="stSidebar"] {
#         display: none;
#     }

#     /* Main container */
#     div.block-container {
#         padding-top: 1rem;
#     }

#     /* Header styling */
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }

#     .main-header h1 {
#         color: white;
#         text-align: center;
#         margin: 0;
#         font-size: 2.5rem;
#         font-weight: 700;
#     }

#     /* Metric cards */
#     div[data-testid="metric-container"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 10px;
#         padding: 15px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }

#     div[data-testid="metric-container"] label {
#         color: white !important;
#         font-weight: 600;
#     }

#     div[data-testid="metric-container"] [data-testid="stMetricValue"] {
#         color: white !important;
#         font-size: 2rem !important;
#     }

#     /* Buttons */
#     .stButton button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 10px 20px;
#         font-weight: 600;
#         transition: all 0.3s;
#     }

#     .stButton button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 12px rgba(0,0,0,0.2);
#     }

#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#         background-color: transparent;
#     }

#     .stTabs [data-baseweb="tab"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border-radius: 8px 8px 0 0;
#         padding: 10px 20px;
#         font-weight: 600;
#     }

#     .stTabs [aria-selected="true"] {
#         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
#     }

#     /* Dataframe */
#     .dataframe {
#         border-radius: 10px;
#         overflow: hidden;
#     }

#     /* Success/Error messages */
#     .stSuccess, .stError, .stInfo {
#         border-radius: 8px;
#     }

#     /* Login Box */
#     .login-container {
#         max-width: 450px;
#         margin: 80px auto;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 40px;
#         border-radius: 15px;
#         box-shadow: 0 8px 20px rgba(0,0,0,0.3);
#     }

#     .login-container h1 {
#         color: white;
#         text-align: center;
#         margin-bottom: 30px;
#     }

#     .scrollable-table {
#         max-height: 800px;
#         overflow-y: auto;
#         border: 1px solid #222;
#         border-radius: 8px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ===================== DATABASE CONNECTION =====================
# @st.cache_resource
# def get_db_engine():
#     DB_USER = "rajif"
#     DB_PASS = "123"
#     DB_HOST = "127.0.1.1"
#     DB_PORT = "5432"
#     DB_NAME = "rajifdb"
#     return create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# # ===================== SESSION STATE INITIALIZATION =====================
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'username' not in st.session_state:
#     st.session_state.username = None
# if 'upload_success' not in st.session_state:
#     st.session_state.upload_success = False

# # ===================== LOGIN FUNCTIONS =====================
# def hash_password(password):
#     """Hash password menggunakan SHA256"""
#     return hashlib.sha256(password.encode()).hexdigest()

# def verify_login(username, password):
#     """Verifikasi login dari tabel admin"""
#     engine = get_db_engine()
#     try:
#         with engine.connect() as conn:
#             query = text("""
#                 SELECT username, password
#                 FROM admin
#                 WHERE username = :username
#             """)
#             result = conn.execute(query, {"username": username}).fetchone()

#             if result:
#                 stored_password = result[1]
#                 if stored_password == hash_password(password) or stored_password == password:
#                     return True
#             return False
#     except Exception as e:
#         st.error(f"Error during login: {str(e)}")
#         return False

# def logout():
#     """Logout user"""
#     st.session_state.logged_in = False
#     st.session_state.username = None
#     st.rerun()

# # ===================== DATA FUNCTIONS =====================
# @st.cache_data(ttl=60)
# def load_data():
#     engine = get_db_engine()
#     query = """
#         SELECT project_name, hostname, site, rack, brand, status, role, device_type,
#                slot, chassis_tag, asset_tag, ip_idrac, ip_os, mac_1, mac_2, wwn_1, wwn_2,
#                core, cpu, kontrak_pengadaan, tahun_pengadaan
#         FROM mytable;
#     """
#     df = pd.read_sql(query, engine)

#     df_rename = df.rename(columns={
#         "hostname": "HOSTNAME",
#         "project_name": "PROJECT",
#         "site": "SITE",
#         "rack": "RACK",
#         "status": "STATUS",
#         "role": "ROLE",
#         "brand": "BRAND",
#         "device_type": "DEVICE_TYPE",
#         "slot": "SLOT",
#         "chassis_tag": "CHASSIS_TAG",
#         "asset_tag": "ASSET_TAG",
#         "ip_idrac": "IP_IDRAC",
#         "ip_os": "IP_OS",
#         "mac_1": "MAC_1",
#         "mac_2": "MAC_2",
#         "wwn_1": "WWN_1",
#         "wwn_2": "WWN_2",
#         "core": "CORE",
#         "cpu": "CPU",
#         "kontrak_pengadaan": "KONTRAK_PENGADAAN",
#         "tahun_pengadaan": "TAHUN_PENGADAAN"
#     })

#     df_rename["STATUS"] = df_rename["STATUS"].apply(lambda x: "Active" if x in [1, True] else "Inactive")
#     return df_rename

# # ===================== LOGIN PAGE =====================
# if not st.session_state.logged_in:
#     st.markdown("""
#         <div class="login-container">
#             <h1>🔐 Login</h1>
#         </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])

#     with col2:
#         username = st.text_input("👤 Username", key="login_username")
#         password = st.text_input("🔑 Password", type="password", key="login_password")

#         if st.button("🚀 Login", use_container_width=True):
#             if username and password:
#                 success = verify_login(username, password)
#                 if success:
#                     st.session_state.logged_in = True
#                     st.session_state.username = username
#                     st.success(f"Welcome, {username}!")
#                     time.sleep(1)
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid username or password")
#             else:
#                 st.warning("⚠️ Please enter username and password")

#     st.stop()

# # ===================== MAIN DASHBOARD =====================
# # Header with logout button
# col_header1, col_header2 = st.columns([4, 1])
# with col_header1:
#     st.markdown("""
#     <div class="main-header">
#         <h1>🖥️ Dashboard Inventory Server Management</h1>
#     </div>
#     """, unsafe_allow_html=True)
# with col_header2:
#     st.write("")
#     st.write(f"**Welcome, {st.session_state.username}** 👋")
#     if st.button("🚪 Logout", use_container_width=True):
#         logout()

# # ===================== LOAD DATA =====================
# df_rename = load_data()

# # ===================== METRICS =====================
# total = len(df_rename)
# active = len(df_rename[df_rename["STATUS"] == "Active"])
# inactive = total - active
# rack_usage = f"{df_rename['RACK'].nunique()}"

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("📊 Total Server", total)
# col2.metric("✅ Active", active)
# col3.metric("⚠️ Inactive", inactive)
# col4.metric("🏢 Total Racks", rack_usage)

# st.divider()

# # ===================== TABS =====================
# tab1, tab2, tab3 = st.tabs(["📋 Data View", "📤 Import Data", "📈 Analytics"])

# # ===================== TAB 1: DATA VIEW =====================
# with tab1:
#     st.subheader("🔎 Search & View Data")

#     # ===================== FILTER KOLOM =====================
#     all_columns = df_rename.columns.tolist()
#     selected_columns = st.multiselect(
#         "🧭 Select columns to display:",
#         options=all_columns,
#         default=all_columns,
#         help="Uncheck columns you want to hide from the table."
#     )

#     # ===================== SEARCH & DOWNLOAD =====================
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         search = st.text_input(
#             "🔍 Search by Hostname / IP iDRAC / Asset Tag:",
#             placeholder="Type to search..."
#         )
#     with col2:
#         st.write("")
#         st.write("")
#         csv = df_rename[selected_columns].to_csv(index=False).encode()
#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             "inventory_filtered.csv",
#             "text/csv",
#             use_container_width=True
#         )

#     # ===================== FILTER DATA =====================
#     if search:
#         df_display = df_rename[
#             df_rename["HOSTNAME"].str.contains(search, case=False, na=False)
#             | df_rename["IP_IDRAC"].astype(str).str.contains(search, case=False, na=False)
#             | df_rename["ASSET_TAG"].astype(str).str.contains(search, case=False, na=False)
#         ]
#     else:
#         df_display = df_rename

#     df_display = df_display[selected_columns]

#     # ===================== STYLING =====================
#     def color_status(val):
#         color = "green" if val == "Active" else "red"
#         return f"color: {color}; font-weight: bold;"

#     def style_table(df):
#         styled = df.style
#         if "STATUS" in df.columns:
#             styled = styled.applymap(color_status, subset=["STATUS"])
#         return styled.set_table_styles([
#             {"selector": "thead th", "props": [("background-color", "#1f2937"), ("color", "white"), ("font-weight", "bold"), ("text-align", "center")]},
#             {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#111111")]},
#             {"selector": "tbody tr:hover", "props": [("background-color", "#2d2d2d")]},
#             {"selector": "td, th", "props": [("padding", "8px 12px"), ("border", "1px solid #444")]},
#             {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%"), ("border-radius", "8px"), ("overflow", "hidden")]}
#         ])

#     st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
#     st.write(style_table(df_display).to_html(index=False), unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.info(f"📊 Showing {len(df_display)} records with {len(selected_columns)} columns displayed")

# # ===================== TAB 2: IMPORT DATA =====================
# with tab2:
#     engine = get_db_engine()

#     st.title("📤 Upload Data ke Database")

#     # --- Download Template CSV ---
#     st.subheader("📄 Download Template CSV")

#     columns = [
#         "project_name", "hostname", "site", "rack", "brand", "status", "role",
#         "device_type", "slot", "chassis_tag", "asset_tag", "ip_idrac", "ip_os",
#         "mac_1", "mac_2", "wwn_1", "wwn_2", "core", "cpu", "kontrak_pengadaan",
#         "tahun_pengadaan"
#     ]

#     template_data = {
#         "project_name": ["Project Alpha"],
#         "hostname": ["server-01"],
#         "site": ["DC-A"],
#         "rack": ["R01"],
#         "brand": ["Dell"],
#         "status": [True],
#         "role": ["Compute"],
#         "device_type": ["PowerEdge R740"],
#         "slot": [""],
#         "chassis_tag": [""],
#         "asset_tag": ["AST12345"],
#         "ip_idrac": ["10.10.10.5"],
#         "ip_os": ["10.10.10.6"],
#         "mac_1": ["00:1A:2B:3C:4D:5E"],
#         "mac_2": [""],
#         "wwn_1": [""],
#         "wwn_2": [""],
#         "core": [8],
#         "cpu": ["Intel Xeon Silver 4214"],
#         "kontrak_pengadaan": [""],
#         "tahun_pengadaan": [2021]
#     }

#     template_df = pd.DataFrame(template_data, columns=columns)
#     buffer = io.BytesIO()
#     template_df.to_csv(buffer, index=False)

#     st.download_button(
#         label="⬇️ Download Template CSV",
#         data=buffer.getvalue(),
#         file_name="template_upload_servers.csv",
#         mime="text/csv"
#     )

#     # --- Upload File CSV ---
#     st.subheader("📥 Upload File CSV")
#     uploaded_file = st.file_uploader("Pilih file CSV untuk diupload ke database", type=["csv"])

#     if uploaded_file is not None:
#         df_upload = pd.read_csv(uploaded_file)
#         st.write("📊 Data yang akan diupload:")
#         st.dataframe(df_upload, use_container_width=True)

#         # --- Deteksi Duplikat ---
#         with engine.connect() as conn:
#             existing_df = pd.read_sql("SELECT hostname, ip_idrac, asset_tag FROM mytable", conn)

#         duplicate_mask = existing_df["hostname"].isin(df_upload["hostname"]) | \
#                         existing_df["ip_idrac"].isin(df_upload["ip_idrac"]) | \
#                         existing_df["asset_tag"].isin(df_upload["asset_tag"])
#         duplicates = existing_df[duplicate_mask]

#         if not duplicates.empty:
#             st.warning(f"⚠️ Ditemukan {len(duplicates)} data duplikat berdasarkan hostname / IP iDRAC / asset tag.")
#             with st.expander("👀 Lihat data duplikat"):
#                 st.dataframe(duplicates, use_container_width=True)

#             action = st.radio(
#                 "Pilih tindakan jika ada data duplikat:",
#                 ["❌ Abaikan duplikat", "♻️ Timpa data lama", "➕ Simpan dua-duanya"],
#                 help="Tentukan bagaimana sistem menangani data yang sama.",
#                 key="duplicate_action"
#             )
#         else:
#             action = "Tambah baru"
#             st.success("✅ Tidak ditemukan data duplikat.")

#         # --- Tombol Upload ---
#         if st.button("🚀 Upload ke Database", key="upload_btn"):
#             try:
#                 if not duplicates.empty:
#                     if action == "❌ Abaikan duplikat":
#                         df_final = df_upload[
#                             ~df_upload["hostname"].isin(existing_df["hostname"]) &
#                             ~df_upload["ip_idrac"].isin(existing_df["ip_idrac"]) &
#                             ~df_upload["asset_tag"].isin(existing_df["asset_tag"])
#                         ]
#                     elif action == "♻️ Timpa data lama":
#                         with engine.begin() as conn:
#                             for _, row in df_upload.iterrows():
#                                 conn.execute(
#                                     text("""
#                                         DELETE FROM mytable
#                                         WHERE hostname = :hostname OR ip_idrac = :ip_idrac OR asset_tag = :asset_tag
#                                     """),
#                                     {"hostname": row["hostname"], "ip_idrac": row["ip_idrac"], "asset_tag": row["asset_tag"]}
#                                 )
#                         df_final = df_upload
#                     else:  # Simpan dua-duanya
#                         df_final = df_upload
#                 else:
#                     df_final = df_upload

#                 # Upload ke database
#                 df_final.to_sql("mytable", engine, if_exists="append", index=False)
#                 st.success(f"✅ {len(df_final)} data berhasil diupload ke database!")
#                 st.cache_data.clear()
#                 st.balloons()

#             except Exception as e:
#                 st.error(f"❌ Gagal upload data: {e}")

# # ===================== TAB 3: ANALYTICS =====================
# with tab3:
#     st.subheader("📊 Server Analytics & Visualization")

#     # Row 1: Brand & Status Distribution
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("#### 🏷️ Brand Distribution")
#         brand_count = df_rename["BRAND"].value_counts().reset_index()
#         brand_count.columns = ["BRAND", "COUNT"]
#         fig1 = px.pie(brand_count, values="COUNT", names="BRAND",
#                      color_discrete_sequence=px.colors.sequential.Purples_r,
#                      height=300)
#         fig1.update_traces(textposition='inside', textinfo='percent+label')
#         fig1.update_layout(margin=dict(l=10, r=10, t=30, b=10))
#         st.plotly_chart(fig1, use_container_width=True)

#     with col2:
#         st.markdown("#### ⚡ Status Distribution")
#         status_count = df_rename["STATUS"].value_counts().reset_index()
#         status_count.columns = ["STATUS", "COUNT"]
#         fig2 = px.pie(status_count, values="COUNT", names="STATUS",
#                      color_discrete_map={"Active": "#10b981", "Inactive": "#ef4444"},
#                      height=300)
#         fig2.update_traces(textposition='inside', textinfo='percent+label')
#         fig2.update_layout(margin=dict(l=10, r=10, t=30, b=10))
#         st.plotly_chart(fig2, use_container_width=True)

#     # Row 2: Yearly Procurement & Top Cores
#     col3, col4 = st.columns(2)
#     with col3:
#         st.markdown("#### 📅 Procurement Trend")
#         tahun_count = df_rename["TAHUN_PENGADAAN"].value_counts().sort_index().reset_index()
#         tahun_count.columns = ["YEAR", "COUNT"]
#         fig3 = px.bar(tahun_count, x="YEAR", y="COUNT",
#                      color="COUNT",
#                      color_continuous_scale="Purples",
#                      height=300)
#         fig3.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=50))
#         st.plotly_chart(fig3, use_container_width=True)

#     with col4:
#         st.markdown("#### 🚀 Top 10 by Core")
#         core_top = df_rename[["HOSTNAME", "CORE"]].dropna().astype({"CORE": int}).nlargest(10, "CORE")
#         fig4 = px.bar(core_top, x="HOSTNAME", y="CORE",
#                      color="CORE",
#                      color_continuous_scale="Purples",
#                      height=300)
#         fig4.update_xaxes(tickangle=45)
#         fig4.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=80))
#         st.plotly_chart(fig4, use_container_width=True)

#     # Row 3: Device Type & Treemap
#     col5, col6 = st.columns(2)
#     with col5:
#         st.markdown("#### 🖥️ Device by Site")
#         device_site = df_rename.groupby(["SITE", "DEVICE_TYPE"]).size().reset_index(name="COUNT")
#         fig5 = px.bar(device_site, x="SITE", y="COUNT", color="DEVICE_TYPE",
#                      barmode="stack",
#                      color_discrete_sequence=px.colors.sequential.Purples_r,
#                      height=300)
#         fig5.update_layout(margin=dict(l=10, r=10, t=30, b=50))
#         st.plotly_chart(fig5, use_container_width=True)

#     with col6:
#         st.markdown("#### 🗂️ Server Hierarchy")
#         fig6 = px.treemap(df_rename, path=["SITE", "RACK", "HOSTNAME"],
#                          color="STATUS",
#                          color_discrete_map={"Active": "#10b981", "Inactive": "#ef4444"},
#                          height=300)
#         fig6.update_layout(margin=dict(l=10, r=10, t=30, b=10))
#         st.plotly_chart(fig6, use_container_width=True)

# # ===================== FOOTER =====================
# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #667eea; padding: 20px;'>
#     <p><strong>Dashboard Inventory Server Management</strong> | Auto-refresh every 60 seconds</p>
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import hashlib
import io

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Server Inventory Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ===================== CUSTOM CSS =====================
st.markdown(
    """
<style>
    div.block-container {
        padding-top: 1rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    div[data-testid="metric-container"] label {
        color: white !important;
        font-weight: 600;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0);
    }
    
    /* Custom Tab Buttons */
    div[data-testid="column"] button {
        height: 50px;
        font-size: 16px;
        font-weight: 600;
    }
    
    .login-container {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        color: white;
        text-align: center;
        padding: 50px 30px;
        border-radius: 25px;
        box-shadow: 0 0 30px rgba(0,0,0,0.3);
        margin: 60px auto;
        max-width: 600px;
    }
    
    .login-container h1 {
        font-size: 2.3em;
        margin-bottom: 15px;
        font-weight: 700;
    }
    
    .login-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .scrollable-table {
        max-height: 800px;
        overflow-y: auto;
        border: 1px solid #222;
        border-radius: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ===================== DATABASE CONNECTION =====================
def get_db_connection():
    """Membuat koneksi ke database PostgreSQL"""
    conn_info = {
        "host": "aws-1-ap-southeast-1.pooler.supabase.com",
        "port": "6543",
        "dbname": "postgres",
        "user": "postgres.ppwvmujtrvxwlgxvfwny",
        "password": "mw60fV77ooK72B6D",
    }
    return psycopg2.connect(**conn_info)


# ===================== SESSION STATE INITIALIZATION =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "edit_hostname" not in st.session_state:
    st.session_state.edit_hostname = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0


# ===================== LOGIN FUNCTIONS =====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_login(username, password):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT username, password FROM admin WHERE username = %s"
        cur.execute(query, (username,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            stored_password = result[1]
            if (
                stored_password == hash_password(password)
                or stored_password == password
            ):
                return True
        return False
    except Exception as e:
        st.error(f"Error during login: {str(e)}")
        return False


def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.edit_hostname = None
    st.rerun()


# ===================== DATA FUNCTIONS =====================
@st.cache_data(ttl=60)
def load_data():
    conn = None
    try:
        conn = get_db_connection()

        # Gunakan cursor untuk fetch data, bukan pd.read_sql langsung
        cur = conn.cursor()
        query = """
            SELECT project_name, hostname, site, rack, brand, status, role, device_type, 
                   slot, chassis_tag, asset_tag, ip_idrac, ip_os, mac_1, mac_2, wwn_1, wwn_2, 
                   core, cpu, kontrak_pengadaan, tahun_pengadaan 
            FROM mytable;
        """
        cur.execute(query)

        # Fetch semua data
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        # Buat DataFrame dari hasil fetch
        df = pd.DataFrame(rows, columns=columns)

        cur.close()
        conn.close()

        # Jika data kosong, return DataFrame dengan kolom yang benar
        if df.empty:
            st.warning(
                "⚠️ Tidak ada data di database. Silakan tambahkan data terlebih dahulu."
            )
            return pd.DataFrame(
                columns=[
                    "HOSTNAME",
                    "PROJECT",
                    "SITE",
                    "RACK",
                    "STATUS",
                    "ROLE",
                    "BRAND",
                    "DEVICE_TYPE",
                    "SLOT",
                    "CHASSIS_TAG",
                    "ASSET_TAG",
                    "IP_IDRAC",
                    "IP_OS",
                    "MAC_1",
                    "MAC_2",
                    "WWN_1",
                    "WWN_2",
                    "CORE",
                    "CPU",
                    "KONTRAK_PENGADAAN",
                    "TAHUN_PENGADAAN",
                ]
            )

        df_rename = df.rename(
            columns={
                "hostname": "HOSTNAME",
                "project_name": "PROJECT",
                "site": "SITE",
                "rack": "RACK",
                "status": "STATUS",
                "role": "ROLE",
                "brand": "BRAND",
                "device_type": "DEVICE_TYPE",
                "slot": "SLOT",
                "chassis_tag": "CHASSIS_TAG",
                "asset_tag": "ASSET_TAG",
                "ip_idrac": "IP_IDRAC",
                "ip_os": "IP_OS",
                "mac_1": "MAC_1",
                "mac_2": "MAC_2",
                "wwn_1": "WWN_1",
                "wwn_2": "WWN_2",
                "core": "CORE",
                "cpu": "CPU",
                "kontrak_pengadaan": "KONTRAK_PENGADAAN",
                "tahun_pengadaan": "TAHUN_PENGADAAN",
            }
        )

        df_rename["STATUS"] = df_rename["STATUS"].apply(
            lambda x: "Active" if x in [1, True] else "Inactive"
        )
        return df_rename

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        if conn:
            conn.close()
        # Return DataFrame kosong dengan kolom yang benar
        return pd.DataFrame(
            columns=[
                "HOSTNAME",
                "PROJECT",
                "SITE",
                "RACK",
                "STATUS",
                "ROLE",
                "BRAND",
                "DEVICE_TYPE",
                "SLOT",
                "CHASSIS_TAG",
                "ASSET_TAG",
                "IP_IDRAC",
                "IP_OS",
                "MAC_1",
                "MAC_2",
                "WWN_1",
                "WWN_2",
                "CORE",
                "CPU",
                "KONTRAK_PENGADAAN",
                "TAHUN_PENGADAAN",
            ]
        )


def insert_data(data_dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO mytable (
                project_name, hostname, site, rack, brand, status, role, device_type,
                slot, chassis_tag, asset_tag, ip_idrac, ip_os, mac_1, mac_2, wwn_1, wwn_2,
                core, cpu, kontrak_pengadaan, tahun_pengadaan
            ) VALUES (
                %(project_name)s, %(hostname)s, %(site)s, %(rack)s, %(brand)s, %(status)s, 
                %(role)s, %(device_type)s, %(slot)s, %(chassis_tag)s, %(asset_tag)s, 
                %(ip_idrac)s, %(ip_os)s, %(mac_1)s, %(mac_2)s, %(wwn_1)s, %(wwn_2)s,
                %(core)s, %(cpu)s, %(kontrak_pengadaan)s, %(tahun_pengadaan)s
            )
        """
        cur.execute(query, data_dict)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error inserting data: {str(e)}")
        return False


def insert_admin(data_dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = (
            "INSERT INTO admin (username, password) VALUES (%(username)s, %(password)s)"
        )
        cur.execute(query, data_dict)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error inserting admin: {str(e)}")
        return False


def update_data(hostname, data_dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE mytable SET
                project_name = %(project_name)s,
                site = %(site)s,
                rack = %(rack)s,
                brand = %(brand)s,
                status = %(status)s,
                role = %(role)s,
                device_type = %(device_type)s,
                slot = %(slot)s,
                chassis_tag = %(chassis_tag)s,
                asset_tag = %(asset_tag)s,
                ip_idrac = %(ip_idrac)s,
                ip_os = %(ip_os)s,
                mac_1 = %(mac_1)s,
                mac_2 = %(mac_2)s,
                wwn_1 = %(wwn_1)s,
                wwn_2 = %(wwn_2)s,
                core = %(core)s,
                cpu = %(cpu)s,
                kontrak_pengadaan = %(kontrak_pengadaan)s,
                tahun_pengadaan = %(tahun_pengadaan)s
            WHERE hostname = %(hostname)s
        """
        data_dict["hostname"] = hostname
        cur.execute(query, data_dict)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error updating data: {str(e)}")
        return False


def delete_data(hostname):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = "DELETE FROM mytable WHERE hostname = %s"
        cur.execute(query, (hostname,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting data: {str(e)}")
        return False


# ===================== LOGIN PAGE =====================
if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="login-container">
            <h1>🔐 Server Inventory Dashboard</h1>
            <p>Silakan login untuk mengakses dashboard</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("👤 Username", key="login_username")
            password = st.text_input(
                "🔒 Password", type="password", key="login_password"
            )
            submitted = st.form_submit_button("🚀 Login", use_container_width=True)

            if submitted:
                if username and password:
                    if verify_login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Welcome, {username}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter username and password")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ===================== MAIN DASHBOARD =====================
# Sidebar
with st.sidebar:
    st.title("📊 Dashboard Menu")
    st.write(f"Welcome, **{st.session_state.username}** 👋")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# Header
st.markdown(
    """
<div class="main-header">
    <h1>🖥️ Dashboard Inventory Server Management</h1>
</div>
""",
    unsafe_allow_html=True,
)

# Load Data
df_rename = load_data()

# Metrics
total = len(df_rename)
active = (
    len(df_rename[df_rename["STATUS"] == "Active"])
    if not df_rename.empty and "STATUS" in df_rename.columns
    else 0
)
inactive = total - active

col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Server", total)
col2.metric("✅ Active", active)
col3.metric("⚠️ Inactive", inactive)

st.divider()


# ===================== TABS =====================
def set_tab(tab_index):
    st.session_state.active_tab = tab_index


tab_names = [
    "📋 Data View",
    "➕ Add Data",
    "✏️ Edit Data",
    "📤 Import Data",
    "📈 Analytics",
]

tab_cols = st.columns(5)
for idx, (col, name) in enumerate(zip(tab_cols, tab_names)):
    with col:
        if st.button(
            name,
            key=f"tab_{idx}",
            use_container_width=True,
            type="primary" if st.session_state.active_tab == idx else "secondary",
        ):
            set_tab(idx)

st.markdown("---")

# Tampilkan konten berdasarkan active tab
if st.session_state.active_tab == 0:
    # TAB 1: DATA VIEW
    st.subheader("🔎 Search & View Data")

    # Check jika data kosong
    if df_rename.empty:
        st.info(
            "📭 Belum ada data. Silakan tambahkan data di tab 'Add Data' atau import CSV."
        )
    else:
        all_columns = df_rename.columns.tolist()
        selected_columns = st.multiselect(
            "🧭 Select columns to display:",
            options=all_columns,
            default=all_columns,
            help="Uncheck columns you want to hide from the table.",
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input(
                "🔍 Search (All Fields):",
                placeholder="Search by Hostname, Project, IP, Asset Tag, Brand, Site, etc...",
                help="Pencarian akan mencari di semua kolom yang tersedia",
            )
        with col2:
            st.write("")
            st.write("")
            csv = df_rename[selected_columns].to_csv(index=False).encode()
            st.download_button(
                "📥 Download CSV",
                csv,
                "inventory_filtered.csv",
                "text/csv",
                use_container_width=True,
            )

        # Sorting controls
        col_sort1, col_sort2, col_sort3 = st.columns(3)
        with col_sort1:
            sort_by = st.selectbox(
                "📊 Sort By:",
                options=[
                    "HOSTNAME",
                    "PROJECT",
                    "TAHUN_PENGADAAN",
                    "BRAND",
                    "SITE",
                    "STATUS",
                    "CORE",
                ],
                index=0,
                help="Pilih kolom untuk sorting",
            )
        with col_sort2:
            sort_order = st.radio(
                "🔼 Sort Order:",
                options=["Ascending ⬆️", "Descending ⬇️"],
                horizontal=True,
                index=0,
            )
        with col_sort3:
            st.write("")
            st.write("")
            if st.button("🔄 Reset Filters", use_container_width=True):
                st.rerun()

        # Search filtering
        if search:
            mask = pd.Series([False] * len(df_rename))
            for column in df_rename.columns:
                mask |= (
                    df_rename[column]
                    .astype(str)
                    .str.contains(search, case=False, na=False)
                )
            df_display = df_rename[mask]
        else:
            df_display = df_rename

        # Sorting
        ascending = True if "Ascending" in sort_order else False
        df_display = df_display.sort_values(by=sort_by, ascending=ascending)
        
        # Reset index untuk nomor urut yang benar
        df_display = df_display.reset_index(drop=True)
        df_display = df_display[selected_columns]

        # PAGINATION CONTROLS
        st.markdown("---")
        col_page1, col_page2, col_page3 = st.columns([1, 2, 1])
        
        with col_page1:
            rows_per_page = st.selectbox(
                "📄 Rows per page:",
                options=[50, 100, 200, "All"],
                index=0,
                help="Pilih jumlah baris yang ditampilkan per halaman"
            )
        
        total_rows = len(df_display)
        
        # Initialize page number in session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Calculate total pages
        if rows_per_page == "All":
            total_pages = 1
            df_paginated = df_display.copy()
            # Tambahkan kolom nomor urut
            df_paginated.insert(0, 'No', range(1, len(df_paginated) + 1))
        else:
            total_pages = max(1, (total_rows + rows_per_page - 1) // rows_per_page)
            
            # Reset to page 1 if current page exceeds total pages
            if st.session_state.current_page > total_pages:
                st.session_state.current_page = 1
            
            # Calculate start and end indices
            start_idx = (st.session_state.current_page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            df_paginated = df_display.iloc[start_idx:end_idx].copy()
            
            # # Tambahkan kolom nomor urut yang kontinyu
            # df_paginated.insert(0, 'No', range(start_idx + 1, end_idx + 1))
        
        with col_page2:
            if rows_per_page != "All" and total_pages > 1:
                st.write("")
                col_prev, col_info, col_next = st.columns([1, 2, 1])
                
                with col_prev:
                    if st.button("⬅️ Previous", disabled=(st.session_state.current_page == 1), use_container_width=True):
                        st.session_state.current_page -= 1
                        st.rerun()
                
                with col_info:
                    st.markdown(f"<div style='text-align: center; padding-top: 8px;'><b>Page {st.session_state.current_page} of {total_pages}</b></div>", unsafe_allow_html=True)
                
                with col_next:
                    if st.button("Next ➡️", disabled=(st.session_state.current_page == total_pages), use_container_width=True):
                        st.session_state.current_page += 1
                        st.rerun()
        
        with col_page3:
            if rows_per_page != "All" and total_pages > 1:
                page_jump = st.number_input(
                    "Go to page:",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state.current_page,
                    step=1,
                    help="Langsung loncat ke halaman tertentu"
                )
                if page_jump != st.session_state.current_page:
                    st.session_state.current_page = page_jump
                    st.rerun()

        st.markdown("---")

        # Styling functions
        def color_status(val):
            color = "green" if val == "Active" else "red"
            return f"color: {color}; font-weight: bold;"

        def style_table(df):
            styled = df.style
            if "STATUS" in df.columns:
                styled = styled.map(color_status, subset=["STATUS"])
            return styled.set_table_styles(
                [
                    {
                        "selector": "thead th",
                        "props": [
                            ("background-color", "#4CAF50"),
                            ("color", "#000000"),
                            ("font-weight", "bold"),
                            ("text-align", "center"),
                            ("padding", "12px 8px"),
                            ("position", "sticky"),
                            ("top", "0"),
                            ("z-index", "10"),
                        ],
                    },
                    {
                        "selector": "tbody tr:nth-child(even)",
                        "props": [
                            ("background-color", "#ffffff"),
                        ],
                    },
                    {
                        "selector": "tbody tr:nth-child(odd)",
                        "props": [
                            ("background-color", "#ffffff"),
                        ],
                    },
                    {
                        "selector": "td, th",
                        "props": [
                            ("padding", "10px 8px"),
                            ("border", "1px solid #ddd"),
                            ("text-align", "left"),
                            ("white-space", "nowrap"),
                        ],
                    },

                    {
                        "selector": "table",
                        "props": [
                            ("border-collapse", "collapse"),
                            ("width", "100%"),
                            ("font-size", "14px"),
                            ("box-shadow", "0 2px 4px rgba(0,0,0,0.1)"),
                        ],
                    },
                ]
            )

        # Display table with horizontal scroll
        st.markdown(
            """
            <style>
            .scrollable-table {
                overflow-x: auto;
                overflow-y: auto;
                max-height: 600px;
                border-radius: 8px;
                border: 1px solid #ddd;
                margin-bottom: 20px;
            }
            .scrollable-table table {
                margin: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
        st.write(style_table(df_paginated).to_html(index=False), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Info summary
        if rows_per_page == "All":
            st.info(
                f"📊 Showing all {total_rows} records with {len(selected_columns)} columns displayed"
            )
        else:
            start_idx = (st.session_state.current_page - 1) * rows_per_page + 1
            end_idx = min(start_idx + rows_per_page - 1, total_rows)
            st.info(
                f"📊 Showing {start_idx}-{end_idx} of {total_rows} records with {len(selected_columns)} columns displayed"
            )

elif st.session_state.active_tab == 1:
    # TAB 2: ADD DATA
    st.subheader("➕ Add New Server Data")

    with st.form("add_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            hostname = st.text_input("Hostname *", placeholder="e.g., server-01")
            project = st.text_input("Project Name", placeholder="e.g., Project Alpha")
            site = st.text_input("Site", placeholder="e.g., DC-A")
            rack = st.text_input("Rack", placeholder="e.g., R01")
            brand = st.text_input("Brand", placeholder="e.g., Dell")
            status = st.selectbox(
                "Status",
                [True, False],
                format_func=lambda x: "Active" if x else "Inactive",
            )

        with col2:
            role = st.text_input("Role", placeholder="e.g., Compute")
            device_type = st.text_input(
                "Device Type", placeholder="e.g., PowerEdge R740"
            )
            slot = st.text_input("Slot", placeholder="e.g., 1")
            chassis_tag = st.text_input("Chassis Tag")
            asset_tag = st.text_input("Asset Tag", placeholder="e.g., AST12345")
            ip_idrac = st.text_input("IP iDRAC", placeholder="e.g., 10.10.10.5")

        with col3:
            ip_os = st.text_input("IP OS", placeholder="e.g., 10.10.10.6")
            mac_1 = st.text_input("MAC 1", placeholder="e.g., 00:1A:2B:3C:4D:5E")
            mac_2 = st.text_input("MAC 2")
            wwn_1 = st.text_input("WWN 1")
            wwn_2 = st.text_input("WWN 2")
            core = st.number_input("Core", min_value=0, value=8)

        col4, col5 = st.columns(2)
        with col4:
            cpu = st.text_input("CPU", placeholder="e.g., Intel Xeon Silver 4214")
        with col5:
            kontrak = st.text_input("Kontrak Pengadaan")

        tahun = st.number_input(
            "Tahun Pengadaan", min_value=2000, max_value=2100, value=2024
        )

        if st.form_submit_button("💾 Add Data", use_container_width=True):
            if not hostname:
                st.error("❌ Hostname is required!")
            else:
                data = {
                    "hostname": hostname,
                    "project_name": project,
                    "site": site,
                    "rack": rack,
                    "brand": brand,
                    "status": status,
                    "role": role,
                    "device_type": device_type,
                    "slot": slot,
                    "chassis_tag": chassis_tag,
                    "asset_tag": asset_tag,
                    "ip_idrac": ip_idrac,
                    "ip_os": ip_os,
                    "mac_1": mac_1,
                    "mac_2": mac_2,
                    "wwn_1": wwn_1,
                    "wwn_2": wwn_2,
                    "core": int(core),
                    "cpu": cpu,
                    "kontrak_pengadaan": kontrak,
                    "tahun_pengadaan": int(tahun),
                }
                if insert_data(data):
                    st.success("✅ Data successfully added!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()

elif st.session_state.active_tab == 2:
    # TAB 3: EDIT DATA
    st.subheader("✏️ Edit or Delete Server Data")

    def set_edit_hostname():
        if st.session_state.hostname_selector:
            st.session_state.edit_hostname = st.session_state.hostname_selector.split(
                " | "
            )[0]
            st.session_state.active_tab = 2

    options = df_rename.apply(
        lambda row: f"{row['HOSTNAME']} | {row['IP_OS']}", axis=1
    ).tolist()

    selected_value = st.selectbox(
        "Select Hostname or IP OS:",
        [""] + options,
        key="hostname_selector",
        on_change=set_edit_hostname,
    )

    if st.session_state.edit_hostname:
        hostname = st.session_state.edit_hostname
        server_data = df_rename[df_rename["HOSTNAME"] == hostname].iloc[0]

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Delete Server", use_container_width=True, key="delete_btn"):
                if delete_data(server_data["HOSTNAME"]):
                    st.success(f"✅ Server {server_data['HOSTNAME']} deleted!")
                    st.cache_data.clear()
                    st.session_state.edit_hostname = None
                    time.sleep(1)
                    st.rerun()

        with st.form("edit_form", clear_on_submit=False):
            col1, col2, col3 = st.columns(3)

            def safe_get(key, default=""):
                return server_data[key] if pd.notna(server_data[key]) else default

            with col1:
                project = st.text_input("Project Name", value=safe_get("PROJECT"))
                site = st.text_input("Site", value=safe_get("SITE"))
                rack = st.text_input("Rack", value=safe_get("RACK"))
                brand = st.text_input("Brand", value=safe_get("BRAND"))
                status = st.selectbox(
                    "Status",
                    [True, False],
                    index=0 if safe_get("STATUS") == "Active" else 1,
                    format_func=lambda x: "Active" if x else "Inactive",
                )
                role = st.text_input("Role", value=safe_get("ROLE"))

            with col2:
                device_type = st.text_input(
                    "Device Type", value=safe_get("DEVICE_TYPE")
                )
                slot = st.text_input("Slot", value=safe_get("SLOT"))
                chassis_tag = st.text_input(
                    "Chassis Tag", value=safe_get("CHASSIS_TAG")
                )
                asset_tag = st.text_input("Asset Tag", value=safe_get("ASSET_TAG"))
                ip_idrac = st.text_input("IP iDRAC", value=safe_get("IP_IDRAC"))
                ip_os = st.text_input("IP OS", value=safe_get("IP_OS"))

            with col3:
                mac_1 = st.text_input("MAC 1", value=safe_get("MAC_1"))
                mac_2 = st.text_input("MAC 2", value=safe_get("MAC_2"))
                wwn_1 = st.text_input("WWN 1", value=safe_get("WWN_1"))
                wwn_2 = st.text_input("WWN 2", value=safe_get("WWN_2"))
                core = st.number_input("Core", value=int(safe_get("CORE", 0)))
                cpu = st.text_input("CPU", value=safe_get("CPU"))
                kontrak = st.text_input("Kontrak", value=safe_get("KONTRAK_PENGADAAN"))
                tahun = st.number_input(
                    "Tahun", value=int(safe_get("TAHUN_PENGADAAN", 2024))
                )

            if st.form_submit_button("💾 Update Data", use_container_width=True):
                data = {
                    "project_name": project,
                    "site": site,
                    "rack": rack,
                    "brand": brand,
                    "status": status,
                    "role": role,
                    "device_type": device_type,
                    "slot": slot,
                    "chassis_tag": chassis_tag,
                    "asset_tag": asset_tag,
                    "ip_idrac": ip_idrac,
                    "ip_os": ip_os,
                    "mac_1": mac_1,
                    "mac_2": mac_2,
                    "wwn_1": wwn_1,
                    "wwn_2": wwn_2,
                    "core": int(core),
                    "cpu": cpu,
                    "kontrak_pengadaan": kontrak,
                    "tahun_pengadaan": int(tahun),
                }
                if update_data(server_data["HOSTNAME"], data):
                    st.success("✅ Data successfully updated!")
                    st.cache_data.clear()
                    st.session_state.edit_hostname = None
                    time.sleep(1)
                    st.rerun()

elif st.session_state.active_tab == 3:
# TAB 4: IMPORT DATA
    st.title("📤 Upload Data ke Database")

    # Field definitions
    REQUIRED_FIELDS = [
        "hostname", "site", "rack", "role", "brand", "status",
        "project_name", "device_type", "kontrak_pengadaan", "tahun_pengadaan",
        "slot", "parent", "chassis_tag", "asset_tag"
    ]
    OPTIONAL_FIELDS = [
        "core", "cpu", "ip_idrac", "ip_os",
        "mac_1", "mac_2", "memory", 
        "wwn_1", "wwn_2"
    ]
    
    INTEGER_FIELDS = ["core", "memory", "tahun_pengadaan"]
    BOOLEAN_FIELDS = ["status"]

    st.subheader("📄 Download Template CSV")
    
    # Info about required fields
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("""**✅ Field Wajib Diisi (14 field):**
        
**Basic Info:**
- hostname
- site
- rack
- role
- brand
- device_type
- status (True/False)

**Asset Tracking:**
- project_name
- kontrak_pengadaan
- tahun_pengadaan
- asset_tag

**Chassis/Blade Info:**
- parent (nama chassis)
- chassis_tag
- slot
        """)
    with col_info2:
        st.info("""**📝 Field Opsional (9 field):**
        
**Hardware Specs:**
- core
- cpu
- memory

**Network:**
- ip_idrac
- ip_os
- mac_1
- mac_2

**Storage:**
- wwn_1
- wwn_2

---
**💡 Tips Status:**
- Tulis **"Active"** atau **"Inactive"**
- Case insensitive (besar/kecil huruf sama saja)
- Variasi diterima:
  - Active: active, ACTIVE, true, 1
  - Inactive: inactive, INACTIVE, false, 0
        """)

    # Create comprehensive template
    all_columns = REQUIRED_FIELDS + OPTIONAL_FIELDS

    template_data = {
        # REQUIRED FIELDS - Basic Info
        "hostname": ["server-blade-01", "server-rack-02", "chassis-01"],
        "site": ["DC-A", "DC-B", "DC-A"],
        "rack": ["R01", "R02", "R01"],
        "role": ["Compute", "Storage", "Chassis"],
        "brand": ["Dell", "HPE", "Dell"],
        "device_type": ["PowerEdge M640", "ProLiant DL380", "PowerEdge M1000e"],
        "status": ["Active", "Active", "Inactive"],  # Gunakan: Active atau Inactive
        
        # REQUIRED FIELDS - Asset Tracking
        "project_name": ["Project Alpha", "Project Beta", "Project Alpha"],
        "kontrak_pengadaan": ["K-2021-001", "K-2022-005", "K-2021-001"],
        "tahun_pengadaan": [2021, 2022, 2021],
        "asset_tag": ["AST12345", "AST12346", "AST12347"],
        
        # REQUIRED FIELDS - Chassis/Blade Info
        "parent": ["chassis-01", "", ""],  # Kosongkan jika bukan blade
        "chassis_tag": ["CHS001", "", "CHS001"],  # Service tag chassis
        "slot": ["Slot-1", "", ""],  # Kosongkan jika bukan blade
        
        # OPTIONAL FIELDS - Hardware Specs
        "core": [8, 16, ""],  # Bisa kosong untuk chassis
        "cpu": ["Intel Xeon Silver 4214", "Intel Xeon Gold 6248", ""],
        "memory": [64, 128, ""],  # GB
        
        # OPTIONAL FIELDS - Network
        "ip_idrac": ["10.10.10.5", "10.10.10.6", "10.10.10.4"],
        "ip_os": ["192.168.1.10", "192.168.1.11", ""],
        "mac_1": ["00:1A:2B:3C:4D:5E", "00:1A:2B:3C:4D:5F", ""],
        "mac_2": ["00:1A:2B:3C:4D:61", "", ""],
        
        # OPTIONAL FIELDS - Storage
        "wwn_1": ["", "50:06:01:60:12:34:56:78", ""],
        "wwn_2": ["", "50:06:01:60:12:34:56:79", ""],
    }

    template_df = pd.DataFrame(template_data, columns=all_columns)
    buffer = io.BytesIO()
    template_df.to_csv(buffer, index=False)

    st.download_button(
        label="⬇️ Download Template CSV Lengkap",
        data=buffer.getvalue(),
        file_name="template_upload_devices.csv",
        mime="text/csv",
        help="Template sudah berisi contoh data untuk memudahkan pengisian"
    )

    st.markdown("---")
    st.subheader("📥 Upload File CSV")
    
    uploaded_file = st.file_uploader(
        "Pilih file CSV untuk diupload ke database", 
        type=["csv"],
        help="File CSV harus mengikuti format template yang sudah disediakan"
    )

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            
            # ========== VALIDATION SECTION ==========
            st.write("### 🔍 Validasi Data")
            
            validation_errors = []
            validation_warnings = []
            
            # 1. Check required columns exist
            missing_columns = [col for col in REQUIRED_FIELDS if col not in df_upload.columns]
            if missing_columns:
                validation_errors.append(f"❌ Kolom wajib tidak ditemukan: {', '.join(missing_columns)}")
            
            # 2. Check required fields are not empty
            if not missing_columns:
                for col in REQUIRED_FIELDS:
                    empty_count = df_upload[col].isna().sum() + (df_upload[col] == "").sum()
                    if empty_count > 0:
                        validation_errors.append(f"❌ Kolom '{col}' (wajib) memiliki {empty_count} baris kosong")
            
            # 3. Validate data types
            for col in INTEGER_FIELDS:
                if col in df_upload.columns:
                    # Allow empty values for optional integer fields
                    non_empty = df_upload[col].dropna()
                    non_empty = non_empty[non_empty != ""]
                    
                    if len(non_empty) > 0:
                        try:
                            pd.to_numeric(non_empty, errors='raise')
                        except:
                            invalid_rows = []
                            for idx, val in non_empty.items():
                                try:
                                    int(val)
                                except:
                                    invalid_rows.append(f"Row {idx+2}: {val}")
                            if invalid_rows:
                                validation_errors.append(
                                    f"❌ Kolom '{col}' harus berisi angka. Invalid di:\n  " + 
                                    "\n  ".join(invalid_rows[:5]) + 
                                    (f"\n  ... dan {len(invalid_rows)-5} lainnya" if len(invalid_rows) > 5 else "")
                                )
            
            # 4. Validate boolean field (status)
            if "status" in df_upload.columns:
                invalid_status = []
                for idx, val in df_upload["status"].items():
                    if pd.isna(val) or str(val).strip() == "":
                        invalid_status.append(f"Row {idx+2}: kosong")
                    else:
                        val_str = str(val).strip().lower()
                        # Accept: active/inactive in any case, true/false, 1/0
                        valid_values = ['active', 'inactive', 'true', 'false', '1', '0']
                        if val_str not in valid_values:
                            invalid_status.append(f"Row {idx+2}: '{val}' (harus Active atau Inactive)")
                
                if invalid_status:
                    validation_errors.append(
                        f"❌ Kolom 'status' harus berisi Active atau Inactive (case insensitive). Invalid di:\n  " + 
                        "\n  ".join(invalid_status[:5]) +
                        (f"\n  ... dan {len(invalid_status)-5} lainnya" if len(invalid_status) > 5 else "") +
                        "\n\n  ✅ Nilai yang diterima: Active, Inactive, active, inactive, ACTIVE, INACTIVE, true, false, 1, 0"
                    )
            
            # 5. Check for duplicate hostnames in upload file
            duplicate_hostnames = df_upload[df_upload.duplicated(subset=['hostname'], keep=False)]
            if not duplicate_hostnames.empty:
                validation_errors.append(
                    f"❌ Ditemukan {len(duplicate_hostnames)} hostname duplikat dalam file upload:\n  " +
                    "\n  ".join(duplicate_hostnames['hostname'].unique()[:5].tolist()) +
                    (f"\n  ... dan {len(duplicate_hostnames['hostname'].unique())-5} lainnya" if len(duplicate_hostnames['hostname'].unique()) > 5 else "")
                )
            
            # 6. Warnings for optional fields
            for col in OPTIONAL_FIELDS:
                if col in df_upload.columns:
                    empty_count = df_upload[col].isna().sum() + (df_upload[col] == "").sum()
                    if empty_count == len(df_upload):
                        validation_warnings.append(f"⚠️ Kolom '{col}' (opsional) kosong di semua baris")
            
            # Display validation results
            if validation_errors:
                st.error("### ❌ Validasi Gagal - Perbaiki Error Berikut:")
                for error in validation_errors:
                    st.error(error)
                st.stop()
            
            if validation_warnings:
                with st.expander("⚠️ Peringatan (tidak menghalangi upload)"):
                    for warning in validation_warnings:
                        st.warning(warning)
            
            st.success("✅ Validasi data berhasil!")
            
            # ========== DISPLAY UPLOADED DATA ==========
            st.write("### 📊 Data yang Akan Diupload:")
            st.dataframe(df_upload, use_container_width=True)
            st.info(f"Total: {len(df_upload)} baris data")

            # ========== CHECK DUPLICATES IN DATABASE ==========
            conn = get_db_connection()
            existing_df = pd.read_sql(
                "SELECT hostname, ip_idrac, asset_tag FROM mytable", conn
            )
            conn.close()

            # Check for duplicates
            duplicate_hostname = df_upload[df_upload["hostname"].isin(existing_df["hostname"])]
            duplicate_ip = df_upload[df_upload["ip_idrac"].isin(existing_df["ip_idrac"])] if "ip_idrac" in df_upload.columns else pd.DataFrame()
            duplicate_asset = df_upload[df_upload["asset_tag"].isin(existing_df["asset_tag"])] if "asset_tag" in df_upload.columns else pd.DataFrame()

            has_duplicates = not (duplicate_hostname.empty and duplicate_ip.empty and duplicate_asset.empty)

            if has_duplicates:
                st.warning("### ⚠️ Deteksi Data Duplikat di Database")
                
                if not duplicate_hostname.empty:
                    with st.expander(f"🔴 {len(duplicate_hostname)} Hostname duplikat"):
                        st.dataframe(duplicate_hostname[["hostname", "site", "rack"]], use_container_width=True)
                
                if not duplicate_ip.empty:
                    with st.expander(f"🔴 {len(duplicate_ip)} IP iDRAC duplikat"):
                        st.dataframe(duplicate_ip[["hostname", "ip_idrac"]], use_container_width=True)
                
                if not duplicate_asset.empty:
                    with st.expander(f"🔴 {len(duplicate_asset)} Asset Tag duplikat"):
                        st.dataframe(duplicate_asset[["hostname", "asset_tag"]], use_container_width=True)

                action = st.radio(
                    "Pilih tindakan untuk data duplikat:",
                    ["❌ Skip duplikat (hanya tambah data baru)", 
                     "♻️ Update/Timpa data lama", 
                     "➕ Paksa tambah semua (bisa duplikat)"],
                    help="Tentukan bagaimana sistem menangani data yang sudah ada di database.",
                )
            else:
                action = "Tambah baru"
                st.success("✅ Tidak ada duplikat dengan data di database")

            # ========== UPLOAD BUTTON ==========
            st.markdown("---")
            if st.button("🚀 Upload ke Database", type="primary", use_container_width=True):
                try:
                    # Normalize status values - Fleksibel menerima berbagai format
                    if "status" in df_upload.columns:
                        def normalize_status(val):
                            """Convert any status format to boolean"""
                            if pd.isna(val):
                                return False  # Default to Inactive if empty
                            
                            val_str = str(val).strip().lower()
                            
                            # Active variations
                            if val_str in ['active', 'true', '1', 'yes', 'aktif', 'on']:
                                return True
                            # Inactive variations
                            elif val_str in ['inactive', 'false', '0', 'no', 'nonaktif', 'off']:
                                return False
                            else:
                                # Default to True if contains "active", else False
                                return 'active' in val_str
                        
                        df_upload["status"] = df_upload["status"].apply(normalize_status)
                    
                    # Convert integer fields
                    for col in INTEGER_FIELDS:
                        if col in df_upload.columns:
                            df_upload[col] = pd.to_numeric(df_upload[col], errors='coerce')
                    
                    conn = get_db_connection()
                    cur = conn.cursor()
                    
                    uploaded_count = 0
                    skipped_count = 0
                    updated_count = 0

                    # Determine which rows to process
                    if has_duplicates:
                        if action == "❌ Skip duplikat (hanya tambah data baru)":
                            # Only insert non-duplicates
                            df_final = df_upload[
                                ~df_upload["hostname"].isin(existing_df["hostname"])
                            ]
                            skipped_count = len(df_upload) - len(df_final)
                            
                        elif action == "♻️ Update/Timpa data lama":
                            df_final = df_upload
                            # Delete existing records first
                            for _, row in df_upload.iterrows():
                                cur.execute(
                                    """
                                    DELETE FROM mytable
                                    WHERE hostname = %s
                                    """,
                                    (row["hostname"],)
                                )
                            conn.commit()
                            updated_count = len(duplicate_hostname)
                            
                        else:  # Paksa tambah semua
                            df_final = df_upload
                    else:
                        df_final = df_upload

                    # Insert data
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, row in df_final.iterrows():
                        try:
                            cur.execute(
                                """
                                INSERT INTO mytable (
                                    hostname, site, rack, role, brand, status,
                                    device_type, chassis_tag, asset_tag, parent, slot,
                                    core, cpu, ip_idrac, ip_os, kontrak_pengadaan,
                                    mac_1, mac_2, memory, tahun_pengadaan,
                                    wwn_1, wwn_2, project_name
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                )
                                """,
                                (
                                    row.get("hostname"),
                                    row.get("site"),
                                    row.get("rack"),
                                    row.get("role"),
                                    row.get("brand"),
                                    row.get("status"),
                                    row.get("device_type") if pd.notna(row.get("device_type")) else None,
                                    row.get("chassis_tag") if pd.notna(row.get("chassis_tag")) else None,
                                    row.get("asset_tag") if pd.notna(row.get("asset_tag")) else None,
                                    row.get("parent") if pd.notna(row.get("parent")) else None,
                                    row.get("slot") if pd.notna(row.get("slot")) else None,
                                    int(row.get("core")) if pd.notna(row.get("core")) else None,
                                    row.get("cpu") if pd.notna(row.get("cpu")) else None,
                                    row.get("ip_idrac") if pd.notna(row.get("ip_idrac")) else None,
                                    row.get("ip_os") if pd.notna(row.get("ip_os")) else None,
                                    row.get("kontrak_pengadaan") if pd.notna(row.get("kontrak_pengadaan")) else None,
                                    row.get("mac_1") if pd.notna(row.get("mac_1")) else None,
                                    row.get("mac_2") if pd.notna(row.get("mac_2")) else None,
                                    int(row.get("memory")) if pd.notna(row.get("memory")) else None,
                                    int(row.get("tahun_pengadaan")) if pd.notna(row.get("tahun_pengadaan")) else None,
                                    row.get("wwn_1") if pd.notna(row.get("wwn_1")) else None,
                                    row.get("wwn_2") if pd.notna(row.get("wwn_2")) else None,
                                    row.get("project_name") if pd.notna(row.get("project_name")) else None,
                                ),
                            )
                            uploaded_count += 1
                            
                            # Update progress
                            progress = (idx + 1) / len(df_final)
                            progress_bar.progress(progress)
                            status_text.text(f"Uploading... {idx + 1}/{len(df_final)}")
                            
                        except Exception as row_error:
                            st.error(f"❌ Error pada baris {idx + 2} (hostname: {row.get('hostname')}): {row_error}")
                            conn.rollback()
                            cur.close()
                            conn.close()
                            st.stop()

                    conn.commit()
                    cur.close()
                    conn.close()
                    
                    progress_bar.empty()
                    status_text.empty()

                    # Success message
                    st.balloons()
                    st.success(f"""
                    ### ✅ Upload Berhasil!
                    - **{uploaded_count}** data berhasil diupload
                    {f"- **{updated_count}** data di-update" if updated_count > 0 else ""}
                    {f"- **{skipped_count}** data diskip (duplikat)" if skipped_count > 0 else ""}
                    """)
                    
                    st.cache_data.clear()
                    time.sleep(2)
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Gagal upload data: {str(e)}")
                    if 'conn' in locals():
                        conn.rollback()
                        conn.close()

        except Exception as e:
            st.error(f"❌ Error membaca file CSV: {str(e)}")
            st.info("💡 Pastikan file CSV menggunakan format yang benar dan encoding UTF-8")

elif st.session_state.active_tab == 4:
# TAB 5: ANALYTICS
    st.subheader("📊 Server Analytics & Visualization")

    # Filter options
    st.markdown("### 🎯 Analytics Filters")
    col_filter1, col_filter2, col_filter3, col_filter4, col_filter5 = st.columns([2, 2, 2, 2, 1])
    
    with col_filter1:
        filter_site = st.selectbox(
            "🏢 Site:",
            options=["All"] + sorted(df_rename["SITE"].dropna().unique().tolist()),
            help="Filter berdasarkan site tertentu"
        )
    
    with col_filter2:
        filter_rack = st.selectbox(
            "🗄️ Rack:",
            options=["All"] + sorted(df_rename["RACK"].dropna().unique().tolist()),
            help="Filter berdasarkan rack tertentu"
        )
    
    with col_filter3:
        filter_role = st.selectbox(
            "👔 Role:",
            options=["All"] + sorted(df_rename["ROLE"].dropna().unique().tolist()),
            help="Filter berdasarkan role tertentu"
        )
    
    with col_filter4:
        filter_brand = st.selectbox(
            "🏷️ Brand:",
            options=["All"] + sorted(df_rename["BRAND"].dropna().unique().tolist()),
            help="Filter berdasarkan brand tertentu"
        )
    
    with col_filter5:
        st.write("")
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()

    # Apply filters
    df_analytics = df_rename.copy()
    
    if filter_site != "All":
        df_analytics = df_analytics[df_analytics["SITE"] == filter_site]
    
    if filter_rack != "All":
        df_analytics = df_analytics[df_analytics["RACK"] == filter_rack]
    
    if filter_role != "All":
        df_analytics = df_analytics[df_analytics["ROLE"] == filter_role]
    
    if filter_brand != "All":
        df_analytics = df_analytics[df_analytics["BRAND"] == filter_brand]

    # Check if data is empty after filtering
    if df_analytics.empty:
        st.warning("⚠️ No data available with current filters. Please adjust your filter settings.")
    else:
        # Color palette
        bright_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
            "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B739", "#52D273",
        ]

        # KPI Metrics Row
        st.markdown("### 📈 Key Performance Indicators")
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        
        with kpi1:
            total_devices = len(df_analytics)
            st.metric("🖥️ Total Devices", f"{total_devices:,}")
        
        with kpi2:
            active_count = len(df_analytics[df_analytics["STATUS"] == "Active"])
            active_pct = (active_count / total_devices * 100) if total_devices > 0 else 0
            st.metric("✅ Active", f"{active_count:,}", f"{active_pct:.1f}%")
        
        with kpi3:
            inactive_count = len(df_analytics[df_analytics["STATUS"] == "Inactive"])
            st.metric("❌ Inactive", f"{inactive_count:,}")
        
        with kpi4:
            total_cores = df_analytics["CORE"].dropna().astype(int).sum()
            st.metric("⚡ Total Cores", f"{total_cores:,}")
        
        with kpi5:
            avg_cores = df_analytics["CORE"].dropna().astype(int).mean()
            st.metric("📊 Avg Cores", f"{avg_cores:.1f}")

        st.markdown("---")

        # Row 1: Brand and Status Distribution
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏷️ Brand Distribution")
            brand_count = df_analytics["BRAND"].value_counts().reset_index()
            brand_count.columns = ["BRAND", "COUNT"]
            fig1 = px.pie(
                brand_count,
                values="COUNT",
                names="BRAND",
                color_discrete_sequence=bright_colors,
                height=350,
            )
            fig1.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=14,
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            fig1.update_layout(
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=13, color="#FFFFFF"),
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("#### ⚡ Status Distribution")
            status_count = df_analytics["STATUS"].value_counts().reset_index()
            status_count.columns = ["STATUS", "COUNT"]
            fig2 = px.pie(
                status_count,
                values="COUNT",
                names="STATUS",
                color_discrete_map={"Active": "#00E676", "Inactive": "#FF5252"},
                height=350,
            )
            fig2.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=14,
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            fig2.update_layout(
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=13, color="#FFFFFF"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Row 2: Procurement and Core Analysis
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### 📅 Procurement Trend by Year")
            tahun_count = (
                df_analytics["TAHUN_PENGADAAN"].value_counts().sort_index().reset_index()
            )
            tahun_count.columns = ["YEAR", "COUNT"]
            fig3 = px.bar(
                tahun_count,
                x="YEAR",
                y="COUNT",
                color="COUNT",
                color_continuous_scale=[[0, "#4ECDC4"], [0.5, "#45B7D1"], [1, "#FF6B6B"]],
                height=350,
                text="COUNT",
            )
            fig3.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color="#FFFFFF",
                marker_line_width=1.5
            )
            fig3.update_layout(
                showlegend=False,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Year"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Count"),
                font=dict(color="#FFFFFF"),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown("#### 🚀 Top 10 Devices by Core Count")
            core_top = (
                df_analytics[["HOSTNAME", "CORE", "BRAND"]]
                .dropna()
                .astype({"CORE": int})
                .nlargest(10, "CORE")
            )
            fig4 = px.bar(
                core_top,
                x="HOSTNAME",
                y="CORE",
                color="BRAND",
                color_discrete_sequence=bright_colors,
                height=350,
                text="CORE",
            )
            fig4.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color="#FFFFFF",
                marker_line_width=1.5
            )
            fig4.update_xaxes(tickangle=45)
            fig4.update_layout(
                margin=dict(l=10, r=10, t=30, b=80),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Hostname"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Cores"),
                font=dict(color="#FFFFFF"),
                legend=dict(
                    bgcolor="rgba(0,0,0,0.5)",
                    font=dict(color="#FFFFFF"),
                    title=dict(text="Brand")
                ),
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Row 3: Site Analysis and Device Type
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### 🖥️ Brand Distribution by Site")
            device_site = (
                df_analytics.groupby(["SITE", "BRAND"]).size().reset_index(name="COUNT")
            )
            fig5 = px.bar(
                device_site,
                x="SITE",
                y="COUNT",
                color="BRAND",
                barmode="stack",
                color_discrete_sequence=bright_colors,
                height=350,
                text="COUNT",
            )
            fig5.update_traces(
                texttemplate='%{text}',
                textposition='inside',
                marker_line_color="#FFFFFF",
                marker_line_width=1
            )
            fig5.update_layout(
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Site"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Count"),
                font=dict(color="#FFFFFF"),
                legend=dict(
                    bgcolor="rgba(0,0,0,0.5)",
                    font=dict(color="#FFFFFF"),
                    title=dict(text="Brand")
                ),
            )
            st.plotly_chart(fig5, use_container_width=True)

        with col6:
            st.markdown("#### 🗂️ Server Hierarchy (Site → Rack → Host)")
            fig6 = px.treemap(
                df_analytics,
                path=["SITE", "RACK", "HOSTNAME"],
                color="STATUS",
                color_discrete_map={"Active": "#00E676", "Inactive": "#FF5252"},
                height=350,
            )
            fig6.update_layout(
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF", size=11),
            )
            fig6.update_traces(
                textfont=dict(size=12, color="#FFFFFF"),
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            st.plotly_chart(fig6, use_container_width=True)

        # Row 4: Role and Rack Distribution
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("#### 👔 Role Distribution")
            role_count = df_analytics["ROLE"].value_counts().reset_index()
            role_count.columns = ["ROLE", "COUNT"]
            fig7 = px.pie(
                role_count,
                values="COUNT",
                names="ROLE",
                color_discrete_sequence=bright_colors,
                height=350,
                hole=0.4,
            )
            fig7.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=12,
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            fig7.update_layout(
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=12, color="#FFFFFF"),
            )
            st.plotly_chart(fig7, use_container_width=True)

        with col8:
            st.markdown("#### 🗄️ Top 10 Racks by Device Count")
            rack_count = df_analytics["RACK"].value_counts().head(10).reset_index()
            rack_count.columns = ["RACK", "COUNT"]
            fig8 = px.bar(
                rack_count,
                y="RACK",
                x="COUNT",
                orientation='h',
                color="COUNT",
                color_continuous_scale=[[0, "#4ECDC4"], [0.5, "#45B7D1"], [1, "#FF6B6B"]],
                height=350,
                text="COUNT",
            )
            fig8.update_traces(
                texttemplate='%{text}',
                textposition='auto',
                marker_line_color="#FFFFFF",
                marker_line_width=1.5
            )
            fig8.update_layout(
                showlegend=False,
                margin=dict(l=100, r=10, t=30, b=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Device Count"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title=""),
                font=dict(color="#FFFFFF", size=11),
            )
            st.plotly_chart(fig8, use_container_width=True)

        # Row 5: Status by Site and Site Distribution
        col9, col10 = st.columns(2)
        # Row 5: Status by Site and Site Distribution
        col9, col10 = st.columns(2)
        with col9:
            st.markdown("#### 📍 Status by Site")
            status_site = (
                df_analytics.groupby(["SITE", "STATUS"]).size().reset_index(name="COUNT")
            )
            fig9 = px.bar(
                status_site,
                x="SITE",
                y="COUNT",
                color="STATUS",
                barmode="group",
                color_discrete_map={"Active": "#00E676", "Inactive": "#FF5252"},
                height=350,
                text="COUNT",
            )
            fig9.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color="#FFFFFF",
                marker_line_width=1
            )
            fig9.update_layout(
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Site"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Device Count"),
                font=dict(color="#FFFFFF"),
                legend=dict(
                    bgcolor="rgba(0,0,0,0.5)",
                    font=dict(color="#FFFFFF"),
                    title=dict(text="Status")
                ),
            )
            st.plotly_chart(fig9, use_container_width=True)

        with col10:
            st.markdown("#### 🏢 Device Count by Site")
            site_count = df_analytics["SITE"].value_counts().reset_index()
            site_count.columns = ["SITE", "COUNT"]
            fig10 = px.bar(
                site_count,
                x="SITE",
                y="COUNT",
                color="COUNT",
                color_continuous_scale=[[0, "#4ECDC4"], [0.5, "#45B7D1"], [1, "#FF6B6B"]],
                height=350,
                text="COUNT",
            )
            fig10.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color="#FFFFFF",
                marker_line_width=1.5
            )
            fig10.update_layout(
                showlegend=False,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Site"),
                yaxis=dict(gridcolor="#333333", color="#FFFFFF", title="Device Count"),
                font=dict(color="#FFFFFF"),
            )
            st.plotly_chart(fig10, use_container_width=True)

        # Summary Statistics
        st.markdown("---")
        st.markdown("### 📋 Summary Statistics")
        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        
        with sum_col1:
            unique_brands = df_analytics["BRAND"].nunique()
            st.info(f"**🏷️ Unique Brands:** {unique_brands}")
        
        with sum_col2:
            unique_sites = df_analytics["SITE"].nunique()
            st.info(f"**🏢 Total Sites:** {unique_sites}")
        
        with sum_col3:
            unique_projects = df_analytics["PROJECT"].nunique()
            st.info(f"**📂 Total Projects:** {unique_projects}")
        
        with sum_col4:
            oldest_year = df_analytics["TAHUN_PENGADAAN"].min()
            newest_year = df_analytics["TAHUN_PENGADAAN"].max()
            st.info(f"**📅 Year Range:** {oldest_year} - {newest_year}")
# ===================== FOOTER =====================
st.divider()
st.markdown(
    """
<div style='text-align: center; color: #667eea; padding: 20px;'>
    <p><strong>Dashboard Inventory Server Management</strong> | Auto-refresh every 60 seconds</p>
</div>
""",
    unsafe_allow_html=True,
)
