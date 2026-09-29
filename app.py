# Antarmuka Web: CryptoVault (AES-256-GCM AEAD)
# Desain: Linear/Vercel Dark Minimalist (Anti AI Slop)

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

st.set_page_config(
    page_title="CryptoVault — AES-256-GCM",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# STYLING: LINEAR / VERCEL MINIMALIST DARK THEME (CLEAN ENGINEERING)
# ==============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset & Base Typography */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #e2e8f0;
}

[data-testid="stAppViewContainer"] {
    background-color: #0b0f17;
    background-image: linear-gradient(180deg, #0f1523 0%, #0b0f17 300px);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Scrollbar Minimal */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0b0f17;
}
::-webkit-scrollbar-thumb {
    background: #1e2638;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #2d3748;
}

/* Header & Meta Panel */
.panel-header {
    background: #111622;
    border: 1px solid #1e2638;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
}

.panel-header-top {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #162032;
    border: 1px solid #233149;
    color: #60a5fa;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.01em;
}

.status-dot {
    width: 6px;
    height: 6px;
    background-color: #3b82f6;
    border-radius: 50%;
}

.panel-title {
    font-size: 1.45rem;
    font-weight: 600;
    color: #f8fafc;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
}

.panel-subtitle {
    color: #94a3b8;
    font-size: 0.88rem;
    line-height: 1.5;
    margin: 0 0 16px 0;
    max-width: 820px;
}

.spec-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding-top: 14px;
    border-top: 1px solid #1a2233;
}

.spec-item {
    background: #0d121c;
    border: 1px solid #1e2638;
    color: #cbd5e1;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Card Minimalist */
.card-box {
    background: #111622;
    border: 1px solid #1e2638;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 16px;
}

.card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0 0 4px 0;
}

.card-desc {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0 0 12px 0;
    line-height: 1.4;
}

/* Tabs Styling - Vercel Flat Style */
[data-testid="stTabs"] {
    background: #0d121c;
    border: 1px solid #1e2638;
    padding: 4px;
    border-radius: 10px;
    margin-bottom: 24px;
}

