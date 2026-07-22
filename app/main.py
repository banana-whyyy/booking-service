from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.rooms.router import router as rooms_router


app = FastAPI(
    title="Booking Service",
    description="Service for finding meeting rooms",
)

app.include_router(auth_router)
app.include_router(rooms_router)

@app.get("/")
async def root():
    return {
        "message": "Booking service",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/register, /auth/login, /auth/refresh",
            "rooms": "/rooms",
            }
        }

