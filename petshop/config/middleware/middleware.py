from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from fastapi import Request
from starlette.responses import Response
from datetime import datetime

from api.auth.token import decode_access_token
from config.database.queries_table import DatabaseQueries


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = None  
        role = "guest"          

        if token:
            try:
                token_data = decode_access_token(token)
                user_id = token_data.user_id
                role = token_data.role
            except Exception as e:
                print(f"Failed to decode token: {e}")

        start_time = datetime.utcnow()
        response: Response = await call_next(request)
        end_time = datetime.utcnow()

        result = "done" if response.status_code < 400 else "fail"
        print(user_id, role, start_time, end_time, result)

        log_entry = {
            "user_id": user_id,
            "role": role,
            "action": f"{request.method} {request.url.path}",
            "result": result,
            "timestamp": end_time,
        }

        
        await DatabaseQueries.add_log_from_dict(log_entry)

        return response
