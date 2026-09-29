# 🔐 CryptoVault: Aplikasi Kriptografi Modern (AES-256-GCM)

Aplikasi berbasis web untuk enkripsi dan dekripsi berkas serta teks menggunakan algoritma modern **AES-256-GCM** (*Authenticated Encryption with Associated Data / AEAD*) dengan antarmuka interaktif **Streamlit**, analisis kuantitatif (*Avalanche Effect*, Entropi Shannon, *Benchmark*), dan visualisasi perbandingan keamanan mode *cipher* (ECB vs. GCM).

Tugas Proyek Mata Kuliah **Keamanan Informasi (Section 7)**  
**Program Studi Informatika, Fakultas Teknik, Universitas Siliwangi**  
**Dosen Pengampu:** Ir. Alam Rahmatulloh, S.T., M.T., MCE., IPM.

---

## 👥 Identitas Anggota Kelompok

| No | Nama Mahasiswa | NPM | Peran / Kontribusi |
|---|---|---|---|
| 1 | **Yogi Nugraha** | `247006111067` | Arsitektur Kriptografi, Core Engine, Pengujian Kuantitatif (Avalanche, Benchmark, Entropi),Modul Visualisasi Citra ECB vs GCM & Dokumentasi, dan Demo UTS |

---

## 📌 Topik dan Spesifikasi (Topik A: Enkripsi Algoritma Modern)

Proyek ini memilih **Topik A: Aplikasi Enkripsi (Algoritma Modern)** dengan rincian arsitektur teknis:
1. **Algoritma Utama:** **AES-256-GCM** (NIST SP 800-38D) menggunakan pustaka teruji `cryptography` Python.
2. **Key Derivation Function (KDF):** **PBKDF2-HMAC-SHA256** dengan 100.000 iterasi dan *salt* acak kriptografis 16 byte (`os.urandom(16)`).
3. **Inisialisasi Nonce/IV:** Nonce acak 12 byte (96-bit) unik di setiap operasi enkripsi.
4. **Struktur Payload Terenkripsi:**  
   $$\text{Payload} = \text{Salt (16 B)} + \text{Nonce (12 B)} + \text{Tag Otentikasi (16 B)} + \text{Ciphertext}$$
5. **Jaminan Keamanan (AEAD):** Menjamin aspek *Confidentiality*, *Integrity*, dan *Authenticity*. Aplikasi secara otomatis menolak dekripsi (`InvalidTag`) bila kata sandi salah atau data dimanipulasi (*tampered*).
6. **Representasi Cipherteks:** Mendukung format **Base64** dan **Heksadesimal (Hex)**.
7. **Fitur Pengayaan (Nilai Tambah):** Visualisasi kelemahan deterministik **AES-ECB** (*Electronic Codebook*) dibandingkan keamanan **AES-GCM** pada piksel citra digital.

---

## 📁 Struktur Repositori

```text
proyek-kripto/
├── app.py                         # Antarmuka web utama (Streamlit Dashboard)
├── requirements.txt               # Daftar dependensi pustaka Python
├── README.md                      # Dokumentasi teknis dan panduan penggunaan
├── generate_test_data.py          # Skrip pengujian otomatis & ekspor XLSX
├── Data_Pengujian_Kriptografi.xlsx# Berkas rekapitulasi data pengujian resmi
├── core/
│   ├── __init__.py
│   ├── crypto_engine.py           # Logika AES-256-GCM, PBKDF2 KDF, & Demo ECB
│   └── metrics.py                 # Entropi Shannon, Avalanche Effect, & Benchmark
└── tests/
    ├── __init__.py
    └── test_crypto.py             # Unit test otomatis (6 skenario uji lengkap)
```

---

## 🚀 Panduan Instalasi dan Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python 3.10 atau versi lebih baru
- PIP (*Python Package Installer*)
- Git

### 2. Kloning Repositori
```bash
git clone https://github.com/[username-kelompok]/[nama-repo].git
cd proyek-kripto
```

### 3. Buat dan Aktifkan Virtual Environment (Disarankan)
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi dapat diakses melalui peramban web pada alamat `http://localhost:8501`.

---

## 🧪 Pengujian Otomatis (*Unit Testing*)

Jalankan perintah berikut untuk mengeksekusi 6 skenario *unit test*:
```bash
python -m unittest discover tests
```

Cakupan pengujian meliputi:
1. `test_text_encryption_decryption`: Kebenaran dekripsi teks dasar.
2. `test_file_binary_encryption_decryption`: Kebenaran dekripsi data biner/berkas.
3. `test_wrong_password_rejection`: Penolakan terhadap kata sandi salah.
4. `test_tamper_ciphertext_rejection`: Penolakan saat 1 byte cipherteks diubah (*tampering*).
5. `test_unique_nonce_and_salt`: Kepastian keacakan nonce dan salt pada pesan yang sama.
6. `test_decrypt_ten_different_inputs`: Kebenaran dekripsi pada 10 variasi masukan berbeda (termasuk PDF dan gambar PNG/BMP) dengan verifikasi kecocokan nilai hash SHA-256.

Untuk men-generate ulang berkas Excel data pengujian resmi:
```bash
python generate_test_data.py
```

