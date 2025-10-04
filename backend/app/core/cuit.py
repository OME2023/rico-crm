import re

_WEIGHTS = [5,4,3,2,7,6,5,4,3,2]

def _checksum(digits11: str) -> int:
    s = sum(int(d)*w for d, w in zip(digits11[:10], _WEIGHTS))
    rem = s % 11
    dv = 11 - rem
    if dv == 11: dv = 0
    elif dv == 10: dv = 9
    return dv

def normalize_cuit(raw: str) -> str | None:
    """Devuelve 'XX-XXXXXXXX-X' si es válido; en caso contrario None."""
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if len(digits) != 11 or not digits.isdigit():
        return None
    dv_calc = _checksum(digits)
    if dv_calc != int(digits[-1]):
        return None
    return f"{digits[0:2]}-{digits[2:10]}-{digits[10]}"

def is_valid_cuit(raw: str) -> bool:
    return normalize_cuit(raw) is not None
