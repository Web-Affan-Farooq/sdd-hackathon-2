from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Request
from ..config.settings import settings
import httpx
import time


# JWKS cache with TTL
_jwks_cache = {}
_jwks_cache_time = 0
JWKS_CACHE_TTL = 3600  # 1 hour


async def fetch_jwks():
    """Fetch JWKS from Better Auth provider with caching."""
    current_time = time.time()
    if current_time - _jwks_cache_time > JWKS_CACHE_TTL or not _jwks_cache:
        if settings.better_auth_url:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(f"{settings.better_auth_url}/api/auth/jwks")
                    response.raise_for_status()
                    _jwks_cache = response.json()
                    _jwks_cache_time = current_time
                except httpx.HTTPStatusError:
                    # Fallback to empty cache in dev mode
                    _jwks_cache = {}
        else:
            # Dev mode - return empty cache
            _jwks_cache = {}

    return _jwks_cache


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user_id from JWT token.
    In a real Better Auth setup, this would extract the user ID from the token claims.
    For now, we'll simulate the extraction.
    """
    try:
        # Decode without verification for dev mode
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], options={"verify_signature": False})

        # In production with Better Auth, we'd verify signature against JWKS
        user_id: str = payload.get("userId")
        if user_id is None:
            return None

        return int(user_id)
    except JWTError:
        return None


async def get_current_user_id(request: Request) -> int:
    """Get current user ID from JWT token in Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id