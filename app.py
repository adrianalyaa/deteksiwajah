"""
app.py
------
Halaman utama PixelFace — landing page (hero, fitur, alur program,
detail algoritma, tentang tim, footer).

Jalankan lokal dengan:
    streamlit run app.py

Atau deploy ke Streamlit Community Cloud dengan file ini sebagai
"Main file path".
"""

import streamlit as st
from pixel_style import inject_css, divider, section_header, flow_diagram, math_box, callout

st.set_page_config(
    page_title="PixelFace — Deteksi Kemiripan Wajah",
    page_icon="👾",
    layout="wide",
)

inject_css()

# ============================================================
# SIDEBAR — pengganti navbar
# ============================================================
with st.sidebar:
    st.markdown("## 👾 PIXELFACE")
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/1_Deteksi_Kemiripan.py", label="🔍 Pendeteksi Kemiripan Wajah")
    st.page_link("pages/2_Kompresi_SVD.py", label="🖼️ Kompresi Wajah (SVD)")
    st.markdown("---")
    st.markdown(
        '<span style="font-family:\'VT323\',monospace;font-size:16px;">'
        "Project Aljabar Linear<br/>UNNES Ilmu Komputer</span>",
        unsafe_allow_html=True,
    )

# ============================================================
# HERO
# ============================================================
st.markdown('<span class="pf-eyebrow">✦ PROJECT ALJABAR LINEAR ✦</span>', unsafe_allow_html=True)
st.markdown(
    '<div class="pf-title">PIXELFACE<br/><span>DETEKSI WAJAHMU</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="pf-subtitle">Seberapa mirip kamu dulu dan sekarang? Upload foto masa kecil '
    "& foto sekarang — biarkan algoritma kami menghitungnya untuk kamu. "
    "Powered by linear algebra. 🎮</p>",
    unsafe_allow_html=True,
)

st.write("")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 CEK KEMIRIPAN", use_container_width=True):
        st.switch_page("pages/1_Deteksi_Kemiripan.py")
with col2:
    if st.button("🖼️ KOMPRESI FOTO", use_container_width=True):
        st.switch_page("pages/2_Kompresi_SVD.py")

st.write("")
hc1, hc2, hc3 = st.columns([1, 0.4, 1])
with hc1:
    st.markdown(
        '<div class="pf-card" style="text-align:center;">'
        '<div style="font-size:48px;">🧒</div>'
        '<div class="pf-label" style="margin-top:8px;">FOTO LAMA</div>'
        "</div>",
        unsafe_allow_html=True,
    )
with hc2:
    st.markdown(
        '<div style="text-align:center;font-family:\'Press Start 2P\',monospace;'
        'font-size:18px;color:white;background:var(--pixel-purple);'
        "border:3px solid var(--pixel-black);box-shadow:4px 4px 0 var(--pixel-black);"
        'padding:18px 6px;margin-top:20px;">VS</div>',
        unsafe_allow_html=True,
    )
with hc3:
    st.markdown(
        '<div class="pf-card" style="text-align:center;">'
        '<div style="font-size:48px;">🧑</div>'
        '<div class="pf-label" style="margin-top:8px;">FOTO SEKARANG</div>'
        "</div>",
        unsafe_allow_html=True,
    )

divider()

# ============================================================
# ALUR PROGRAM
# ============================================================
section_header(
    "✦ CARA KERJA PROGRAM",
    "ALUR PROGRAM KAMI",
    "Pilih modul untuk melihat alur kerja lengkap dari masing-masing fitur.",
)

tab1, tab2 = st.tabs(["🔍 PENDETEKSI KEMIRIPAN WAJAH", "🖼️ KOMPRESI WAJAH"])

