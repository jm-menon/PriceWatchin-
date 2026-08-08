import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from pqc import SESSIONS
from shared.pqc.crypto import (
    encrypt_payload,
    b64_encode,
)

router = APIRouter()