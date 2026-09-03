from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.middlewares import register_middlewares
from app.modules.auth.router import router as auth_router
from app.modules.rooms.router import router as rooms_router
from app.modules.bookings.router import router as bookings_router


app = FastAPI(
    title="Booking Service",
    description="Service for finding meeting rooms",
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

register_middlewares(app)

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(bookings_router)

@app.get("/")
async def root():
    return {
        "message": "Booking service",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/register, /auth/login, /auth/refresh",
            "rooms": "/rooms",
            "bookings": "/bookings"
            }
        }

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
        swagger_favicon_url="/static/swagger/favicon.png",
    )