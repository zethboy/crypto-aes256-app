# Antarmuka Web (Streamlit)

import streamlit as st
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from core.crypto_engine import (
    encrypt_text, decrypt_text,
    encrypt_aes_gcm, decrypt_aes_gcm,
    encrypt_ecb_demo
)
from core.metrics import (
    calculate_entropy, calculate_byte_histogram,
    calculate_avalanche_effect, benchmark_algorithms
)
from cryptography.exceptions import InvalidTag

st.set_page_config(page_title="CryptoVault - AES-256-GCM Modern", page_icon="🔐", layout="wide")

st.title("🔐 CryptoVault: Aplikasi Kriptografi Modern (AES-256-GCM)")
st.caption("Implementasi Enkripsi Terotentikasi (AEAD), Analisis Kuantitatif, dan Demonstrasi Keamanan Mode Cipher")

tabs = st.tabs([
    "📝 Enkripsi/Dekripsi Teks",
    "📁 Enkripsi/Dekripsi Berkas",
    "🎯 Skenario Demo UTS",
    "📊 Pengujian & Metrik",
    "🖼️ Pengayaan: Visualisasi ECB vs GCM"
])

# ==========================================
# TAB 1: TEKS
# ==========================================
with tabs[0]:
    st.subheader("Enkripsi & Dekripsi Teks")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Proses Enkripsi")
        plain_input = st.text_area("Masukkan Plainteks:", "Rahasia Keamanan Informasi 2026")
        pwd_enc = st.text_input("Kata Sandi Enkripsi:", type="password", key="pwd_enc_text")
        out_fmt = st.selectbox("Format Output:", ["base64", "hex"])
        
        if st.button("Enkripsi Teks", key="btn_enc_text"):
            if not pwd_enc:
                st.error("Kata sandi tidak boleh kosong!")
            else:
                try:
                    c_text = encrypt_text(plain_input, pwd_enc, out_fmt)
                    st.success("Teks berhasil dienkripsi!")
                    st.text_area("Cipherteks:", c_text, height=120)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    with col2:
        st.markdown("#### Proses Dekripsi")
        cipher_input = st.text_area("Masukkan Cipherteks:")
        pwd_dec = st.text_input("Kata Sandi Dekripsi:", type="password", key="pwd_dec_text")
        in_fmt = st.selectbox("Format Input:", ["base64", "hex"], key="in_fmt_text")
        
        if st.button("Dekripsi Teks", key="btn_dec_text"):
            if not pwd_dec:
                st.error("Kata sandi tidak boleh kosong!")
            else:
                try:
                    p_text = decrypt_text(cipher_input, pwd_dec, in_fmt)
                    st.success("Teks berhasil didekripsi!")
                    st.info(f"Hasil: {p_text}")
                except InvalidTag:
                    st.error("❌ Verifikasi Gagal! Kata sandi salah atau data cipherteks telah dimanipulasi.")
                except Exception as e:
                    st.error(f"Format cipherteks tidak valid: {e}")

# ==========================================
# TAB 2: BERKAS
# ==========================================
with tabs[1]:
    st.subheader("Enkripsi & Dekripsi Berkas (PDF, Dokumen, Gambar)")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("#### Enkripsi Berkas")
        file_to_enc = st.file_uploader("Pilih berkas untuk dienkripsi:", key="upload_enc")
        pwd_f_enc = st.text_input("Kata Sandi Berkas:", type="password", key="pwd_f_enc")
        
        if st.button("Enkripsi Berkas"):
            if file_to_enc and pwd_f_enc:
                raw_bytes = file_to_enc.read()
                encrypted_payload = encrypt_aes_gcm(raw_bytes, pwd_f_enc)
                st.success(f"Berkas berhasil dienkripsi! Ukuran awal: {len(raw_bytes)} bytes -> Terenkripsi: {len(encrypted_payload)} bytes")
                st.download_button(
                    label="💾 Unduh Berkas Terenkripsi (.enc)",
                    data=encrypted_payload,
                    file_name=f"{file_to_enc.name}.enc",
                    mime="application/octet-stream"
                )
            else:
                st.warning("Unggah berkas dan masukkan kata sandi terlebih dahulu.")

    with col_f2:
        st.markdown("#### Dekripsi Berkas")
        file_to_dec = st.file_uploader("Unggah berkas .enc:", key="upload_dec")
        pwd_f_dec = st.text_input("Kata Sandi Dekripsi:", type="password", key="pwd_f_dec")
        target_name = st.text_input("Simpan nama berkas hasil dekripsi sebagai:", "hasil_dekripsi.pdf")
        
        if st.button("Dekripsi Berkas"):
            if file_to_dec and pwd_f_dec:
                try:
                    enc_bytes = file_to_dec.read()
                    decrypted_bytes = decrypt_aes_gcm(enc_bytes, pwd_f_dec)
                    st.success("Berkas berhasil didekripsi dan integritas terverifikasi!")
                    st.download_button(
                        label="💾 Unduh Berkas Asli",
                        data=decrypted_bytes,
                        file_name=target_name,
                        mime="application/octet-stream"
                    )
                except InvalidTag:
                    st.error("❌ Dekripsi Ditolak! Kata sandi salah atau berkas .enc rusak/diubah.")
                except Exception as e:
                    st.error(f"Gagal memproses berkas: {e}")

