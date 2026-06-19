from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Public routes
        if (
            request.url.path.startswith("/docs")
            or request.url.path.startswith("/openapi.json")
            or request.url.path.startswith("/api/v1/auth")
        ):
            return await call_next(request)

        # Custom logic can be added here
        # JWT validation is already handled by dependencies

        response = await call_next(request)

        return response