import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from api.routes import get_apps_router
from config.database.create_tables import TableCreator
from config.middleware.middleware import LoggingMiddleware
from config.project_config import Database


def create_application() -> FastAPI:
    # Создаем основной объект приложения
    application = FastAPI(
        title="Pet_Shop",
        version="1.0.0",
        description="API for Pet Shop with JWT authentication",
        debug=True,
    )

    # Настройка CORS для поддержки кросс-доменных запросов
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Добавляем пользовательский логгинг
    application.add_middleware(LoggingMiddleware)

    # Перенаправление с корневого URL на документацию
    @application.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    # Событие старта приложения
    @application.on_event("startup")
    async def startup():
        # Подключаем пул соединений к БД и создаем все таблицы
        await Database.connect()  # Создаём пул
        await TableCreator.create_all_tables()

    # Событие завершения работы приложения
    @application.on_event("shutdown")
    async def shutdown():
        # Закрываем пул соединений
        await Database.disconnect()

    # Подключаем роутеры
    application.include_router(get_apps_router())

    # Кастомный OpenAPI (JWT и авторизация)
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

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