with tab1:
    callout(
        "📌 Program menerima dua foto wajah — foto masa kecil dan foto masa sekarang. "
        "Sistem mereduksi kedua foto ke ruang eigen menggunakan PCA, lalu mengukur "
        "kemiripan dari proyeksi eigenvector-nya."
    )
    flow_diagram(
        [
            "Upload FOTO MASA KECIL",
            "Upload FOTO MASA SEKARANG",
            "Konversi GRAYSCALE & RESIZE",
            "Ubah jadi VEKTOR PIKSEL",
            "Proyeksi ke EIGENVECTOR (PCA)",
            "OUTPUT: SKOR KEMIRIPAN %",
        ]
    )
    callout(
        "💡 PCA mencari arah (eigenvector) yang menyimpan variasi terbesar dari data "
        "wajah. Setiap foto diproyeksikan ke arah-arah ini, lalu kemiripan diukur dari "
        "jarak antar proyeksinya — semakin dekat, semakin mirip wajahnya!"
    )

with tab2:
    callout(
        "📌 Program menerima satu foto wajah. Sistem mengubahnya ke grayscale lalu "
        "mengkompresi menggunakan SVD sehingga ukuran file berkurang namun kualitas "
        "visual tetap baik."
    )
    flow_diagram(
        [
            "Upload FOTO WAJAH (berwarna)",
            "Konversi ke GRAYSCALE",
            "Ubah jadi MATRIKS PIKSEL m×n",
            "Dekomposisi SVD: U Σ Vᵗ",
            "Ambil k nilai SINGULAR TERBESAR",
            "OUTPUT: FOTO TERKOMPRESI",
        ]
    )
    callout("💡 SVD itu seperti meringkas novel 500 halaman jadi 50 halaman — buang yang kurang penting, inti cerita tetap ada. 📚✂️")

divider()

# ============================================================
# DETAIL ALGORITMA
# ============================================================
section_header(
    "✦ DETAIL ALGORITMA",
    "BAGAIMANA ALGORITMA BEKERJA?",
    "Penjelasan konsep aljabar linear di balik kedua fitur PixelFace.",
)

ac1, ac2 = st.columns(2)

