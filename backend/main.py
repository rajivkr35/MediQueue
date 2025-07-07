from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi  # 🔒 for custom docs
from auth import router as auth_router
from routers.queue import router as queue_router
from routers.predict import router as predict_router
from routers import admin

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(queue_router)
app.include_router(predict_router)
app.include_router(admin.router)

# ✅ Custom OpenAPI schema for token auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Smart Queue API",
        version="1.0",
        description="API for Smart Hospital Queue System",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply globally
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# uvicorn backend.main:app --reload

print("🚀 Allowed origins:", ["http://127.0.0.1:3000"])
