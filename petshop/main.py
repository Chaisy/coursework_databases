import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from api.routes import get_apps_router

from config.database.create_tables import TableCreator
from config.middleware.middleware import LoggingMiddleware
from config.project_config import Database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_application() -> FastAPI:
    application = FastAPI(
        title="Pet_Shop",
        version="1.0.0",
        description="API for Pet Shop with JWT authentication",
        debug=True,
    )

    
    application.add_middleware(LoggingMiddleware)

    
    @application.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    
    @application.on_event("startup")
    async def startup():
        await Database.connect()
        await TableCreator.create_all_tables()

    @application.on_event("shutdown")
    async def shutdown():
        await Database.disconnect()

    
    application.include_router(get_apps_router())

    
    def custom_openapi():
        if application.openapi_schema:
            return application.openapi_schema
        openapi_schema = get_openapi(
            title=application.title,
            version=application.version,
            description=application.description,
            routes=application.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        openapi_schema["security"] = [{"BearerAuth": []}]
        application.openapi_schema = openapi_schema
        return application.openapi_schema

    application.openapi = custom_openapi
    return application


app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
