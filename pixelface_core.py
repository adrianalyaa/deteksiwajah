"""
pixelface_core.py
------------------
Port 1:1 dari logic JavaScript asli (pixelface_v3_partial_fix.html):
1. pca_similarity()   -> deteksi kemiripan wajah via PCA (eigenvalue 2x2 closed-form)
2. power_iteration()  -> SVD manual via power iteration + deflation
3. Helper grayscale & resize yang menjaga aspect ratio (center-crop),
   sama persis seperti fungsi handleUpload() di JS.

Semua nama variabel & komentar sengaja dibuat paralel dengan versi JS
supaya mudah ditelusuri / di-debug bersama dosen atau tim.
"""

from __future__ import annotations

import numpy as np
from PIL import Image


# ======================================================
# 1. GRAYSCALE & RESIZE HELPERS
# ======================================================

def load_image_centered_square(file, size: int = 100) -> np.ndarray:
    """
    Setara dengan handleUpload() di JS:
    - Ambil sisi terpendek dari foto (center-crop ke persegi)
    - Resize ke (size x size)
    - Kembalikan array RGB uint8 berbentuk (size, size, 3)

    Ini PENTING dipertahankan: tanpa center-crop, foto potret/lanskap
    akan "digepengkan" berbeda-beda saat di-resize, sehingga posisi
    piksel wajah antar dua foto tidak sebanding ketika dibandingkan.
    """
    img = Image.open(file).convert("RGB")
    iw, ih = img.size
    side = min(iw, ih)
    sx = (iw - side) // 2
    sy = (ih - side) // 2
    img_cropped = img.crop((sx, sy, sx + side, sy + side))
    img_resized = img_cropped.resize((size, size), Image.LANCZOS)
    return np.array(img_resized, dtype=np.float64)


def load_image_full(file) -> np.ndarray:
    """Muat foto tanpa crop/resize (dipakai untuk SVD compression source)."""
    img = Image.open(file).convert("RGB")
    return np.array(img, dtype=np.float64)


def to_grayscale(rgb_array: np.ndarray) -> np.ndarray:
    """
    Rumus grayscale standar ITU-R BT.601, identik dengan JS:
    Gray = 0.299*R + 0.587*G + 0.114*B
    """
    r = rgb_array[..., 0]
    g = rgb_array[..., 1]
    b = rgb_array[..., 2]
    return 0.299 * r + 0.587 * g + 0.114 * b


def get_gray_vector(rgb_array: np.ndarray) -> np.ndarray:
    """Flatten matriks grayscale (size,size) jadi vektor 1D panjang size*size."""
    gray = to_grayscale(rgb_array)
    return gray.flatten()


# ======================================================
# 2. PCA SIMILARITY (deteksi kemiripan wajah)
# ======================================================

