"""
pages/2_Kompresi_SVD.py
------------------------
Halaman fitur: Kompresi Wajah via SVD (power iteration + deflation).
Port fungsional dari section #tool-kompresi di HTML asli.
"""

import io

import numpy as np
import streamlit as st
from PIL import Image

from pixel_style import inject_css, section_header, divider
from pixelface_core import (
    load_image_full,
    to_grayscale,
    svd_compress,
    svd_compress_color,
    SVD_W,
    SVD_H,
    SVD_MAX_K,
)

st.set_page_config(page_title="Kompresi SVD — PixelFace", page_icon="🖼️", layout="wide")
inject_css()

with st.sidebar:
    st.markdown("## 👾 PIXELFACE")
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/1_Deteksi_Kemiripan.py", label="🔍 Pendeteksi Kemiripan Wajah")
    st.page_link("pages/2_Kompresi_SVD.py", label="🖼️ Kompresi Wajah (SVD)")

section_header(
    "✦ COBA SEKARANG",
    "🖼️ KOMPRESI WAJAH",
    "Upload foto wajah, lalu kompresi menggunakan SVD. Pilih mode Grayscale (1 matriks, "
    "lebih hemat) atau Warna (3 matriks R/G/B, hasil tetap berwarna). Atur nilai k untuk "
    "mengontrol kualitas vs ukuran.",
)

if "svd_result" not in st.session_state:
    st.session_state.svd_result = None
if "svd_stats" not in st.session_state:
    st.session_state.svd_stats = None

col_src, col_ctrl, col_out = st.columns([1, 1, 1])

with col_src:
    st.markdown('<span class="pf-label">FOTO ASLI (BERWARNA)</span>', unsafe_allow_html=True)
    file_c = st.file_uploader(
        "Upload foto", type=["png", "jpg", "jpeg", "webp"], key="file_c", label_visibility="collapsed"
    )
    if file_c:
        img_preview = Image.open(file_c)
        st.image(img_preview, use_container_width=True)
        st.caption(f"{img_preview.width}×{img_preview.height}px · {file_c.size / 1024:.1f} KB")

