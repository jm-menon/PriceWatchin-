import requests

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PublicKey,
)

from shared.pqc.crypto import (
    generate_x25519_keypair,
    generate_mlkem_keypair,
    derive_session_key,
    b64_encode,
    b64_decode,
)


def perform_pqc_handshake(base_url):
    """
    Establish a hybrid X25519 + ML-KEM session
    with a vendor simulator.
    """

    # ------------------------------------------------
    # 1. Generate client's X25519 keypair
    # ------------------------------------------------

    x25519_private, x25519_public = (
        generate_x25519_keypair()
    )

    # ------------------------------------------------
    # 2. Generate client's ML-KEM-768 keypair
    # ------------------------------------------------

    kem, mlkem_public = generate_mlkem_keypair()

    # ------------------------------------------------
    # 3. Serialize client's X25519 public key
    # ------------------------------------------------

    x25519_public_bytes = x25519_public.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    # ------------------------------------------------
    # 4. Send both public keys to vendor
    # ------------------------------------------------

    payload = {
        "x25519_public_key": b64_encode(
            x25519_public_bytes
        ),
        "mlkem_public_key": b64_encode(
            mlkem_public
        ),
    }

    response = requests.post(
        f"{base_url}/pqc/pqc-handshake",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    handshake = response.json()

    # ------------------------------------------------
    # 5. Recover vendor's X25519 public key
    # ------------------------------------------------

    server_x25519_public = (
        X25519PublicKey.from_public_bytes(
            b64_decode(
                handshake["x25519_public_key"]
            )
        )
    )

    # ------------------------------------------------
    # 6. Compute X25519 shared secret
    # ------------------------------------------------

    x25519_secret = x25519_private.exchange(
        server_x25519_public
    )

    # ------------------------------------------------
    # 7. Recover ML-KEM shared secret
    # ------------------------------------------------

    mlkem_ciphertext = b64_decode(
        handshake["mlkem_ciphertext"]
    )

    mlkem_secret = kem.decap_secret(
        mlkem_ciphertext
    )

    # ------------------------------------------------
    # 8. Combine both secrets into one session key
    # ------------------------------------------------

    session_key = derive_session_key(
        x25519_secret,
        mlkem_secret,
    )

    return {
        "session_id": handshake["session_id"],
        "session_key": session_key,
    }


def fetch_encrypted_price(
    base_url,
    session_id,
    session_key,
    product_id,
):
    """
    Request an encrypted price from the vendor
    using the established PQC-derived session key.
    """

    response = requests.get(
        f"{base_url}/pqc/encrypted-price/{product_id}",
        headers={
            "X-Session-ID": session_id,
        },
        timeout=10,
    )

    response.raise_for_status()

    encrypted_payload = response.json()

    # TODO:
    # decrypt encrypted_payload using session_key
    #
    # This should eventually return the same structure
    # that fetch_product() returned previously.

    return encrypted_payload