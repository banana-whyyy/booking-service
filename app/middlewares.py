from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


# Ограничение размера тела запроса
class LimitUploadSizeLimit(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int = 2 * 1024  * 1024):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request, call_next):
        content_lenght = request.headers.get("content-lenght")
        if content_lenght and int(content_lenght) > self.max_bytes:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request too large (max 2 Mb)"}
            )
        return await call_next(request)


# Защитные заголовки
class SecurityHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response


# Функция регистрации всех Middleware 
def register_middlewares(app: FastAPI):
    # При Входящем запросе они будут идти в обратном порядке
    # CorsMiddleware -> SecurityHeaderMiddleware -> LimitUploadSizeLimit
    app.add_middleware(LimitUploadSizeLimit, max_bytes=2 * 1024 * 1024)
    app.add_middleware(SecurityHeaderMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )