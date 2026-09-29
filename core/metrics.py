# Uji Avalanche effect, Entropi, Benchmark

import os
import time
import math
from collections import Counter
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from core.crypto_engine import derive_key, encrypt_aes_gcm, decrypt_aes_gcm

def calculate_entropy(data: bytes) -> float:
    """
    Menghitung entropi Shannon dari sekumpulan byte.
    Skala ideal untuk data acak/terenkripsi adalah mendekati 8.0 bit/byte.
    """
    if not data:
        return 0.0
    
    length = len(data)
    byte_counts = Counter(data)
    entropy = 0.0
    
    for count in byte_counts.values():
        p_x = count / length
        entropy -= p_x * math.log2(p_x)
        
    return round(entropy, 4)

def calculate_byte_histogram(data: bytes) -> list[int]:
    """Menghitung frekuensi kemunculan setiap nilai byte (0-255)."""
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]

def count_bit_differences(bytes1: bytes, bytes2: bytes) -> int:
    """Menghitung jumlah bit yang berbeda (Hamming Distance) antara dua bytes."""
    min_len = min(len(bytes1), len(bytes2))
    diff_bits = 0
    
    for i in range(min_len):
        diff_bits += bin(bytes1[i] ^ bytes2[i]).count('1')
        
    # Tambahkan selisih panjang jika ukuran payload berbeda
    diff_bits += abs(len(bytes1) - len(bytes2)) * 8
    return diff_bits

def calculate_avalanche_effect(plaintext: bytes, password: str, flip_target: str = "plaintext") -> dict:
    """
    Menghitung Avalanche Effect:
    Membalik tepat 1 bit pada plainteks atau kata sandi, lalu mengukur persentase bit cipherteks yang berubah.
    Nilai ideal mendekati 50%.
    """
    fixed_salt = b"avalanche_salt16"
    fixed_nonce = b"aval_nonce12"
    
    # 1. Enkripsi kondisi dasar
    key_base = derive_key(password, fixed_salt)
    aesgcm_base = AESGCM(key_base)
    cipher_base = aesgcm_base.encrypt(fixed_nonce, plaintext, None)
    
    if flip_target == "plaintext":
        # Balik bit ke-0 dari byte ke-0 pada plaintext
        flipped_plaintext = bytearray(plaintext)
        if not flipped_plaintext:
            flipped_plaintext = bytearray(b"\x00")
        flipped_plaintext[0] ^= 0x01
        
        cipher_modified = aesgcm_base.encrypt(fixed_nonce, bytes(flipped_plaintext), None)
        
    elif flip_target == "key":
        # Balik 1 bit pada kata sandi
        pwd_bytes = bytearray(password.encode('utf-8'))
        pwd_bytes[0] ^= 0x01
        modified_pwd = pwd_bytes.decode('utf-8', errors='ignore')
        
        key_modified = derive_key(modified_pwd, fixed_salt)
        aesgcm_mod = AESGCM(key_modified)
        cipher_modified = aesgcm_mod.encrypt(fixed_nonce, plaintext, None)
    else:
        raise ValueError("flip_target harus 'plaintext' atau 'key'")
        
    diff_bits = count_bit_differences(cipher_base, cipher_modified)
    total_bits = len(cipher_base) * 8
    percentage = (diff_bits / total_bits) * 100 if total_bits > 0 else 0.0
    
    return {
        "target": flip_target,
        "total_bits": total_bits,
        "different_bits": diff_bits,
        "avalanche_percentage": round(percentage, 2)
    }

def benchmark_algorithms(sizes_bytes: dict[str, int] = None) -> list[dict]:
    """
    Mengukur waktu enkripsi & dekripsi untuk ukuran berkas tertentu (1 KB, 1 MB, 10 MB)
    serta membandingkan AES-256-GCM vs ChaCha20-Poly1305.
    """
    if sizes_bytes is None:
        sizes_bytes = {
            "1 KB": 1024,
            "1 MB": 1024 * 1024,
            "10 MB": 10 * 1024 * 1024
        }
        
    results = []
    pwd = "BenchmarkPasswordSuperSecure123"
    salt = os.urandom(16)
    key_aes = derive_key(pwd, salt)
    key_chacha = ChaCha20Poly1305.generate_key()
    
    nonce_aes = os.urandom(12)
    nonce_chacha = os.urandom(12)
    
    for label, size in sizes_bytes.items():
        data = os.urandom(size)
        
        # --- Uji AES-256-GCM ---
        aes = AESGCM(key_aes)
        t0 = time.perf_counter()
        enc_aes = aes.encrypt(nonce_aes, data, None)
        t_enc_aes = time.perf_counter() - t0
        
        t0 = time.perf_counter()
        _ = aes.decrypt(nonce_aes, enc_aes, None)
        t_dec_aes = time.perf_counter() - t0
        
        # --- Uji ChaCha20-Poly1305 ---
        chacha = ChaCha20Poly1305(key_chacha)
        t0 = time.perf_counter()
        enc_chacha = chacha.encrypt(nonce_chacha, data, None)
        t_enc_chacha = time.perf_counter() - t0
        
        t0 = time.perf_counter()
        _ = chacha.decrypt(nonce_chacha, enc_chacha, None)
        t_dec_chacha = time.perf_counter() - t0
        
        results.append({
            "Ukuran Berkas": label,
            "Ukuran (Bytes)": size,
            "AES-GCM Enc (detik)": round(t_enc_aes, 5),
            "AES-GCM Dec (detik)": round(t_dec_aes, 5),
            "ChaCha20 Enc (detik)": round(t_enc_chacha, 5),
            "ChaCha20 Dec (detik)": round(t_dec_chacha, 5),
        })
        
    return results