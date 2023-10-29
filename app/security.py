from abc import ABC
from json import loads

from fastapi import Header
from jose import jwt
from loguru import logger
from requests import get

from app.config import config
from app.exceptions import CustomError


class Principal(ABC):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"<Principal name={self.name}>"


class ApiPrincipal(Principal):
    def __init__(self):
        super().__init__("API")


class JwtPrincipal(Principal):
    def __init__(self, claims: dict):
        super().__init__("JWT")
        self.claims = claims

    def __repr__(self) -> str:
        return f"<Principal name={self.name}>: {self.claims}"


class LocalPrincipal(Principal):
    def __init__(self):
        super().__init__("LOCAL")


def _get_rsa_key(jwks: dict, unverified_header: dict) -> dict | None:
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    return None


def _decode_jwt(unverified_token: str) -> dict:
    response = get(config["JWKS_URL"], timeout=10)
    jwks = loads(response.text)

    unverified_header = jwt.get_unverified_header(unverified_token)
    rsa_key = _get_rsa_key(jwks, unverified_header)

    if not rsa_key:
        logger.error("Authentication Exception: RSA key not found")
        raise CustomError(401, "UNAUTHORIZED")

    try:
        payload = jwt.decode(
            unverified_token,
            rsa_key,
            algorithms=config["JWT_ALGORITHMS"],
            audience=config["JWT_AUDIENCE"],
            issuer=config["JWT_ISSUER"],
        )
        return payload[f"https://{config['AUTH_DOMAIN']}/metadata"]
    except jwt.ExpiredSignatureError as exception:
        logger.error("Authentication Exception: Expired signature")
        raise CustomError(401, "UNAUTHORIZED") from exception
    except jwt.JWTClaimsError as exception:
        logger.error("Authentication Exception: Invalid claims")
        raise CustomError(401, "UNAUTHORIZED") from exception
    except Exception as exception:
        logger.error("Authentication Exception: Unspecified error")
        raise CustomError(401, "UNAUTHORIZED") from exception


def authorization(
    api_key: str = Header(None),
    authorization: str = Header(None),
) -> Principal:
    """Check for Api-Key header or JWT in the Authorization header as fallback."""
    if config["STAGE"] == "LOCAL":
        return LocalPrincipal()

    if api_key is not None and api_key == config["API_KEY"]:
        return ApiPrincipal()

    if authorization is None:
        logger.error("Illegal access without Api-Key or Authorization set")
        raise CustomError(401, "UNAUTHORIZED")
    token = authorization.replace("Bearer ", "").strip()

    try:
        claims = _decode_jwt(token)
        return JwtPrincipal(claims)
    except Exception as exception:
        logger.error(f"Invalid bearer token: {token}")
        raise CustomError(401, "UNAUTHORIZED") from exception
