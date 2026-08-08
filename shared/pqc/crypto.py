import base64
import os
import oqs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64


KEM_ALGORITHM = "ML-KEM-768"


def b64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64_decode(data: str) -> bytes:
    return base64.b64decode(data)


def generate_x25519_keypair():
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key


def generate_mlkem_keypair():
    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)

    public_key = kem.generate_keypair()

    return kem, public_key


def derive_session_key(
    x25519_secret: bytes,
    mlkem_secret: bytes,
) -> bytes:

    combined_secret = x25519_secret + mlkem_secret

    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"PriceWatchin-Hybrid-X25519-MLKEM768",
    ).derive(combined_secret)



def encrypt_payload(plaintext: bytes,key: bytes,) -> tuple[bytes, bytes]:
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce,plaintext,None,)
    return ciphertext, nonce

def decrypt_payload(ciphertext: bytes,nonce: bytes,key: bytes,) -> bytes:
    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce,ciphertext,None,)
    return plaintext