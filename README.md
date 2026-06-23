# 👾 PixelFace (Streamlit Edition)

Port Python/Streamlit dari aplikasi PixelFace (HTML/JS) — deteksi kemiripan wajah
via PCA dan kompresi gambar via SVD (power iteration), dengan styling pixel-pink
yang dipertahankan semirip mungkin dengan versi aslinya.

## Struktur Project

```
pixelface_streamlit/
├── app.py                          # Landing page (hero, fitur, alur, algoritma, tim)
├── pixel_style.py                  # CSS pixel-art shared + komponen UI
├── pixelface_core.py               # Logic inti: PCA similarity & SVD power iteration
├── pages/
│   ├── 1_Deteksi_Kemiripan.py      # Fitur: Pendeteksi Kemiripan Wajah
│   └── 2_Kompresi_SVD.py           # Fitur: Kompresi Wajah via SVD
├── requirements.txt
└── README.md
```

## Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` di browser.

## Deploy ke GitHub + Streamlit Community Cloud

### 1. Push ke GitHub

```bash
cd pixelface_streamlit
git init
git add .
git commit -m "Initial commit: PixelFace Streamlit"
git branch -M main
git remote add origin https://github.com/USERNAME/pixelface-streamlit.git
git push -u origin main
```

### 2. Deploy di Streamlit Community Cloud

1. Buka share.streamlit.io dan login dengan akun GitHub.
2. Klik "New app".
3. Pilih repo pixelface-streamlit, branch main.
4. Main file path: app.py
5. Klik "Deploy".

Streamlit Cloud otomatis membaca requirements.txt dan menginstall semua dependency.

## Catatan Teknis

- Logic PCA similarity (pixelface_core.pca_similarity) dan SVD power iteration
  (pixelface_core.svd_compress) adalah port 1:1 dari kode JavaScript asli, termasuk
  rumus grayscale, standarisasi z-score, eigenvalue closed-form 2x2, kalibrasi skor
  dengan floor 0.35, dan batas k_max untuk kompresi SVD. Ini supaya hasil perhitungan
  konsisten dengan versi web aslinya dan tetap bisa dipertanggungjawabkan secara
  matematis ke dosen.
- Karena power_iteration memakai inisialisasi vektor acak, hasil SVD compression bisa
  sedikit berbeda setiap kali dijalankan (sama seperti versi JS aslinya yang juga pakai
  Math.random()). Ini normal dan tidak mempengaruhi kualitas hasil secara signifikan.
- Font pixel (Press Start 2P, VT323) dimuat dari Google Fonts via @import di CSS;
  pastikan koneksi internet tersedia saat app diakses agar font termuat dengan benar.