# ==========================================
# TAB 3: DEMO RESMI UTS
# ==========================================
with tabs[2]:
    st.subheader("🎯 Skenario Wajib Demo UTS (7 Menit)")
    st.info("Alur Wajib: Enkripsi PDF -> Tunjukkan Cipherteks -> Dekripsi Kata Sandi Benar -> Uji Password Salah -> Uji Tamper 1 Byte")
    
    demo_file = st.file_uploader("1. Unggah Dokumen PDF untuk Uji Demo:", type=["pdf"], key="demo_pdf")
    demo_pwd = st.text_input("2. Buat Kata Sandi Demo:", value="KriptoUnsil2026!", type="password", key="demo_pwd")
    
    if demo_file and demo_pwd:
        pdf_bytes = demo_file.read()
        enc_demo_bytes = encrypt_aes_gcm(pdf_bytes, demo_pwd)
        
        st.markdown("---")
        st.write(f"**Ukuran Berkas PDF Asli:** {len(pdf_bytes)} bytes | **Ukuran Cipherteks:** {len(enc_demo_bytes)} bytes")
        st.text_area("Cuplikan Cipherteks (Format Hex 128 byte pertama):", enc_demo_bytes[:128].hex() + "...", height=80)
        
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            st.markdown("##### Uji 1: Kata Sandi Benar")
            if st.button("Jalankan Dekripsi Normal"):
                try:
                    res = decrypt_aes_gcm(enc_demo_bytes, demo_pwd)
                    st.success(f"✅ Sukses! {len(res)} bytes dipulihkan utuh.")
                except Exception as e:
                    st.error(str(e))
                    
        with col_d2:
            st.markdown("##### Uji 2: Kata Sandi Salah")
            if st.button("Uji dengan Password Salah"):
                try:
                    decrypt_aes_gcm(enc_demo_bytes, "PasswordYangPastiSalah123")
                    st.error("Gagal menolak kata sandi salah!")
                except InvalidTag:
                    st.success("✅ Terverifikasi: Aplikasi menolak dekripsi (Invalid Tag Authentication).")
                    
        with col_d3:
            st.markdown("##### Uji 3: Serangan Tamper (Ubah 1 Byte)")
            if st.button("Ubah 1 Byte Cipherteks"):
                tampered = bytearray(enc_demo_bytes)
                tampered[-1] ^= 0xFF  # Membalik seluruh bit pada byte terakhir
                try:
                    decrypt_aes_gcm(bytes(tampered), demo_pwd)
                    st.error("Gagal mendeteksi tampering!")
                except InvalidTag:
                    st.success("✅ Integritas Terjaga: Sistem menolak data karena tag autentikasi tidak valid.")