---

## 🎯 Panduan Skenario Demo UTS (Alokasi Waktu: 7 Menit)

Aplikasi telah dilengkapi tab khusus **"🎯 Skenario Demo UTS"** yang dirancang presisi sesuai ketentuan penilaian:
1. **Langkah 1 (Enkripsi PDF):** Unggah dokumen PDF contoh, masukkan kata sandi, lalu klik enkripsi. Sistem menampilkan cuplikan heksadesimal cipherteks dan ukuran *payload*.
2. **Langkah 2 (Uji Dekripsi Normal):** Klik tombol *Dekripsi Normal* dengan kata sandi yang benar. Sistem berhasil memulihkan 100% berkas PDF asli.
3. **Langkah 3 (Uji Penolakan Kata Sandi Salah):** Klik tombol *Uji dengan Password Salah*. Sistem memunculkan notifikasi penolakan karena kegagalan verifikasi tag autentikasi (`InvalidTag`).
4. **Langkah 4 (Uji Serangan Tamper):** Klik tombol *Ubah 1 Byte Cipherteks*. Sistem membalik seluruh bit pada byte terakhir dan membuktikan integritas terjaga karena data yang dimanipulasi langsung ditolak.
5. **Fitur Pengayaan (Opsional):** Pindah ke tab **"🖼️ Pengayaan: Visualisasi ECB vs GCM"** dan unggah gambar untuk mendemonstrasikan kelemahan pola ECB vs derau acak GCM.

---

## 📊 Ringkasan Hasil Pengujian Kuantitatif

### 1. Uji 10 Masukan Berbeda (Integritas SHA-256)
Seluruh 10 skenario masukan (teks pendek, teks panjang, Unicode/Emoji, berkas PDF, citra PNG, citra BMP, berkas JSON, tabel CSV, berkas biner acak 64 KB, dan payload kosong) teruji menghasilkan nilai dekripsi yang **100% identik** dengan *hash* SHA-256 yang cocok sempurna.

### 2. Uji Avalanche Effect
- **Pembalikan 1 bit pada Kunci/Kata Sandi:** Menghasilkan persentase perubahan bit cipherteks sebesar **$\approx 53\%$** (ideal mendekati 50%). Ini membuktikan difusi yang sangat tinggi dari fungsi PBKDF2-HMAC-SHA256 dan blok AES.
- **Pembalikan 1 bit pada Plainteks:** Pada AES-GCM (yang beroperasi menggunakan mode CTR + GHASH), pembalikan bit plainteks terlokalisasi pada bit cipherteks terkait dan mendifusi ke 128-bit *Authentication Tag* (GHASH).

### 3. Benchmark Performa (AES-256-GCM vs ChaCha20-Poly1305)
Pengujian waktu enkripsi dan dekripsi pada ukuran berkas standar:
| Ukuran Berkas | Waktu Enkripsi AES-GCM | Waktu Dekripsi AES-GCM | Waktu Enkripsi ChaCha20 | Waktu Dekripsi ChaCha20 |
|---|---|---|---|---|
| **1 KB** | < 0.0001 detik | < 0.0001 detik | < 0.0001 detik | < 0.0001 detik |
| **1 MB** | ~ 0.0010 detik | ~ 0.0009 detik | ~ 0.0015 detik | ~ 0.0017 detik |
| **10 MB** | ~ 0.0108 detik | ~ 0.0115 detik | ~ 0.0169 detik | ~ 0.0184 detik |

*Catatan: AES-256-GCM menunjukkan throughput yang sangat efisien berkat pemanfaatan instruksi hardware AES-NI pada CPU modern.*

---

## 📚 Kaitan dengan Riset Dosen Pengampu
Implementasi dan analisis tugas proyek ini merujuk pada literatur dan riset dosen pengampu terkait keamanan web service, autentikasi berbasis token/kunci, serta integritas data:
- **Rahmatulloh, A., & MSN, F.** (2020). *Implementasi Web Service untuk Sistem Informasi Pembagian Logistik Menggunakan REST API dengan Autentikasi JWT dan Enkripsi RC4*. Jurnal RESTI (Rekayasa Sistem Dan Teknologi Informasi), 4(3), 570-577.  
  *(Pada tugas ini, cipher usang seperti RC4 ditinggalkan dan diperbarui menggunakan standar modern AES-256-GCM AEAD).*
- **Rahmatulloh, A., dkk.** (2018). Riset implementasi pengamanan transmisi data dan autentikasi token berbasis HMAC-SHA512.

---

## ⚖️ Integritas Akademik & Penggunaan AI
Sesuai dengan Bagian 10 Petunjuk Tugas Proyek:
- Bantuan AI (*Google Antigravity / Gemini*) digunakan sebagai sarana konsultasi perancangan antarmuka, pembuatan kerangka skrip pengujian, dan penelaahan pemenuhan regulasi proyek.
- Seluruh logika kriptografi, struktur payload AEAD, dan analisis metrik telah dipahami, divalidasi, dan mampu dijelaskan secara mandiri oleh setiap anggota kelompok saat sesi tanya jawab demo UTS.