[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: #94a3b8 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    transition: all 0.15s ease !important;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: #f1f5f9 !important;
    background: #141c2c !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background: #1e2638 !important;
    border: 1px solid #2b374e !important;
    font-weight: 600 !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Inputs & Form Controls */
[data-testid="stTextInput"] input, 
[data-testid="stTextArea"] textarea {
    background: #0d121c !important;
    border: 1px solid #1e2638 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

[data-testid="stTextInput"] input:focus, 
[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #0d121c !important;
    border: 1px solid #1e2638 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-size: 0.85rem !important;
}

/* Buttons - Solid Minimalist */
div.stButton > button {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    background: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    transition: background 0.15s ease, border-color 0.15s ease !important;
    width: 100%;
}

div.stButton > button:hover {
    background: #1d4ed8 !important;
    border-color: #2563eb !important;
}

div.stButton > button:active {
    background: #1e40af !important;
}

/* Download Button - Minimal Dark Slate */
div.stDownloadButton > button {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    background: #15803d !important;
    color: #ffffff !important;
    border: 1px solid #16a34a !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    transition: background 0.15s ease !important;
    width: 100%;
}

div.stDownloadButton > button:hover {
    background: #166534 !important;
}

/* File Uploader Minimal */
[data-testid="stFileUploader"] section {
    background: #0d121c !important;
    border: 1px dashed #26344d !important;
    border-radius: 8px !important;
    padding: 16px !important;
    transition: border-color 0.15s ease !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: #3b82f6 !important;
}

/* Metric Display Minimal */
[data-testid="stMetric"] {
    background: #111622;
    border: 1px solid #1e2638;
    border-radius: 8px;
    padding: 14px;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.35rem !important;
    font-weight: 600 !important;
    color: #60a5fa !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: #94a3b8 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid #1e2638 !important;
    font-size: 0.85rem !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2638;
    border-radius: 8px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# HEADER PANEL (Clean Engineering)
# ==============================================================================
st.markdown("""
<div class="panel-header">
    <div class="panel-header-top">
        <span class="status-badge"><span class="status-dot"></span> NIST SP 800-38D • RFC 5116 Compliant</span>
        <span class="status-badge">PBKDF2-HMAC-SHA256</span>
    </div>
    <div class="panel-title">CryptoVault: AES-256-GCM AEAD System</div>
    <div class="panel-subtitle">
        Modul enkripsi dan dekripsi berkas/teks berbasis Authenticated Encryption with Associated Data (AEAD),
        pengujian metrik kuantitatif, dan perbandingan keamanan mode cipher.
    </div>
    <div class="spec-row">
        <span class="spec-item">Cipher: AES-256 (256-bit Key)</span>
        <span class="spec-item">Mode: GCM (CTR + GHASH)</span>
        <span class="spec-item">Nonce: 96-bit Random (os.urandom)</span>
        <span class="spec-item">Auth Tag: 128-bit</span>
        <span class="spec-item">KDF: 100,000 Iterations + 16B Salt</span>
        <span class="spec-item">Author: Yogi Nugraha (247006111067)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs([
    "Enkripsi & Dekripsi Teks",
    "Enkripsi & Dekripsi Berkas",
    "Skenario Demo UTS",
    "Pengujian & Metrik",
    "Fitur Pengayaan (ECB vs GCM)"
])

# ==============================================================================
# TAB 1: TEKS
# ==============================================================================
with tabs[0]:
    st.subheader("Enkripsi & Dekripsi Teks")
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">Enkripsi Plainteks</div>
            <div class="card-desc">Plainteks dienkripsi dengan AES-256-GCM. Kunci diturunkan via PBKDF2 dengan salt acak 16 byte.</div>
        </div>
        """, unsafe_allow_html=True)
        
        plain_input = st.text_area("Plainteks:", "Rahasia Keamanan Informasi 2026", height=90)
        pwd_enc = st.text_input("Kata Sandi Enkripsi:", type="password", key="pwd_enc_text")
        out_fmt = st.selectbox("Format Output:", ["base64", "hex"])
        
        if st.button("Enkripsi Teks", key="btn_enc_text"):
            if not pwd_enc:
                st.error("Kata sandi tidak boleh kosong.")
            else:
                try:
                    c_text = encrypt_text(plain_input, pwd_enc, out_fmt)
                    st.success("Enkripsi berhasil.")
                    st.text_area("Cipherteks:", c_text, height=120)
                except Exception as e:
                    st.error(f"Kesalahan enkripsi: {e}")

    with col2:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">Dekripsi Cipherteks</div>
            <div class="card-desc">Cipherteks didekripsi dan diverifikasi integritasnya via 128-bit Authentication Tag.</div>
        </div>
        """, unsafe_allow_html=True)
        
        cipher_input = st.text_area("Cipherteks:", height=90)
        pwd_dec = st.text_input("Kata Sandi Dekripsi:", type="password", key="pwd_dec_text")
        in_fmt = st.selectbox("Format Input:", ["base64", "hex"], key="in_fmt_text")
        
        if st.button("Dekripsi Teks", key="btn_dec_text"):
            if not pwd_dec:
                st.error("Kata sandi tidak boleh kosong.")
            else:
                try:
                    p_text = decrypt_text(cipher_input, pwd_dec, in_fmt)
                    st.success("Dekripsi berhasil. Integritas tag terverifikasi.")
                    st.info(f"Plainteks: {p_text}")
                except InvalidTag:
                    st.error("Verifikasi gagal: Kata sandi salah atau data cipherteks telah dimanipulasi (Invalid Tag).")
                except Exception as e:
                    st.error(f"Format cipherteks tidak valid: {e}")

# ==============================================================================
# TAB 2: BERKAS
# ==============================================================================
with tabs[1]:
    st.subheader("Enkripsi & Dekripsi Berkas")
    col_f1, col_f2 = st.columns(2, gap="large")
    
    with col_f1:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">Enkripsi Berkas Biner</div>
            <div class="card-desc">Mendukung berkas PDF, citra, dokumen, atau arsip biner dengan struktur header Salt+Nonce+Tag.</div>
        </div>
        """, unsafe_allow_html=True)
        
        file_to_enc = st.file_uploader("Pilih berkas sumber:", key="upload_enc")
        pwd_f_enc = st.text_input("Kata Sandi Berkas:", type="password", key="pwd_f_enc")
        
        if st.button("Enkripsi Berkas"):
            if file_to_enc and pwd_f_enc:
                raw_bytes = file_to_enc.read()
                encrypted_payload = encrypt_aes_gcm(raw_bytes, pwd_f_enc)
                st.success(f"Berkas berhasil dienkripsi ({len(raw_bytes):,} B -> {len(encrypted_payload):,} B).")
                st.download_button(
                    label="Unduh Berkas Terenkripsi (.enc)",
                    data=encrypted_payload,
                    file_name=f"{file_to_enc.name}.enc",
                    mime="application/octet-stream"
                )
            else:
                st.warning("Unggah berkas dan tentukan kata sandi terlebih dahulu.")

    with col_f2:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">Dekripsi Berkas Terenkripsi</div>
            <div class="card-desc">Memulihkan berkas biner asli setelah otentikasi tag berhasil divalidasi.</div>
        </div>
        """, unsafe_allow_html=True)
        
        file_to_dec = st.file_uploader("Unggah berkas terenkripsi (.enc):", key="upload_dec")
        pwd_f_dec = st.text_input("Kata Sandi Dekripsi:", type="password", key="pwd_f_dec")
        target_name = st.text_input("Nama Berkas Hasil Dekripsi:", "dokumen_pulih.pdf")
        
        if st.button("Dekripsi Berkas"):
            if file_to_dec and pwd_f_dec:
                try:
                    enc_bytes = file_to_dec.read()
                    decrypted_bytes = decrypt_aes_gcm(enc_bytes, pwd_f_dec)
                    st.success("Dekripsi berhasil. Integritas data terverifikasi penuh.")
                    st.download_button(
                        label=f"Unduh Berkas Asli ({target_name})",
                        data=decrypted_bytes,
                        file_name=target_name,
                        mime="application/octet-stream"
                    )
                except InvalidTag:
                    st.error("Dekripsi ditolak: Kata sandi salah atau berkas .enc telah diubah.")
                except Exception as e:
                    st.error(f"Gagal memproses berkas: {e}")

# ==============================================================================
# TAB 3: DEMO RESMI UTS
# ==============================================================================
with tabs[2]:
    st.subheader("Skenario Demo UTS (Alur 7 Menit)")
    st.caption("Prosedur: Enkripsi PDF -> Inspeksi Cipherteks -> Dekripsi Password Benar -> Uji Password Salah -> Uji Tamper 1 Byte.")
    
    col_demo_input, col_demo_stat = st.columns([3, 2], gap="large")
    
    with col_demo_input:
        demo_file = st.file_uploader("1. Dokumen PDF Uji Demo:", type=["pdf"], key="demo_pdf")
        demo_pwd = st.text_input("2. Kata Sandi Pengujian:", value="KriptoUnsil2026!", type="password", key="demo_pwd")
        
    with col_demo_stat:
        if demo_file and demo_pwd:
            pdf_bytes = demo_file.read()
            enc_demo_bytes = encrypt_aes_gcm(pdf_bytes, demo_pwd)
            
            st.markdown(f"""
            <div class="card-box" style="margin-top:24px;">
                <div class="card-title">Metrik Berkas Demo</div>
                <div style="font-size:0.8rem; color:#94a3b8; font-family:'JetBrains Mono', monospace;">
                    Berkas: {demo_file.name}<br>
                    Ukuran Asli: {len(pdf_bytes):,} Bytes<br>
                    Ukuran Cipherteks: {len(enc_demo_bytes):,} Bytes<br>
                    Overhead AEAD: 44 Bytes (Salt 16B + Nonce 12B + Tag 16B)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    if demo_file and demo_pwd:
        st.markdown("#### Inspeksi Cipherteks")
        st.text_area("Cuplikan Heksadesimal (128 Byte Pertama):", enc_demo_bytes[:128].hex() + "...", height=70)
        
        st.markdown("#### Tahapan Uji Skenario")
        col_d1, col_d2, col_d3 = st.columns(3, gap="medium")
        
        with col_d1:
            st.markdown("""
            <div class="card-box">
                <div class="card-title" style="color:#22c55e;">Uji 1: Kata Sandi Benar</div>
                <div class="card-desc">Memulihkan berkas PDF dengan kata sandi yang sesuai.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Dekripsi Normal", key="btn_demo_ok"):
                try:
                    res = decrypt_aes_gcm(enc_demo_bytes, demo_pwd)
                    st.success(f"Sukses: {len(res):,} bytes dipulihkan utuh.")
                except Exception as e:
                    st.error(str(e))
                    
        with col_d2:
            st.markdown("""
            <div class="card-box">
                <div class="card-title" style="color:#eab308;">Uji 2: Kata Sandi Salah</div>
                <div class="card-desc">Menguji penolakan sistem terhadap kata sandi yang salah.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Uji Kata Sandi Salah", key="btn_demo_wrong"):
                try:
                    decrypt_aes_gcm(enc_demo_bytes, "PasswordPastiSalah_12345")
                    st.error("Gagal menolak kata sandi salah.")
                except InvalidTag:
                    st.success("Terverifikasi: Sistem menolak dekripsi (InvalidTag).")
                    
        with col_d3:
            st.markdown("""
            <div class="card-box">
                <div class="card-title" style="color:#ef4444;">Uji 3: Serangan Tamper</div>
                <div class="card-desc">Membalik 1 byte cipherteks untuk simulasi manipulasi data.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Simulasi Tamper (Inversi 1 Byte)", key="btn_demo_tamper"):
                tampered = bytearray(enc_demo_bytes)
                tampered[-1] ^= 0xFF
                try:
                    decrypt_aes_gcm(bytes(tampered), demo_pwd)
                    st.error("Gagal mendeteksi manipulasi data.")
                except InvalidTag:
                    st.success("Integritas Terjaga: Sistem menolak data karena tag otentikasi tidak cocok.")

# ==============================================================================
# TAB 4: PENGUJIAN & METRIK
# ==============================================================================
with tabs[3]:
    st.subheader("Pengujian Metrik Kuantitatif & Benchmark")
    
    # 1. Entropi Shannon & Histogram
    st.markdown("#### 1. Entropi Shannon & Histogram Distribusi Byte")
    sample_text = st.text_area(
        "Teks Sampel Analisis:",
        "Keamanan Informasi Universitas Siliwangi 2026. AES-256-GCM AEAD Mode.",
        key="sample_entropy"
    )
    sample_pwd = "PasswordEntropi123"
    
    if st.button("Hitung Entropi & Histogram"):
        p_bytes = sample_text.encode('utf-8')
        c_bytes = encrypt_aes_gcm(p_bytes, sample_pwd)
        
        h_plain = calculate_entropy(p_bytes)
        h_cipher = calculate_entropy(c_bytes)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Entropi Plainteks", f"{h_plain} bit/byte")
        col_m2.metric("Entropi Cipherteks (AES-GCM)", f"{h_cipher} bit/byte", delta=f"{round(h_cipher - h_plain, 4)} bit/byte")
        st.caption("Catatan: Nilai entropi acak ideal mendekati 8.00 bit/byte. Cipherteks AES-GCM mendekati distribusi seragam.")
        
        # Clean Scientific Plot Minimalist
        fig, axes = plt.subplots(1, 2, figsize=(12, 3.2), facecolor='#0b0f17')
        
        for ax in axes:
            ax.set_facecolor('#111622')
            ax.tick_params(colors='#94a3b8', labelsize=8)
            ax.xaxis.label.set_color('#94a3b8')
            ax.yaxis.label.set_color('#94a3b8')
            ax.title.set_color('#f1f5f9')
            for spine in ax.spines.values():
                spine.set_color('#1e2638')
        
        axes[0].bar(range(256), calculate_byte_histogram(p_bytes), color="#3b82f6", width=1.0)
        axes[0].set_title("Histogram Byte Plainteks", fontsize=10, fontweight='500')
        axes[0].set_xlabel("Nilai Byte (0-255)", fontsize=8)
        axes[0].set_ylabel("Frekuensi", fontsize=8)
        
        axes[1].bar(range(256), calculate_byte_histogram(c_bytes), color="#6366f1", width=1.0)
        axes[1].set_title("Histogram Byte Cipherteks (Distribusi Seragam)", fontsize=10, fontweight='500')
        axes[1].set_xlabel("Nilai Byte (0-255)", fontsize=8)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("---")
    
    # 2. Avalanche Effect
    st.markdown("#### 2. Uji Avalanche Effect")
    col_av1, col_av2 = st.columns(2, gap="large")
    
    with col_av1:
        if st.button("Uji Avalanche: Plainteks (1 Bit)"):
            av_p = calculate_avalanche_effect(b"Contoh plainteks uji avalanche effect untuk praktikum kriptografi", "KunciKuat123", "plaintext")
            st.metric("Avalanche (Plainteks)", f"{av_p['avalanche_percentage']}%", f"{av_p['different_bits']} / {av_p['total_bits']} bit berubah")
            st.caption("Karakteristik Mode CTR: Perubahan 1 bit plainteks terlokalisasi pada bit cipherteks terkait dan mendifusi ke 128-bit Authentication Tag (GHASH).")
            
    with col_av2:
        if st.button("Uji Avalanche: Kunci (1 Bit)"):
            av_k = calculate_avalanche_effect(b"Contoh plainteks uji avalanche effect untuk praktikum kriptografi", "KunciKuat123", "key")
            st.metric("Avalanche (Kunci)", f"{av_k['avalanche_percentage']}%", f"{av_k['different_bits']} / {av_k['total_bits']} bit berubah")
            st.caption("Difusi Kunci: Perubahan 1 bit kunci mendifusi ke seluruh blok keystream AES sehingga menghasilkan avalanche effect mendekati 50%.")

    st.markdown("---")
    
    # 3. Benchmark Performa
    st.markdown("#### 3. Benchmark Performa (AES-256-GCM vs ChaCha20-Poly1305)")
    if st.button("Jalankan Benchmark Performa"):
        with st.spinner("Mengukur throughput enkripsi dan dekripsi..."):
            bench_data = benchmark_algorithms()
            df = pd.DataFrame(bench_data)
            st.dataframe(df, use_container_width=True)
            
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Benchmark")
            output_excel.seek(0)
            
            st.download_button(
                label="Unduh Data Benchmark Format Excel (.xlsx)",
                data=output_excel,
                file_name="Data_Pengujian_Kriptografi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ==============================================================================
# TAB 5: FITUR PENGAYAAN (ECB VS GCM)
# ==============================================================================
with tabs[4]:
    st.subheader("Fitur Pengayaan: Analisis Mode Cipher Citra (ECB vs. GCM)")
    st.markdown("""
    <div class="card-box">
        <div class="card-desc" style="margin-bottom:0;">
            <b>Electronic Codebook (ECB)</b> mengenkripsi blok 16-byte secara deterministik tanpa IV, sehingga blok piksel identik 
            menghasilkan cipherteks identik yang membocorkan siluet visual.<br>
            <b>Galois/Counter Mode (GCM)</b> mengacak seluruh blok data menjadi derau acak menggunakan nonce dinamis dan mode stream CTR.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    img_file = st.file_uploader("Unggah gambar pengujian (format PNG / JPG disarankan):", type=["png", "jpg", "jpeg", "bmp"], key="upload_img_demo")
    
    if img_file:
        img = Image.open(img_file).convert("RGB")
        img_bytes = img.tobytes()
        pwd_img = "DemonstrasiECBAman123"
        
        col_img1, col_img2, col_img3 = st.columns(3, gap="medium")
        
        with col_img1:
            st.markdown("**1. Citra Asli**")
            st.image(img, use_container_width=True)
            
        with col_img2:
            st.markdown("**2. Mode ECB (Kelemahan Visual)**")
            enc_ecb = encrypt_ecb_demo(img_bytes, pwd_img)
            ecb_pixels = enc_ecb[:len(img_bytes)]
            ecb_img = Image.frombytes("RGB", img.size, ecb_pixels)
            st.image(ecb_img, use_container_width=True)
            st.caption("Pola dan siluet objek tetap tampak akibat enkripsi blok deterministik.")
            
        with col_img3:
            st.markdown("**3. Mode Aman AES-GCM (AEAD)**")
            enc_gcm = encrypt_aes_gcm(img_bytes, pwd_img)
            gcm_pixels = enc_gcm[44:44 + len(img_bytes)]
            gcm_img = Image.frombytes("RGB", img.size, gcm_pixels)
            st.image(gcm_img, use_container_width=True)
            st.caption("Teracak sempurna menjadi derau acak tanpa kebocoran pola objek.")