def pca_similarity(x_a: np.ndarray, x_b: np.ndarray) -> dict:
    """
    Port 1:1 dari fungsi pcaSimilarity() di JS.

    Dua foto = 2 vektor piksel berdimensi tinggi (n).
    Bentuk matriks kovarians 2x2 di "ruang sampel" (trik dual/Gram),
    cari eigenvalue & eigenvector-nya secara eksak (closed-form untuk
    matriks 2x2), lalu hitung skor kemiripan akhir dari cosine similarity
    vektor wajah yang sudah distandarisasi (lihat penjelasan di bawah).
    """
    n = x_a.shape[0]

    # 1. Mean-centering: kurangi setiap vektor dengan rata-ratanya sendiri
    #    (standar pada PCA/Eigenface: setiap wajah dipusatkan sebelum dianalisis)
    mean_a = x_a.mean()
    mean_b = x_b.mean()

    var_a = np.mean((x_a - mean_a) ** 2)
    var_b = np.mean((x_b - mean_b) ** 2)
    std_a = np.sqrt(var_a) or 1.0
    std_b = np.sqrt(var_b) or 1.0

    # 1b. Standardisasi (z-score): menghilangkan pengaruh kecerahan & kontras
    #     kamera yang berbeda, sehingga yang dibandingkan murni
    #     POLA/BENTUK relatif piksel, bukan exposure/pencahayaan.
    a = (x_a - mean_a) / std_a
    b = (x_b - mean_b) / std_b

    # 2. Matriks kovarians C = D Dᵗ / n (ukuran 2x2), elemen = dot product
    #    antar vektor foto yang sudah distandarisasi.
    caa = float(np.dot(a, a)) / n
    cab = float(np.dot(a, b)) / n
    cbb = float(np.dot(b, b)) / n

    # 3. Eigenvalue dari C (2x2) secara eksak:
    #    lambda^2 - (caa+cbb)*lambda + (caa*cbb - cab^2) = 0
    trace = caa + cbb
    det = caa * cbb - cab * cab
    disc = np.sqrt(max(0.0, trace * trace - 4 * det))
    lambda1 = (trace + disc) / 2  # eigenvalue terbesar (variansi PC1)
    lambda2 = (trace - disc) / 2  # eigenvalue terkecil (variansi PC2)

    # 4. Eigenvector PC1 dari C
    w1 = cab
    w2 = lambda1 - caa
    if abs(w1) < 1e-9 and abs(w2) < 1e-9:
        w1, w2 = 1.0, 0.0
    w_norm = np.sqrt(w1 * w1 + w2 * w2)
    w1 /= w_norm
    w2 /= w_norm

    # 5. Rasio energi PC1 -> info PCA saja, TIDAK dipakai untuk skor akhir
    #    (dengan n=2 sampel, PC1 hampir selalu menyerap mayoritas variansi
    #    terlepas dari foto mirip atau tidak -- sifat matematis, bukan
    #    indikator kemiripan yang valid).
    total_var = lambda1 + lambda2
    energy_ratio = (lambda1 / total_var) if total_var > 1e-9 else 1.0

    # 6. Skor kemiripan yang sebenarnya dipakai: cosine similarity antara
    #    dua vektor wajah yang sudah distandarisasi. Ini konsisten dengan
    #    kerangka Eigenface -- proyeksi pada eigenvector PC1 di atas secara
    #    matematis berkaitan langsung dengan cosine antar dua vektor pada
    #    kasus 2 sampel.
    dot = float(np.dot(a, b))
    norm_a = float(np.dot(a, a))
    norm_b = float(np.dot(b, b))
    cosine = dot / (np.sqrt(norm_a) * np.sqrt(norm_b)) if (norm_a > 1e-9 and norm_b > 1e-9) else 0.0

    # 7. Kalibrasi skor: pemetaan linear naif (cosine+1)/2 terlalu "longgar" --
    #    dua foto wajah yang TIDAK berhubungan secara empiris tetap
    #    menghasilkan cosine ~ 0.15-0.20 (bukan ~0), karena foto apa pun
    #    berbagi struktur kasar (area terang di tengah, dst). Sedangkan dua
    #    foto ORANG YANG SAMA secara empiris berada di kisaran 0.55-0.75+.
    #    Floor = 0.35 dipakai sebagai titik tengah (~50%) pembeda dua
    #    kelompok ini.
    floor = 0.35
    if cosine <= floor:
        score = 0.5 * (cosine + 1) / (floor + 1)
    else:
        score = 0.5 + 0.5 * (cosine - floor) / (1 - floor)
    score = max(0.0, min(1.0, score))

    return {
        "score": score,
        "lambda1": lambda1,
        "lambda2": lambda2,
        "w1": w1,
        "w2": w2,
        "energy_ratio": energy_ratio,
        "cosine": cosine,
    }


def similarity_label(score: float) -> str:
    """Setara dengan logic label di runSimilarity() JS."""
    if score >= 0.95:
        return "✨ Sangat Mirip!"
    elif score >= 0.85:
        return "😊 Mirip"
    elif score >= 0.70:
        return "🤔 Cukup Mirip"
    elif score >= 0.50:
        return "😮 Sedikit Mirip"
    else:
        return "❓ Berbeda"


# ======================================================
# 3. SVD COMPRESSION (power iteration + deflation)
# ======================================================

SVD_W = 180
SVD_H = 180

# BATAS NILAI k -- alasan matematisnya (identik dgn komentar JS asli):
# Kompresi rank-k menyimpan k vektor u (panjang H), k vektor v (panjang W),
# dan k nilai singular -> total k*(H+W+1) angka.
# Foto asli (grayscale) menyimpan H*W angka.
# Supaya hasilnya betul-betul "kompresi", harus k*(H+W+1) < H*W, yaitu
# k < (H*W)/(H+W+1). Untuk H=W=180 -> k < 89.75.
# Supaya hasil masih "berarti" (bukan cuma hemat <1%), diberi margin agar
# efisiensi minimal tetap ~10% di nilai k tertinggi:
#     k_max = floor(0.9 * (H*W) / (H+W+1))
# Untuk H=W=180 ini menghasilkan k_max = 80.
SVD_MAX_K = int(np.floor(0.9 * (SVD_W * SVD_H) / (SVD_W + SVD_H + 1)))


