from fastapi import FastAPI

from app.modules.auth.router import auth

app = FastAPI(
    title="Booking Service",
    description="Service for finding meeting rooms",
)

app.include_router(auth)

@app.get("/")
async def root():
    return {
        "message": "Booking service",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/register, /auth/login, /auth/refresh"
            }
        }

