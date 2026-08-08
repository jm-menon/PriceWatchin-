import base64
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey,
)

from shared.pqc.crypto import (
    generate_x25519_keypair,
    derive_session_key,
    b64_encode,
    b64_decode,
    KEM_ALGORITHM,
)

import oqs


router = APIRouter()

# Demo-only session storage.
# Do NOT use this approach for a production distributed service.
SESSIONS = {}


class PQCHandshakeRequest(BaseModel):
    x25519_public_key: str
    mlkem_public_key: str


@router.post("/pqc-handshake")
async def pqc_handshake(request: PQCHandshakeRequest):

    # ------------------------------------------------
    # 1. Decode client's public keys
    # ------------------------------------------------

    client_x25519_public = X25519PublicKey.from_public_bytes(
        b64_decode(request.x25519_public_key)
    )

    client_mlkem_public = b64_decode(
        request.mlkem_public_key
    )

    # ------------------------------------------------
    # 2. Generate server ephemeral X25519 keypair
    # ------------------------------------------------

    server_x25519_private, server_x25519_public = (
        generate_x25519_keypair()
    )

    # ------------------------------------------------
    # 3. Perform X25519 ECDH
    # ------------------------------------------------

    x25519_secret = server_x25519_private.exchange(
        client_x25519_public
    )

    # ------------------------------------------------
    # 4. ML-KEM encapsulation
    # ------------------------------------------------

    kem = oqs.KeyEncapsulation(KEM_ALGORITHM)

    ciphertext, mlkem_secret = kem.encap_secret(
        client_mlkem_public
    )

    # ------------------------------------------------
    # 5. Combine both secrets through HKDF
    # ------------------------------------------------

    session_key = derive_session_key(
        x25519_secret,
        mlkem_secret,
    )

    # ------------------------------------------------
    # 6. Create session
    # ------------------------------------------------

    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = session_key

    # ------------------------------------------------
    # 7. Return server X25519 public key + KEM ciphertext
    # ------------------------------------------------

    return {
        "session_id": session_id,
        "x25519_public_key": b64_encode(
            server_x25519_public.public_bytes_raw()
        ),
        "mlkem_ciphertext": b64_encode(ciphertext),
        "algorithm": "X25519 + ML-KEM-768",
    }