# ==========================================
# TAB 4: PENGUJIAN & METRIK
# ==========================================
with tabs[3]:
    st.subheader("Analisis Kuantitatif & Benchmark Metrik")
    
    st.markdown("#### 1. Entropi Shannon & Histogram Distribusi Byte")
    sample_text = st.text_area("Teks Sampel untuk Analisis Entropi:", "Keamanan Informasi Universitas Siliwangi 2026. AES-256-GCM AEAD Mode.", key="sample_entropy")
    sample_pwd = "PasswordEntropi123"
    
    if st.button("Hitung Entropi & Tampilkan Histogram"):
        p_bytes = sample_text.encode('utf-8')
        c_bytes = encrypt_aes_gcm(p_bytes, sample_pwd)
        
        h_plain = calculate_entropy(p_bytes)
        h_cipher = calculate_entropy(c_bytes)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Entropi Plainteks", f"{h_plain} bit/byte")
        col_m2.metric("Entropi Cipherteks (AES-GCM)", f"{h_cipher} bit/byte", delta=f"{round(h_cipher - h_plain, 4)}")
        st.caption("Entropi acak ideal mendekati 8.00 bit/byte. Nilai tinggi menunjukkan data seragam tanpa pola redundan.")
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 3))
        axes[0].bar(range(256), calculate_byte_histogram(p_bytes), color="tab:blue")
        axes[0].set_title("Histogram Byte Plainteks")
        axes[0].set_xlabel("Nilai Byte (0-255)")
        axes[0].set_ylabel("Frekuensi")
        
        axes[1].bar(range(256), calculate_byte_histogram(c_bytes), color="tab:red")
        axes[1].set_title("Histogram Byte Cipherteks (Mendekati Uniform)")
        axes[1].set_xlabel("Nilai Byte (0-255)")
        
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 2. Uji Avalanche Effect")
    col_av1, col_av2 = st.columns(2)
    with col_av1:
        if st.button("Uji Avalanche: Balik 1 Bit pada Plainteks"):
            av_p = calculate_avalanche_effect(b"Contoh plainteks uji avalanche effect untuk praktikum kriptografi", "KunciKuat123", "plaintext")
            st.metric("Persentase Avalanche (Plainteks)", f"{av_p['avalanche_percentage']}%", f"{av_p['different_bits']} dari {av_p['total_bits']} bit berubah")
            st.info("ℹ️ **Analisis Mode CTR:** Pada AES-GCM, enkripsi beroperasi sebagai stream cipher (CTR mode). Pembalikan 1 bit plainteks terlokalisasi pada bit cipherteks terkait dan mendifusi ke 128-bit Authentication Tag (GHASH).")
    with col_av2:
        if st.button("Uji Avalanche: Balik 1 Bit pada Kunci/Kata Sandi"):
            av_k = calculate_avalanche_effect(b"Contoh plainteks uji avalanche effect untuk praktikum kriptografi", "KunciKuat123", "key")
            st.metric("Persentase Avalanche (Kunci/Kata Sandi)", f"{av_k['avalanche_percentage']}%", f"{av_k['different_bits']} dari {av_k['total_bits']} bit berubah")
            st.success("✅ **Difusi Kunci Ideal:** Perubahan 1 bit kunci mendifusi ke seluruh blok keystream AES sehingga menghasilkan avalanche effect mendekati 50%.")


    st.markdown("---")
    st.markdown("#### 3. Benchmark Perbandingan Waktu: AES-GCM vs ChaCha20-Poly1305 (1 KB, 1 MB, 10 MB)")
    if st.button("Jalankan Benchmark (1 KB, 1 MB, 10 MB)"):
        with st.spinner("Menjalankan pengujian performa..."):
            bench_data = benchmark_algorithms()
            df = pd.DataFrame(bench_data)
            st.dataframe(df)
            
            # Siapkan ekspor Excel XLSX
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Benchmark")
            output_excel.seek(0)
            
            st.download_button(
                label="📥 Unduh Data Pengujian (.xlsx)",
                data=output_excel,
                file_name="Data_Pengujian_Kriptografi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ==========================================
# TAB 5: FITUR PENGAYAAN (ECB VS GCM)
# ==========================================
with tabs[4]:
    st.subheader("🖼️ Fitur Pengayaan: Perbandingan Mode ECB vs Mode Aman (GCM)")
    st.write(
        "Mode **Electronic Codebook (ECB)** mengenkripsi setiap blok 16 byte secara independen tanpa IV. "
        "Akibatnya, blok plainteks yang identik menghasilkan blok cipherteks yang identik, sehingga pola/siluet gambar masih terlihat. "
        "Mode **Galois/Counter Mode (GCM)** mengacak seluruh blok dan menyertakan tag integritas autentikasi."
    )
    
    img_file = st.file_uploader("Unggah gambar pengujian (format PNG disarankan):", type=["png", "jpg", "jpeg", "bmp"], key="upload_img_demo")
    
    if img_file:
        img = Image.open(img_file).convert("RGB")
        img_bytes = img.tobytes()
        pwd_img = "DemonstrasiECBAman123"
        
        col_img1, col_img2, col_img3 = st.columns(3)
        with col_img1:
            st.markdown("**Citra Asli**")
            st.image(img, use_container_width=True)
            
        with col_img2:
            st.markdown("**Hasil Mode ECB (Pola Bocor)**")
            enc_ecb = encrypt_ecb_demo(img_bytes, pwd_img)
            # Potong ke panjang byte piksel asli untuk rendering
            ecb_pixels = enc_ecb[:len(img_bytes)]
            ecb_img = Image.frombytes("RGB", img.size, ecb_pixels)
            st.image(ecb_img, use_container_width=True)
            st.caption("Pola dan siluet objek masih terlihat karena deterministik per blok.")
            
        with col_img3:
            st.markdown("**Hasil Mode Aman AES-GCM (Derau Acak)**")
            enc_gcm = encrypt_aes_gcm(img_bytes, pwd_img)
            gcm_pixels = enc_gcm[44:44 + len(img_bytes)]
            gcm_img = Image.frombytes("RGB", img.size, gcm_pixels)
            st.image(gcm_img, use_container_width=True)
            st.caption("Pola teracak sempurna menjadi white noise tanpa bocoran visual.")