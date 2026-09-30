import os

def create_tampered_file(source_enc_path: str, output_tampered_path: str):
    if not os.path.exists(source_enc_path):
        print(f"Berkas sumber {source_enc_path} tidak ditemukan!")
        return

    # 1. Baca byte berkas terenkripsi asli
    with open(source_enc_path, "rb") as f:
        data = bytearray(f.read())

    if len(data) == 0:
        print("Berkas kosong!")
        return

    # 2. Lakukan simulasi serangan: balik bit pada byte terakhir
    data[-1] ^= 0xFF

    # 3. Simpan sebagai berkas hasil serangan
    with open(output_tampered_path, "wb") as f:
        f.write(data)

    print(f"Sukses membuat berkas hasil serangan:")
    print(f"-> {output_tampered_path}")

if __name__ == "__main__":
    # Contoh mengambil berkas demo PDF terenkripsi
    # Pastikan kamu sudah mengenkripsi satu PDF di Tab 2/Tab 3
    source_file = "RUNDOWN SHARING SESSION.pdf.enc"  # Sesuaikan dengan nama berkas .enc yang ada
    output_file = "RUNDOWN_SHARING_SESSION_TAMPERED.pdf.enc"
    
    # Jika berkas di atas belum ada, gunakan dummy berkas terenkripsi
    if not os.path.exists(source_file):
        from core.crypto_engine import encrypt_aes_gcm
        dummy_enc = encrypt_aes_gcm(b"%PDF-1.4 simulasi dokumen berkas asli", "PasswordDemo123")
        with open("dokumen_asli.pdf.enc", "wb") as f:
            f.write(dummy_enc)
        source_file = "dokumen_asli.pdf.enc"
        output_file = "dokumen_tampered_hasil_serangan.pdf.enc"

    create_tampered_file(source_file, output_file)