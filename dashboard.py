import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Analisis Prioritas Pembangunan",
    page_icon="📊",
    layout="wide"
)

import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64("download.png")

st.markdown(f"""
<style>

/* =========================
   BACKGROUND IMAGE (LOCAL)
========================= */
.stApp {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* overlay gelap (AMAN & STABIL) */
.stApp {{
    background-color: rgba(15, 23, 42, 0.65);
    background-blend-mode: darken;
}}

/* =========================
   TEXT GLOBAL
========================= */
p, h1, h2, h3, label {{
    color: white !important;
}}

/* =========================
   SIDEBAR (GLASS STYLE AMAN)
========================= */
[data-testid="stSidebar"] {{
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(6px);
}}

/* =========================
   INPUT FIELD
========================= */
input, textarea {{
    color: black !important;
    background-color: white !important;
}}

.stTextInput input {{
    color: black !important;
    background-color: white !important;
}}

/* =========================
   METRIC CARD
========================= */
div[data-testid="stMetric"] {{
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    transition: 0.2s ease;
}}

div[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
}}

div[data-testid="stMetric"] * {{
    color: black !important;
}}

div[data-testid="stMetricLabel"] {{
    color: #334155 !important;
}}

div[data-testid="stMetricValue"] {{
    color: #0f172a !important;
}}

div[data-testid="stMetricDelta"] {{
    color: #16a34a !important;
}}

/* =========================
   ALERT BOX
========================= */
div[data-testid="stAlert"] {{
    color: white !important;
}}

</style>
""", unsafe_allow_html=True)
# ==========================
# LOAD DATA
# ==========================
df = pd.read_excel("hasil_final_sepi.xlsx")

# ==========================
# JUDUL
# ==========================
st.title("Dashboard Analisis Prioritas Pembangunan Provinsi Indonesia")
st.markdown("### Berdasarkan Data Resmi BPS Tahun 2025")

st.markdown("---")

# ==========================
# KPI
# ==========================
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Jumlah Provinsi",
    f"{len(df)}",
    border=True
)

col2.metric(
    "Rata-rata IPM",
    f"{df['IPM'].mean():.2f}",
    border=True
)

col3.metric(
    "Rata-rata Kemiskinan",
    f"{df['Kemiskinan'].mean():.2f}%",
    border=True
)

prioritas = df.sort_values(
    "SEPI",
    ascending=False
).iloc[0]["Provinsi"]

col4.metric(
    "Prioritas Utama",
    prioritas,
    border=True
)

st.markdown("---")

# ==========================
# SIDEBAR
# ==========================
st.sidebar.header("Filter")

provinsi = st.sidebar.selectbox(
    "Pilih Provinsi",
    df["Provinsi"]
)

data = df[df["Provinsi"]==provinsi]
data = data.iloc[0]

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Detail Provinsi")

st.sidebar.markdown(f"""
<div style="
background:#1B4F8A;
padding:18px;
border-radius:14px;
margin-bottom:18px;
box-shadow:0px 3px 8px rgba(0,0,0,0.25);
">

<h4 style="
margin:0;
color:white;
font-size:18px;">
📍 Provinsi
</h4>

<p style="
margin-top:10px;
font-size:24px;
font-weight:bold;
color:white;">
{provinsi}
</p>

</div>
""", unsafe_allow_html=True)


info = {
    "IPM": f"{data['IPM']:.2f}",
    "Kemiskinan": f"{data['Kemiskinan']:.2f}%",
    "TPT": f"{data['TPT']:.2f}%",
    "PDRB": f"Rp {data['PDRB']:,.0f}",
    "SEPI": f"{data['SEPI']:.3f}",
    "Cluster": f"{int(data['Cluster'])}"
}

