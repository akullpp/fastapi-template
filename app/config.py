from os import getenv

db_config = {
    "DB_URL": getenv("DB_URL", "localhost"),
    "DB_NAME": getenv("DB_NAME", "platform"),
    "DB_USER": getenv("DB_USER", "admin"),
    "DB_PASS": getenv("DB_PASS", "admin"),
}

log_config = {
    "LOG_LEVEL": getenv("LOG_LEVEL", "DEBUG"),
    "LOG_JSON": getenv("LOG_JSON", "0"),
}

AUTH_DOMAIN = getenv("AUTH_DOMAIN", "")
auth_config = {
    "AUTH_DOMAIN": AUTH_DOMAIN,
    "JWT_AUDIENCE": getenv("JWT_AUDIENCE", ""),
    "JWT_ALGORITHMS": ["RS256"],
    "JWT_ISSUER": f"https://{AUTH_DOMAIN}/",
    "JWKS_URL": f"https://{AUTH_DOMAIN}/.well-known/jwks.json",
}

config = {
    "STAGE": getenv("STAGE", "LOCAL"),
    "NAME": getenv("NAME", "fastapi"),
    "API_KEY": getenv("API_KEY", "0a9231ef-9f5a-48d2-bfa3-7236bba09a69"),
    **db_config,
    **log_config,
    **auth_config,
}
