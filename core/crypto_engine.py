# Logika AES-256-GCM, KDF, & ECB demo

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.exceptions import InvalidTag

def derive_key(password: str, salt: bytes) -> bytes:
    """Menurunkan kunci 256-bit dari password menggunakan PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_aes_gcm(plaintext: bytes, password: str) -> bytes:
    """
    Enkripsi data biner menggunakan AES-256-GCM.
    Format output: Salt (16B) + Nonce (12B) + Tag (16B) + Ciphertext
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)  # Rekomendasi standar GCM adalah 96-bit (12 bytes)
    key = derive_key(password, salt)
    
    aesgcm = AESGCM(key)
    # AESGCM.encrypt mengembalikan ciphertext + tag di 16 byte terakhir
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, None)
    tag = ciphertext_with_tag[-16:]
    ciphertext = ciphertext_with_tag[:-16]
    
    return salt + nonce + tag + ciphertext

def decrypt_aes_gcm(payload: bytes, password: str) -> bytes:
    """
    Mendekripsi data payload AES-256-GCM.
    Melempar exception jika password salah atau data dimanipulasi.
    """
    if len(payload) < 44:  # 16 (salt) + 12 (nonce) + 16 (tag)
        raise ValueError("Ukuran berkas terenkripsi tidak valid atau rusak.")
    
    salt = payload[:16]
    nonce = payload[16:28]
    tag = payload[28:44]
    ciphertext = payload[44:]
    
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    
    # AESGCM.decrypt butuh ciphertext + tag digabung kembali
    return aesgcm.decrypt(nonce, ciphertext + tag, None)

def encrypt_text(plaintext: str, password: str, output_format: str = "base64") -> str:
    """Enkripsi teks dengan output Base64 atau Heksadesimal."""
    encrypted_bytes = encrypt_aes_gcm(plaintext.encode('utf-8'), password)
    if output_format == "hex":
        return encrypted_bytes.hex()
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_text(ciphertext_str: str, password: str, input_format: str = "base64") -> str:
    """Dekripsi teks dari format Base64 atau Heksadesimal."""
    if input_format == "hex":
        encrypted_bytes = bytes.fromhex(ciphertext_str.strip())
    else:
        encrypted_bytes = base64.b64decode(ciphertext_str.strip())
    
    decrypted_bytes = decrypt_aes_gcm(encrypted_bytes, password)
    return decrypted_bytes.decode('utf-8')

def encrypt_ecb_demo(image_bytes: bytes, password: str) -> bytes:
    """
    Enkripsi khusus demonstrasi kelemahan ECB pada payload piksel/citra.
    (Hanya untuk visualisasi perbandingan di fitur pengayaan).
    """
    salt = b"demo_ecb_salt_16"
    key = derive_key(password, salt)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(image_bytes) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()