def power_iteration(A: np.ndarray, iters: int = 15, rng: np.random.Generator | None = None):
    """
    Port 1:1 dari powerIteration() di JS. Menghitung 1 pasang
    (singular value sigma, vektor u, vektor v) dominan dari matriks A
    via power iteration murni (tanpa numpy.linalg.svd).
    """
    if rng is None:
        rng = np.random.default_rng()

    m, n = A.shape
    v = rng.random(n) - 0.5
    u = np.zeros(m)

    for _ in range(iters):
        u = A @ v
        nu = np.linalg.norm(u)
        if nu < 1e-10:
            break
        u = u / nu

        v = A.T @ u
        nv = np.linalg.norm(v)
        if nv < 1e-10:
            break
        v = v / nv

    sigma = abs(float(u @ A @ v))
    return u, sigma, v


def _svd_reconstruct_single_channel(matrix: np.ndarray, k: int, iters: int, rng: np.random.Generator) -> np.ndarray:
    """
    Inti SVD rank-k untuk SATU matriks 2D (satu channel), via power
    iteration + deflation. Dipakai baik oleh svd_compress() (grayscale)
    maupun svd_compress_color() (RGB, dipanggil 3x per channel).
    """
    H, W = matrix.shape
    A_copy = matrix.copy().astype(np.float64)

    us, ss, vs = [], [], []
    for _ in range(k):
        u, s, v = power_iteration(A_copy, iters=iters, rng=rng)
        us.append(u)
        ss.append(s)
        vs.append(v)
        # deflation: A -= s * outer(u, v)
        A_copy -= s * np.outer(u, v)

    recon = np.zeros((H, W), dtype=np.float64)
    for i in range(k):
        recon += ss[i] * np.outer(us[i], vs[i])

    return recon


def svd_compress(gray_matrix: np.ndarray, k: int, iters: int = 15, seed: int | None = None):
    """
    Port 1:1 dari runSVD() di JS (mode grayscale): hitung k singular
    value/vector terbesar via power iteration + deflation, lalu
    rekonstruksi gambar rank-k dari SATU matriks (grayscale).

    Returns: (reconstructed_uint8_array (H,W), stats_dict)
    """
    rng = np.random.default_rng(seed)
    H, W = gray_matrix.shape

    recon = _svd_reconstruct_single_channel(gray_matrix, k, iters, rng)
    recon_clamped = np.clip(np.round(recon), 0, 255).astype(np.uint8)

    orig_vals = H * W
    comp_vals = k * (H + W + 1)
    saved_pct = max(0.0, (100 - comp_vals / orig_vals * 100))

    stats = {
        "width": W,
        "height": H,
        "comp_vals": comp_vals,
        "orig_vals": orig_vals,
        "saved_pct": saved_pct,
        "k": k,
        "mode": "grayscale",
    }
    return recon_clamped, stats


def svd_compress_color(rgb_array: np.ndarray, k: int, iters: int = 15, seed: int | None = None):
    """
    Mode WARNA: jalankan SVD rank-k secara TERPISAH untuk tiap channel
    (R, G, B), masing-masing diperlakukan sebagai matriks 2D sendiri,
    lalu hasil ketiganya digabung kembali jadi gambar RGB.

    Konsekuensi: karena ada 3 channel, data yang disimpan jadi
    3 * k*(H+W+1) angka (bukan cuma 1x seperti mode grayscale), sehingga
    efisiensi kompresi untuk k yang sama akan lebih rendah dibanding
    mode grayscale -- ini wajar karena kita memang menyimpan informasi
    warna, bukan cuma kecerahan.

    Returns: (reconstructed_uint8_array (H,W,3), stats_dict)
    """
    H, W, _ = rgb_array.shape
    recon_channels = []

    for c in range(3):
        # Seed per-channel dibuat berbeda (tapi tetap reproducible dari
        # seed utama) supaya inisialisasi vektor power iteration tidak
        # identik antar channel.
        channel_seed = None if seed is None else seed + c
        rng = np.random.default_rng(channel_seed)
        channel_matrix = rgb_array[:, :, c]
        recon_c = _svd_reconstruct_single_channel(channel_matrix, k, iters, rng)
        recon_channels.append(recon_c)

    recon_rgb = np.stack(recon_channels, axis=-1)
    recon_clamped = np.clip(np.round(recon_rgb), 0, 255).astype(np.uint8)

    orig_vals = H * W * 3
    comp_vals = 3 * k * (H + W + 1)
    saved_pct = max(0.0, (100 - comp_vals / orig_vals * 100))

    stats = {
        "width": W,
        "height": H,
        "comp_vals": comp_vals,
        "orig_vals": orig_vals,
        "saved_pct": saved_pct,
        "k": k,
        "mode": "color",
    }
    return recon_clamped, stats
