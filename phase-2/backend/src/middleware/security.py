from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from ..config.settings import settings
from datetime import datetime, timedelta
from typing import Optional


class JWTBearer(HTTPBearer):
    """
    JWT Token authentication middleware.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            if not self.verify_jwt(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token."
                )
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication credentials were not provided."
            )

    def verify_jwt(self, jwt_token: str) -> bool:
        """
        Verify the JWT token.
        """
        try:
            payload = jwt.decode(jwt_token, settings.secret_key, algorithms=[settings.algorithm])
            return payload is not None
        except JWTError:
            return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_current_user(token: str = None):
    """
    Get the current user from the token.
    This is a placeholder implementation - in a real app, you'd decode the token
    and return user information.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required"
        )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        # In a real implementation, you'd extract user info from the payload
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )