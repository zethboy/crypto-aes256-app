"""
Script untuk mengotomasi pengujian dan menghasilkan berkas 'Data_Pengujian_Kriptografi.xlsx'
sesuai ketentuan luaran proyek:
1. Lembar '10_Masukan_Berbeda': Uji 10 tipe data (termasuk PDF dan gambar).
2. Lembar 'Avalanche_Effect': Uji pembalikan 1 bit pada plainteks dan kunci.
3. Lembar 'Benchmark_Performa': Waktu enkripsi & dekripsi berkas 1 KB, 1 MB, 10 MB (AES-GCM vs ChaCha20).
"""

import os
import hashlib
import pandas as pd
from core.crypto_engine import encrypt_aes_gcm, decrypt_aes_gcm
from core.metrics import calculate_avalanche_effect, benchmark_algorithms

def run_ten_inputs_test():
    ten_inputs = [
        ("1. Teks Pendek ASCII", "text/plain", b"Hello World - Keamanan Informasi 2026"),
        ("2. Teks Panjang Berparagraf", "text/plain", b"Kriptografi modern AES-256-GCM menjamin kerahasiaan dan integritas pesan." * 25),
        ("3. Teks Multibyte & Unicode", "text/utf-8", "Keamanan Informasi Unsil 2026 🔐✨ Sukses!".encode("utf-8")),
        ("4. Berkas PDF Terstruktur", "application/pdf", b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"),
        ("5. Berkas Gambar PNG", "image/png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"),
        ("6. Berkas Gambar BMP", "image/bmp", b"BM" + b"\x00" * 52),
        ("7. Dokumen JSON", "application/json", b'{"project": "CryptoVault", "course": "Information Security", "status": "Pass", "score": 100}'),
        ("8. Berkas Tabel CSV", "text/csv", b"id,name,role\n1,User1,Admin\n2,User2,Operator\n3,User3,Auditor\n"),
        ("9. Biner Acak Berukuran 64 KB", "application/octet-stream", bytes([i % 256 for i in range(64 * 1024)])),
        ("10. Payload Kosong Edge-case", "application/octet-stream", b"")
    ]
    
    pwd = "PengujianDataKripto2026!"
    rows = []
    
    for label, mime, raw_data in ten_inputs:
        enc = encrypt_aes_gcm(raw_data, pwd)
        dec = decrypt_aes_gcm(enc, pwd)
        
        h_orig = hashlib.sha256(raw_data).hexdigest()
        h_dec = hashlib.sha256(dec).hexdigest()
        is_identical = (raw_data == dec) and (h_orig == h_dec)
        
        rows.append({
            "No & Skenario Masukan": label,
            "Tipe MIME": mime,
            "Ukuran Asli (Bytes)": len(raw_data),
            "Ukuran Cipherteks (Bytes)": len(enc),
            "Overhead Metadata (Salt+Nonce+Tag)": f"{len(enc) - len(raw_data)} Bytes",
            "Hash SHA-256 Asli": h_orig,
            "Hash SHA-256 Dekripsi": h_dec,
            "Status Integritas": "VALID (100% Identik)" if is_identical else "GAGAL"
        })
        
    return pd.DataFrame(rows)

def run_avalanche_test():
    sample_text = b"Kriptografi Modern AES-256-GCM Universitas Siliwangi 2026"
    pwd = "PasswordAman123!"
    
    res_p = calculate_avalanche_effect(sample_text, pwd, "plaintext")
    res_k = calculate_avalanche_effect(sample_text, pwd, "key")
    
    rows = [
        {
            "Pengujian Target": "Plainteks (Balik 1 Bit pada Byte Pertama)",
            "Total Bit Cipherteks": res_p["total_bits"],
            "Bit yang Berubah": res_p["different_bits"],
            "Persentase Avalanche (%)": f"{res_p['avalanche_percentage']}%",
            "Analisis Kriptografi": "Pada AES-GCM (mode CTR), pembalikan bit plainteks terlokalisasi pada bit cipherteks terkait dan mendifusi ke 128-bit Authentication Tag (GHASH)."
        },
        {
            "Pengujian Target": "Kunci / Kata Sandi (Balik 1 Bit)",
            "Total Bit Cipherteks": res_k["total_bits"],
            "Bit yang Berubah": res_k["different_bits"],
            "Persentase Avalanche (%)": f"{res_k['avalanche_percentage']}%",
            "Analisis Kriptografi": "Kunci berbeda mendifusi ke seluruh blok keystream AES, menghasilkan avalanche effect ideal mendekati 50%."
        }
    ]
    return pd.DataFrame(rows)

def generate_all_excel():
    output_path = "Data_Pengujian_Kriptografi.xlsx"
    print("Menjalankan pengujian 10 masukan berbeda...")
    df_inputs = run_ten_inputs_test()
    
    print("Menjalankan pengujian avalanche effect...")
    df_avalanche = run_avalanche_test()
    
    print("Menjalankan benchmark performa (1 KB, 1 MB, 10 MB)...")
    bench_data = benchmark_algorithms()
    df_bench = pd.DataFrame(bench_data)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_inputs.to_excel(writer, sheet_name="10_Masukan_Berbeda", index=False)
        df_avalanche.to_excel(writer, sheet_name="Avalanche_Effect", index=False)
        df_bench.to_excel(writer, sheet_name="Benchmark_Performa", index=False)
        
    print(f"Berhasil membuat berkas Excel pengujian: {output_path}")

if __name__ == "__main__":
    generate_all_excel()