for judul, nilai in info.items():

    st.sidebar.markdown(f"""
    <div style="
    background:white;
    border-radius:14px;
    padding:18px;
    margin-bottom:15px;
    box-shadow:0 2px 8px rgba(0,0,0,.15);
    ">

    <div style="
    color:#6b7280;
    font-size:15px;
    font-weight:600;">
    {judul}
    </div>

    <div style="
    color:#123458;
    font-size:34px;
    font-weight:bold;
    margin-top:8px;">
    {nilai}
    </div>

    </div>
    """, unsafe_allow_html=True)

st.subheader("Hubungan IPM dan Kemiskinan")

fig = px.scatter(
    df,
    x="IPM",
    y="Kemiskinan",
    color="Cluster",
    hover_name="Provinsi",
    template="plotly_dark"
)

fig.update_layout(
    font=dict(color="white"),
    title_x=0.5,
    legend_title="Cluster",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
fig.update_xaxes(title_font=dict(color="white"), tickfont=dict(color="white"))
fig.update_yaxes(title_font=dict(color="white"), tickfont=dict(color="white"))

st.plotly_chart(fig, use_container_width=True)

st.subheader("Hubungan PDRB dan Kemiskinan")

fig = px.scatter(
    df,
    x="PDRB",
    y="Kemiskinan",
    color="Cluster",
    hover_name="Provinsi",
    template="plotly_dark"
)

fig.update_layout(
    font=dict(color="white"),
    title_x=0.5,
    legend_title="Cluster",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
fig.update_xaxes(title_font=dict(color="white"), tickfont=dict(color="white"))
fig.update_yaxes(title_font=dict(color="white"), tickfont=dict(color="white"))

st.plotly_chart(fig, use_container_width=True)

st.subheader("Visualisasi Cluster Provinsi")

fig = px.scatter(
    df,
    x="IPM",
    y="SEPI",
    color="Cluster",
    size="PDRB",
    hover_name="Provinsi",
    template="plotly_dark"
)

fig.update_layout(
    font=dict(color="white"),
    title_x=0.5,
    legend_title="Cluster",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

fig.update_xaxes(title_font=dict(color="white"), tickfont=dict(color="white"))
fig.update_yaxes(title_font=dict(color="white"), tickfont=dict(color="white"))

st.plotly_chart(fig, use_container_width=True)

st.subheader("10 Prioritas Pembangunan")

top10 = df.sort_values(
    "SEPI",
    ascending=False
).head(10)[["Provinsi", "SEPI", "Cluster"]]

# ==========================
# Grafik Ranking
# ==========================
fig = px.bar(
    top10,
    x="SEPI",
    y="Provinsi",
    orientation="h",
    color="Cluster",
    text="SEPI",
    template="plotly_dark",
    title="Ranking 10 Provinsi Prioritas Pembangunan"
)

fig.update_layout(
    font=dict(color="white"),
    title_x=0.5,
    legend_title="Cluster",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

fig.update_xaxes(title_font=dict(color="white"), tickfont=dict(color="white"))
fig.update_yaxes(title_font=dict(color="white"), tickfont=dict(color="white"))

st.plotly_chart(fig, use_container_width=True)

# ==========================
# Tabel
# ==========================
st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True
)

st.subheader("Kesimpulan Analisis")

st.markdown(f"""
<div style="
background-color:#1e293b;
padding:18px;
border-radius:12px;
color:white;
line-height:1.6;
">

<b>Provinsi dengan prioritas pembangunan tertinggi adalah {prioritas}</b><br>
berdasarkan nilai SEPI terbesar.<br><br>

Analisis dilakukan menggunakan metode K-Means Clustering terhadap indikator:<br>

- IPM  
- Kemiskinan  
- Tingkat Pengangguran Terbuka  
- PDRB per kapita  

<br>
Semakin tinggi nilai SEPI, semakin tinggi prioritas pembangunan provinsi tersebut.

</div>
""", unsafe_allow_html=True)

st.subheader("📋 Data Lengkap")

with st.expander("Klik untuk melihat seluruh data"):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

st.caption(
    "Dashboard dibuat menggunakan Python • Streamlit • Pandas • Scikit-Learn • Matplotlib | Data BPS 2025"
)