with ac1:
    st.markdown(
        '<div class="pf-card-dark"><span class="pf-label-light">01 — PCA & EIGENVECTOR<br/>PENDETEKSI KEMIRIPAN</span></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown("**LANGKAH 1 — REPRESENTASI VEKTOR**")
        st.caption("Foto wajah diubah jadi array angka (vektor). Foto 100×100 piksel menjadi vektor berdimensi 10.000.")
        math_box("// VEKTOR PIKSEL", "Foto A = [a₁, a₂, ..., aₙ]<br/>Foto B = [b₁, b₂, ..., bₙ]")

        st.markdown("**LANGKAH 2 — MATRIKS KOVARIANS**")
        st.caption("Dari kumpulan vektor wajah, hitung matriks kovarians C. Matriks ini menyimpan informasi tentang variasi piksel antar foto.")
        math_box("// MATRIKS KOVARIANS", "C = (1/n) × Σ (xᵢ − x̄)(xᵢ − x̄)ᵗ<br/>x̄ = rata-rata vektor wajah")

        st.markdown("**LANGKAH 3 — EIGENVALUE & EIGENVECTOR**")
        st.caption('Cari eigenvalue (λ) dan eigenvector (v) dari matriks C. Eigenvector dengan eigenvalue terbesar disebut "eigenface" — arah variasi wajah paling dominan.')
        math_box("// PERSAMAAN KARAKTERISTIK", "C·v = λ·v<br/>det(C − λI) = 0")

        st.markdown("**LANGKAH 4 — PROYEKSI & KEMIRIPAN**")
        st.caption("Kedua foto diproyeksikan ke ruang eigenvector (PCA). Jarak antar hasil proyeksi inilah yang menjadi skor kemiripan — semakin dekat, semakin mirip!")
        math_box("// PROYEKSI PCA", "yᵢ = vᵗ · (xᵢ − x̄)<br/>Skor = f(‖y_A − y_B‖)")

        st.markdown("**🎯 ANALOGI SEDERHANA**")
        st.caption('Eigenvector itu seperti "sumbu utama" wajah — arah di mana wajah-wajah paling berbeda satu sama lain. PCA memetakan setiap foto ke sumbu ini, lalu kita bandingkan posisinya.')

with ac2:
    st.markdown(
        '<div class="pf-card-dark"><span class="pf-label-light">02 — ALGORITMA SVD<br/>KOMPRESI GAMBAR</span></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown("**LANGKAH 1 — GRAYSCALE**")
        st.caption("Foto berwarna (RGB) diubah ke satu nilai kecerahan per piksel.")
        math_box("// RUMUS GRAYSCALE", "Gray = 0.299×R + 0.587×G + 0.114×B")

        st.markdown("**LANGKAH 2 — DEKOMPOSISI SVD**")
        st.caption("Matriks piksel dipecah menjadi 3 komponen: pola baris, tingkat kepentingan, dan pola kolom.")
        math_box("// SVD", "A = U × Σ × Vᵗ")

        st.markdown("**LANGKAH 3 — AMBIL k KOMPONEN**")
        st.caption("Hanya simpan k nilai singular terbesar, lalu rekonstruksi foto. Semakin kecil k = file lebih ringan.")
        math_box(
            "// RANK-k",
            "Aₖ = U[:,:k] × Σ[:k,:k] × Vᵗ[:k,:]<br/>k=10 kecil | k=50 seimbang ✓ | k=80 tinggi",
        )

divider()

# ============================================================
# TENTANG TIM
# ============================================================
section_header("✦ SIAPA KAMI", "TENTANG TIM KAMI")
st.markdown(
    '<p class="pf-section-desc">PixelFace adalah proyek akhir mata kuliah Aljabar Linear, '
    "dikembangkan oleh mahasiswa Program Studi Ilmu Komputer Universitas Negeri Semarang "
    "(UNNES). Proyek ini menggabungkan konsep matematika dengan aplikasi nyata pengolahan "
    "citra digital. 🎓</p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="pf-section-desc">Kami percaya bahwa aljabar linear bukan hanya soal angka '
    "di papan tulis — tapi juga tentang mendeteksi wajah, mengompresi gambar, dan "
    "memecahkan masalah nyata di dunia digital.</p>",
    unsafe_allow_html=True,
)

st.write("")

import base64 as _b64

def _img_b64(path):
    with open(path, "rb") as f:
        return _b64.b64encode(f.read()).decode()

team_data = [
    ("assets/team/team_diar.jpg",     "DIAR ALYA<br/>ADRIANA",       "ENGINEER"),
    ("assets/team/team_zhaafira.jpg", "ZHAAFIRA AFIFAH<br/>PUTRI",   "PENULIS LAPORAN"),
    ("assets/team/team_nadin.jpg",    "NADIN CAHYA<br/>FEBRIANTI",   "PENULIS LAPORAN"),
    ("assets/team/team_fardhan.jpg",  "FARDHAN NAFIISAH<br/>PUTRA",  "RESEARCH"),
]
cols = st.columns(4)
for c, (photo, name, role) in zip(cols, team_data):
    with c:
        b64 = _img_b64(photo)
        st.markdown(
            f'''<div class="pf-team-card">
<img src="data:image/jpeg;base64,{b64}" style="width:100%;aspect-ratio:1/1;object-fit:cover;border:3px solid var(--pink-dark);box-shadow:3px 3px 0 var(--pink-deeper);display:block;margin-bottom:10px;" />
<div class="pf-team-name">{name}</div>
<div class="pf-team-role">{role}</div>
</div>''',
            unsafe_allow_html=True,
        )

st.markdown(
    '<p class="pf-footer">👾 PIXELFACE · © 2025 — Proyek Aljabar Linear · UNNES Ilmu Komputer<br/>'
    "Dibuat dengan 💜 dan banyak matriks</p>",
    unsafe_allow_html=True,
)
