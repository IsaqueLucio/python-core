import base64
from datetime import datetime
from io import BytesIO
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import qrcode
import qrcode.constants

app = FastAPI(title="Pix QR Code Generator")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")


class PixRequest(BaseModel):
    copyPasteCode: str
    expiration: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "JSON de entrada inválido. Certifique-se de informar 'copyPasteCode' e 'expiration' como textos."
        },
    )


def sanitize_pix_code(raw_code: str) -> str:
    """Remove contaminação de sintaxe markdown [codigo](http://...) preservando espaços internos."""
    if not isinstance(raw_code, str):
        return ""
    code = raw_code.strip()
    # Substitui [texto](url) por texto (repete caso haja aninhamento)
    prev = None
    while prev != code:
        prev = code
        code = re.sub(r"\[([^\[\]]*)\]\([^)]*\)", r"\1", code)
    # Remove eventuais trechos (http://...) ou (https://...) remanescentes e colchetes soltos
    code = re.sub(r"\(https?://[^)]*\)", "", code)
    code = code.replace("[", "").replace("]", "")
    # Remove quebras de linha acidentais nas bordas ou meio, preservando espaços normais (" ")
    code = code.replace("\r", "").replace("\n", "").strip()
    return code


def crc16_ccitt(data: str) -> str:
    """Calcula CRC16-CCITT (polinômio 0x1021, valor inicial 0xFFFF)."""
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def validate_pix_code(code: str) -> None:
    """Valida prefixo 000201 e o CRC16-CCITT nos 4 últimos caracteres."""
    if not code:
        raise HTTPException(status_code=400, detail="O código Pix (copyPasteCode) está vazio.")
    if not code.startswith("000201"):
        raise HTTPException(
            status_code=400,
            detail="Código Pix inválido: deve começar com '000201'.",
        )
    if len(code) < 10:
        raise HTTPException(
            status_code=400,
            detail="Código Pix inválido: tamanho insuficiente.",
        )

    payload_without_crc = code[:-4]
    informed_crc = code[-4:].upper()
    calculated_crc = crc16_ccitt(payload_without_crc)

    if informed_crc != calculated_crc:
        raise HTTPException(
            status_code=400,
            detail=f"Código Pix inválido: CRC16 incorreto (esperado {calculated_crc}, recebido {informed_crc}).",
        )


def parse_expiration(expiration_str: str) -> datetime:
    """Interpreta datetime ISO 8601 sem fuso como horário local America/Sao_Paulo."""
    if not isinstance(expiration_str, str) or not expiration_str.strip():
        raise HTTPException(
            status_code=400,
            detail="A data de expiração (expiration) é obrigatória.",
        )

    cleaned = expiration_str.strip()
    if "T" not in cleaned and " " not in cleaned:
        raise HTTPException(
            status_code=400,
            detail="Formato de expiração inválido: informe data e hora em formato ISO 8601 (ex.: 2026-10-28T06:42:13.293).",
        )

    try:
        dt = datetime.fromisoformat(cleaned)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Formato de expiração inválido: use ISO 8601 (ex.: 2026-10-28T06:42:13.293).",
        ) from exc

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SAO_PAULO_TZ)
    else:
        dt = dt.astimezone(SAO_PAULO_TZ)

    return dt


def generate_qr_base64(data: str) -> str:
    """Gera imagem PNG do QR Code em memória (BytesIO) e retorna em Base64."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = TEMPLATES_DIR / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/api/qr")
async def create_qr(payload: PixRequest):
    clean_code = sanitize_pix_code(payload.copyPasteCode)
    validate_pix_code(clean_code)

    expiration_dt = parse_expiration(payload.expiration)
    now_sp = datetime.now(SAO_PAULO_TZ)
    is_expired = now_sp >= expiration_dt

    qr_b64 = generate_qr_base64(clean_code)

    return {
        "qr_png_base64": qr_b64,
        "copy_paste": clean_code,
        "expiration": expiration_dt.isoformat(),
        "expired": is_expired,
    }
