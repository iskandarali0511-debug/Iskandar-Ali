import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SMART NDVI AI SYSTEM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
    linear-gradient(
        rgba(2,6,23,0.90),
        rgba(2,6,23,0.92)
    ),

    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1920");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =====================================================
FONT
===================================================== */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;
    color: white;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        rgba(2,6,23,0.97),
        rgba(15,23,42,0.97)
    );

    border-right: 1px solid rgba(255,255,255,0.05);
}

/* =====================================================
TITLE
===================================================== */

.main-title {

    text-align:center;

    font-size:70px;

    font-weight:900;

    background:
    linear-gradient(
        90deg,
        #4ade80,
        #22c55e,
        #16a34a
    );

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

    margin-top:20px;
}

.subtitle {

    text-align:center;

    font-size:24px;

    color:#e2e8f0;

    margin-bottom:40px;
}

/* =====================================================
GLASS CARD
===================================================== */

.glass {

    background: rgba(15,23,42,0.72);

    backdrop-filter: blur(12px);

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.08);

    padding:25px;

    margin-bottom:25px;

    box-shadow:
    0 8px 32px rgba(0,255,170,0.10);
}

/* =====================================================
METRIC CARD
===================================================== */

.metric-card {

    background: rgba(30,41,59,0.75);

    border-radius:24px;

    padding:25px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.05);

    box-shadow:
    0 0 25px rgba(0,255,150,0.08);

    transition:0.3s;
}

.metric-card:hover {

    transform: translateY(-5px);

    box-shadow:
    0 0 40px rgba(0,255,150,0.20);
}

.metric-value {

    font-size:42px;

    font-weight:800;

    color:#4ade80;
}

.metric-label {

    font-size:18px;

    color:#cbd5e1;
}

/* =====================================================
SECTION TITLE
===================================================== */

.section-title {

    font-size:34px;

    font-weight:700;

    color:white;

    margin-bottom:20px;
}

/* =====================================================
FOOTER
===================================================== */

.footer {

    text-align:center;

    color:#cbd5e1;

    padding:30px;

    margin-top:40px;

    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
# 🛰️ Upload Sentinel Bands

Upload data Sentinel-2 asli
""")

# =========================================================
# FILE UPLOAD
# =========================================================

b04_file = st.sidebar.file_uploader(
    "Upload Data RED",
    type=["jp2", "tif"]
)

b08_file = st.sidebar.file_uploader(
    "Upload Data NIR",
    type=["jp2", "tif"]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
## 🌱 NDVI Information

🟢 Hijau = Vegetasi sehat

🟡 Kuning = Vegetasi sedang

🔴 Merah = Vegetasi tidak sehat
""")

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class='main-title'>
🛰️ SMART NDVI AI SYSTEM
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Precision Agriculture • GIS Dashboard • Sentinel-2 Analysis
</div>
""", unsafe_allow_html=True)

# =========================================================
# PROCESS NDVI
# =========================================================

if b04_file and b08_file:

    # =====================================================
    # READ FILE
    # =====================================================

    with rasterio.open(b04_file) as src_red:
        red = src_red.read(1).astype('float32')

    with rasterio.open(b08_file) as src_nir:
        nir = src_nir.read(1).astype('float32')

    # =====================================================
    # CLEAN DATA
    # =====================================================

    red = np.nan_to_num(red)
    nir = np.nan_to_num(nir)

    # =====================================================
    # RESIZE DATA AGAR RINGAN
    # =====================================================

    red = red[::3, ::3]
    nir = nir[::3, ::3]

    # =====================================================
    # NDVI
    # =====================================================

    ndvi = (nir - red) / (nir + red + 0.001)

    ndvi = np.clip(ndvi, -1, 1)

    # =====================================================
    # STATISTICS
    # =====================================================

    avg_ndvi = np.nanmean(ndvi)

    max_ndvi = np.nanmax(ndvi)

    min_ndvi = np.nanmin(ndvi)

    healthy = np.sum(ndvi > 0.5)

    medium = np.sum((ndvi > 0.2) & (ndvi <= 0.5))

    unhealthy = np.sum(ndvi <= 0.2)

    pixel_area = 100

    healthy_ha = (healthy * pixel_area) / 10000

    medium_ha = (medium * pixel_area) / 10000

    unhealthy_ha = (unhealthy * pixel_area) / 10000

    total_ha = healthy_ha + medium_ha + unhealthy_ha

    # =====================================================
    # METRIC CARD
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-value'>{avg_ndvi:.2f}</div>
        <div class='metric-label'>Average NDVI</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-value'>{max_ndvi:.2f}</div>
        <div class='metric-label'>Maximum NDVI</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-value'>{min_ndvi:.2f}</div>
        <div class='metric-label'>Minimum NDVI</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-value'>{total_ha:.1f}</div>
        <div class='metric-label'>Total Area (Ha)</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    if avg_ndvi > 0.5:

        status = "🌱 Vegetation detected as HEALTHY"

    elif avg_ndvi > 0.2:

        status = "🌾 Vegetation detected as MODERATE"

    else:

        status = "🍂 Vegetation detected as UNHEALTHY"

    st.markdown(f"""
    <div class='glass'>

    <h2>🤖 AI Vegetation Analysis</h2>

    <h3 style='color:#4ade80;'>{status}</h3>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # VISUALIZATION
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # RED BAND
    # =====================================================

    with col1:

        st.markdown("""
        <div class='glass'>

        <div class='section-title'>
        🔴 RED Band
        </div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(5,5))

        ax.imshow(red, cmap='Reds')

        ax.axis("off")

        st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # NDVI MAP
    # =====================================================

    with col2:

        st.markdown("""
        <div class='glass'>

        <div class='section-title'>
        🌱 NDVI Vegetation Map
        </div>
        """, unsafe_allow_html=True)

        fig2, ax2 = plt.subplots(figsize=(5,5))

        img = ax2.imshow(
            ndvi,
            cmap='RdYlGn',
            vmin=-1,
            vmax=1
        )

        ax2.axis("off")

        cbar = plt.colorbar(img)

        cbar.set_label("NDVI")

        st.pyplot(fig2)

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # HISTOGRAM
    # =====================================================

    st.markdown("""
    <div class='glass'>

    <div class='section-title'>
    📊 NDVI Distribution
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # SAMPLING DATA AGAR TIDAK BERAT
    # =====================================================

    ndvi_flat = ndvi.flatten()

    if len(ndvi_flat) > 100000:

        ndvi_flat = np.random.choice(
            ndvi_flat,
            100000,
            replace=False
        )

    fig_hist = px.histogram(
        x=ndvi_flat,
        nbins=60,
        title="NDVI Histogram"
    )

    fig_hist.update_layout(

        template="plotly_dark",

        paper_bgcolor='rgba(0,0,0,0)',

        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(color='white')
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # AREA STATISTICS
    # =====================================================

    st.markdown("""
    <div class='glass'>

    <div class='section-title'>
    📏 Area Statistics
    </div>
    """, unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)

    with a1:

        st.success(f"""
        🌱 Healthy Area

        {healthy_ha:.2f} Ha
        """)

    with a2:

        st.warning(f"""
        🌾 Moderate Area

        {medium_ha:.2f} Ha
        """)

    with a3:

        st.error(f"""
        🍂 Unhealthy Area

        {unhealthy_ha:.2f} Ha
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.markdown("""
    <div class='glass'>

    <h1 style='text-align:center;
    color:#4ade80;
    font-size:48px;'>

    📂 Upload Sentinel-2 Data

    </h1>

    <p style='text-align:center;
    color:#e2e8f0;
    font-size:22px;'>

    Upload data RED dan NIR
    untuk memulai analisis NDVI

    </p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class='footer'>

SMART NDVI AI SYSTEM • Sentinel-2 • GIS • Precision Agriculture

</div>
""", unsafe_allow_html=True)