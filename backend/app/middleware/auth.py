from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Lightweight auth middleware.
    In development mode, all requests pass through automatically.
    In production, validate Bearer token from Authorization header.
    """

    UNPROTECTED_PATHS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}

    async def dispatch(self, request: Request, call_next):
        # Always allow unprotected paths
        if request.url.path in self.UNPROTECTED_PATHS:
            return await call_next(request)

        # In development, bypass auth
        if settings.APP_ENV == "development":
            request.state.user_id = settings.DEFAULT_USER_ID
            return await call_next(request)

        # Production: check Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"},
            )

        token = auth_header.split(" ")[1]
        try:
            from jose import jwt, JWTError
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user_id = payload.get("sub", settings.DEFAULT_USER_ID)
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)
