import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Always allow login and static files
        if path.startswith("/login") or path.startswith("/static"):
            response = await call_next(request)
            return response

        # Check authentication for admin routes
        if (
            path.startswith("/admin")
            or path.startswith("/new")
            or path.startswith("/edit")
            or (path.startswith("/posts") and request.method in ["POST", "DELETE"])
        ):
            if not self.is_authenticated(request):
                return RedirectResponse(url="/login", status_code=303)

        response = await call_next(request)
        return response

        # Check if path is protected
        if any(path.startswith(route) for route in protected_routes):
            if not self.is_authenticated(request):
                return RedirectResponse(url="/login", status_code=303)

        response = await call_next(request)
        return response

        # Check if path is protected
        if any(path.startswith(route) for route in protected_routes):
            if not self.is_authenticated(request):
                print(f"Redirecting to login for path: {path}")
                return RedirectResponse(url="/login", status_code=303)

        response = await call_next(request)
        return response

        # Check if path is protected
        if any(path.startswith(route) for route in protected_routes):
            if not self.is_authenticated(request):
                return RedirectResponse(url="/login", status_code=303)

        response = await call_next(request)
        return response

    def is_authenticated(self, request: Request) -> bool:
        auth_token = request.cookies.get("auth_token")
        return auth_token == SECRET_KEY


def require_auth(request: Request):
    auth_token = request.cookies.get("auth_token")
    if auth_token != SECRET_KEY:
        raise HTTPException(status_code=303, detail="Authentication required")


def set_auth_cookie(response, token: str):
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=3600,  # 1 hour
        httponly=True,
        samesite="lax",
    )
    return response


def clear_auth_cookie(response):
    response.delete_cookie("auth_token")
    return response
