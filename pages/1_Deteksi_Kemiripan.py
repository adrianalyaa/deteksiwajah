"""
pages/1_Deteksi_Kemiripan.py
-----------------------------
Halaman fitur: Pendeteksi Kemiripan Wajah via PCA (eigenvalue & eigenvector).
Port fungsional dari section #tool-kemiripan di HTML asli.
"""

import streamlit as st
from PIL import Image

from pixel_style import inject_css, section_header, divider
from pixelface_core import (
    load_image_centered_square,
    get_gray_vector,
    pca_similarity,
    similarity_label,
)

st.set_page_config(page_title="Deteksi Kemiripan — PixelFace", page_icon="🔍", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("## 👾 PIXELFACE")
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/1_Deteksi_Kemiripan.py", label="🔍 Pendeteksi Kemiripan Wajah")
    st.page_link("pages/2_Kompresi_SVD.py", label="🖼️ Kompresi Wajah (SVD)")

section_header(
    "✦ COBA SEKARANG",
    "🔍 PENDETEKSI KEMIRIPAN WAJAH",
    "Upload foto masa kecil & foto sekarang. Algoritma PCA (berbasis eigenvalue & "
    "eigenvector) akan menghitung seberapa mirip kedua wajah secara matematis.",
)

if "sim_result" not in st.session_state:
    st.session_state.sim_result = None

col_a, col_b, col_result = st.columns([1, 1, 1.1])

with col_a:
    st.markdown('<span class="pf-label">FOTO MASA KECIL</span>', unsafe_allow_html=True)
    file_a = st.file_uploader("Upload foto A", type=["png", "jpg", "jpeg", "webp"], key="file_a", label_visibility="collapsed")
    if file_a:
        st.image(file_a, use_container_width=True)
        st.caption(f"{file_a.name} · {file_a.size / 1024:.1f} KB")

with col_b:
    st.markdown('<span class="pf-label">FOTO MASA SEKARANG</span>', unsafe_allow_html=True)
    file_b = st.file_uploader("Upload foto B", type=["png", "jpg", "jpeg", "webp"], key="file_b", label_visibility="collapsed")
    if file_b:
        st.image(file_b, use_container_width=True)
        st.caption(f"{file_b.name} · {file_b.size / 1024:.1f} KB")

with col_result:
    result = st.session_state.sim_result
    score_text = f"{result['score']*100:.2f}%" if result else "—"
    label_text = similarity_label(result["score"]) if result else "Belum dianalisis"

    if result:
        pct = min(result["score"], 1.0) * 100
        progress_html = (
            f'<div class="pf-progress-wrap"><div class="pf-progress-fill" '
            f'style="width:{pct:.1f}%;"></div></div>'
        )
    else:
        progress_html = ""

    st.markdown(
        '<div class="pf-card-dark">'
        '<span class="pf-label-light">HASIL ANALISIS</span>'
        f'<div style="font-family:\'Press Start 2P\',monospace;font-size:34px;'
        f'color:var(--pink);text-align:center;margin:10px 0;">{score_text}</div>'
        f'<div style="font-family:\'VT323\',monospace;font-size:19px;'
        f'color:var(--pink-light);text-align:center;margin-bottom:6px;">{label_text}</div>'
        f"{progress_html}"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    btn1, btn2 = st.columns([2, 1])
    with btn1:
        hitung = st.button("⚡ HITUNG KEMIRIPAN", use_container_width=True)
    with btn2:
        reset = st.button("🔄 RESET", use_container_width=True)


if reset:
    st.session_state.sim_result = None
    st.rerun()

if hitung:
    if not file_a or not file_b:
        st.warning("⚠️ Upload kedua foto terlebih dahulu!")
    else:
        with st.spinner("Menghitung PCA & cosine similarity..."):
            rgb_a = load_image_centered_square(file_a, size=100)
            rgb_b = load_image_centered_square(file_b, size=100)
            vec_a = get_gray_vector(rgb_a)
            vec_b = get_gray_vector(rgb_b)
            result = pca_similarity(vec_a, vec_b)
            st.session_state.sim_result = result
        st.rerun()

# Detail hasil (eigenvalue, eigenvector, cosine) -- setara #sim-detail di JS
if st.session_state.sim_result:
    r = st.session_state.sim_result
    with st.expander("📊 Lihat detail perhitungan PCA", expanded=True):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown(f"**λ₁ (eigenvalue terbesar)** = `{r['lambda1']:.4f}`")
            st.markdown(f"**λ₂ (eigenvalue terkecil)** = `{r['lambda2']:.4f}`")
            st.markdown(f"**Eigenvector PC1** = `[{r['w1']:.4f}, {r['w2']:.4f}]`")
        with d2:
            st.markdown(f"**Rasio energi PC1** = `{r['energy_ratio']*100:.2f}%`")
            st.markdown(f"**Cosine vektor wajah** = `{r['cosine']:.4f}`")
            st.markdown(f"**Skor akhir** = `{r['score']*100:.2f}%`")

divider()

with st.expander("ℹ️ Bagaimana cara kerjanya?"):
    st.markdown(
        """
1. Kedua foto di-**center-crop** ke persegi (menjaga rasio aspek), lalu di-*resize* ke 100×100 piksel.
2. Foto dikonversi ke **grayscale** lalu di-*flatten* jadi vektor 10.000 dimensi.
3. Kedua vektor di-**standarisasi** (z-score) supaya tidak terpengaruh kecerahan/kontras kamera.
4. Dihitung **matriks kovarians 2×2** dan dicari **eigenvalue & eigenvector**-nya secara eksak.
5. Skor akhir didapat dari **cosine similarity** kedua vektor wajah yang sudah distandarisasi,
   dikalibrasi dengan *floor* 0.35 agar foto orang berbeda jatuh di bawah 50% dan foto orang
   yang sama jatuh di atas 50%.
        """
    )