with col_ctrl:
    st.markdown('<span class="pf-label">PENGATURAN SVD</span>', unsafe_allow_html=True)

    st.markdown('<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;">MODE WARNA</span>', unsafe_allow_html=True)
    mode = st.radio(
        "mode",
        options=["Grayscale (1 matriks)", "Warna / RGB (3 matriks)"],
        index=0,
        label_visibility="collapsed",
    )
    is_color = mode.startswith("Warna")
    if is_color:
        st.caption(
            "Mode warna menjalankan SVD terpisah untuk channel R, G, dan B, lalu "
            "menggabungkannya lagi — hasil tetap berwarna, tapi data yang disimpan "
            "3× lebih banyak dibanding mode grayscale untuk nilai k yang sama."
        )
    else:
        st.caption("Mode grayscale hanya menyimpan 1 matriks kecerahan — paling hemat ruang.")

    st.markdown('<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;">NILAI K (KOMPONEN SVD)</span>', unsafe_allow_html=True)
    k_value = st.slider("k", min_value=1, max_value=SVD_MAX_K, value=20, label_visibility="collapsed")
    st.caption(
        f"k kecil = file lebih kecil, kualitas turun · k besar = kualitas lebih baik. "
        f"Maks k={SVD_MAX_K}: di atas titik ini, data hasil SVD (k×(H+W+1) angka) makin "
        f"mendekati lalu melebihi jumlah piksel foto asli (H×W) — bukan kompresi lagi "
        f"namanya kalau hasilnya malah lebih besar."
    )

    stats = st.session_state.svd_stats
    if stats:
        stats_inner = (
            f"Dimensi: {stats['width']}×{stats['height']}<br/>"
            f"Nilai disimpan: {stats['comp_vals']:,}<br/>"
            f"Nilai asli: {stats['orig_vals']:,}<br/>"
            f"Efisiensi: {stats['saved_pct']:.1f}% lebih kecil"
        )
    else:
        stats_inner = "— Belum ada foto —"

    st.markdown(
        '<div class="pf-card-dark">'
        '<span class="pf-label-light" style="font-size:7px;">STATISTIK KOMPRESI</span>'
        f'<div style="font-family:\'VT323\',monospace;font-size:17px;'
        f'color:var(--pink-light);line-height:1.8;">{stats_inner}</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    run_svd = st.button("⚡ KOMPRESI SEKARANG", use_container_width=True)


with col_out:
    out_label = "HASIL KOMPRESI (WARNA)" if is_color else "HASIL KOMPRESI (GRAYSCALE)"
    st.markdown(f'<span class="pf-label">{out_label}</span>', unsafe_allow_html=True)
    if st.session_state.svd_result is not None:
        st.image(st.session_state.svd_result, use_container_width=True)
        result_stats = st.session_state.svd_stats
        mode_badge = "🎨 Warna" if result_stats.get("mode") == "color" else "⚫ Grayscale"
        st.markdown(
            f"**k={result_stats['k']}** · {mode_badge} · Ruang disimpan **{result_stats['saved_pct']:.1f}%**"
        )

        # Tombol download PNG
        buf = io.BytesIO()
        Image.fromarray(st.session_state.svd_result).save(buf, format="PNG")
        st.download_button(
            "💾 DOWNLOAD HASIL",
            data=buf.getvalue(),
            file_name=f"pixelface_svd_k{result_stats['k']}.png",
            mime="image/png",
            use_container_width=True,
        )
    else:
        st.markdown(
            '<div style="background:#eee;border:3px solid var(--pink-dark);'
            'height:240px;display:flex;align-items:center;justify-content:center;'
            'font-family:\'VT323\',monospace;color:#888;">Belum ada hasil</div>',
            unsafe_allow_html=True,
        )

if run_svd:
    if not file_c:
        st.warning("⚠️ Upload foto terlebih dahulu!")
    else:
        spinner_msg = f"⏳ Memproses SVD k={k_value} ({'warna' if is_color else 'grayscale'})... (harap tunggu beberapa detik)"
        with st.spinner(spinner_msg):
            rgb_full = load_image_full(file_c)
            img_pil = Image.fromarray(rgb_full.astype(np.uint8)).resize((SVD_W, SVD_H), Image.LANCZOS)
            rgb_resized = np.array(img_pil, dtype=np.float64)

            if is_color:
                # Mode warna: SVD dijalankan terpisah per channel R/G/B,
                # hasilnya digabung lagi jadi gambar RGB (lihat svd_compress_color()).
                recon, stats = svd_compress_color(rgb_resized, k=k_value, iters=15)
            else:
                # Mode grayscale: foto diratakan ke 1 matriks kecerahan dulu (lihat
                # to_grayscale()), baru di-SVD -- paling hemat ruang.
                gray_matrix = to_grayscale(rgb_resized)
                recon, stats = svd_compress(gray_matrix, k=k_value, iters=15)

            st.session_state.svd_result = recon
            st.session_state.svd_stats = stats
        st.rerun()

divider()

with st.expander("ℹ️ Bagaimana cara kerjanya?"):
    st.markdown(
        f"""
1. Foto di-*resize* ke {SVD_W}×{SVD_H} piksel, lalu dikonversi ke **grayscale**.
2. Matriks piksel didekomposisi memakai **power iteration + deflation** untuk mencari
   k pasangan vektor singular (u, v) dan nilai singular (σ) terbesar — ini setara
   dengan SVD parsial **A ≈ U Σ Vᵗ** tanpa memanggil `numpy.linalg.svd` langsung,
   supaya hasilnya konsisten dengan versi JavaScript aslinya.
3. Gambar direkonstruksi dari k komponen tersebut.
4. Nilai k maksimum dibatasi ke **{SVD_MAX_K}** — di atas itu, data hasil kompresi
   (k×(H+W+1) angka) sudah lebih besar dari foto aslinya (H×W piksel), jadi bukan
   kompresi lagi namanya.
        """
    )
