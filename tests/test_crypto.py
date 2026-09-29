import sys
from pathlib import Path

# Masukkan folder root proyek ke sys.path agar folder 'core' bisa diimpor dari mana saja
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import unittest
from core.crypto_engine import encrypt_text, decrypt_text, encrypt_aes_gcm, decrypt_aes_gcm
from cryptography.exceptions import InvalidTag

class TestCryptoEngine(unittest.TestCase):
    
    def test_text_encryption_decryption(self):
        """1. Tes kebenaran enkripsi dan dekripsi teks biasa"""
        pesan = "Keamanan Informasi Unsil 2026"
        pwd = "PasswordKuat123!"
        enc = encrypt_text(pesan, pwd, "base64")
        dec = decrypt_text(enc, pwd, "base64")
        self.assertEqual(pesan, dec)

    def test_file_binary_encryption_decryption(self):
        """2. Tes kebenaran enkripsi dan dekripsi data biner/berkas"""
        dummy_data = b"%PDF-1.4 header palsu dan byte biner \x00\xff\xfe"
        pwd = "PasswordRahasia"
        enc = encrypt_aes_gcm(dummy_data, pwd)
        dec = decrypt_aes_gcm(enc, pwd)
        self.assertEqual(dummy_data, dec)

    def test_wrong_password_rejection(self):
        """3. Tes penolakan jika kata sandi salah (harus gagal verifikasi tag)"""
        pesan = "Data Sangat Rahasia"
        enc = encrypt_text(pesan, "PasswordBenar", "hex")
        with self.assertRaises(InvalidTag):
            decrypt_text(enc, "PasswordSalah", "hex")

    def test_tamper_ciphertext_rejection(self):
        """4. Tes penolakan saat 1 byte ciphertext diubah (simulasi manipulasi data)"""
        data = b"Laporan Nilai Mahasiswa"
        pwd = "KunciAman"
        enc = bytearray(encrypt_aes_gcm(data, pwd))
        enc[-1] ^= 0x01
        with self.assertRaises(InvalidTag):
            decrypt_aes_gcm(bytes(enc), pwd)

    def test_unique_nonce_and_salt(self):
        """5. Tes bahwa enkripsi pesan yang sama menghasilkan ciphertext berbeda (salt & nonce acak)"""
        pesan = "Teks Sama"
        pwd = "Password"
        enc1 = encrypt_text(pesan, pwd)
        enc2 = encrypt_text(pesan, pwd)
        self.assertNotEqual(enc1, enc2)

    def test_decrypt_ten_different_inputs(self):
        """6. Tes kebenaran dekripsi pada minimal 10 masukan berbeda (termasuk gambar dan PDF)"""
        import hashlib
        
        ten_inputs = [
            ("1. Teks Pendek ASCII", b"Hello World"),
            ("2. Teks Panjang Berparagraf", b"Kriptografi modern AES-256-GCM menjamin kerahasiaan dan integritas pesan." * 20),
            ("3. Teks Multibyte & Unicode", "Keamanan Informasi Unsil 2026 🔐✨ Sukses!".encode("utf-8")),
            ("4. Berkas PDF Terstruktur", b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"),
            ("5. Berkas Gambar PNG", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"),
            ("6. Berkas Gambar BMP", b"BM" + b"\x00" * 52),
            ("7. Dokumen JSON", b'{"project": "CryptoVault", "course": "Information Security", "score": 100}'),
            ("8. Berkas Tabel CSV", b"id,name,role\n1,User1,Admin\n2,User2,Operator\n"),
            ("9. Biner Acak Berukuran 64 KB", bytes([i % 256 for i in range(64 * 1024)])),
            ("10. Payload Kosong Edge-case", b"")
        ]
        
        test_password = "PasswordPengujian10Masukan!"
        
        for label, original_bytes in ten_inputs:
            with self.subTest(label=label):
                encrypted = encrypt_aes_gcm(original_bytes, test_password)
                decrypted = decrypt_aes_gcm(encrypted, test_password)
                
                # Pastikan data identik
                self.assertEqual(original_bytes, decrypted, f"Gagal mendekripsi: {label}")
                
                # Verifikasi hash SHA-256 sebelum dan sesudah identik 100%
                hash_orig = hashlib.sha256(original_bytes).hexdigest()
                hash_dec = hashlib.sha256(decrypted).hexdigest()
                self.assertEqual(hash_orig, hash_dec, f"Hash SHA-256 tidak cocok pada {label}")

if __name__ == '__main__':
    unittest.main()