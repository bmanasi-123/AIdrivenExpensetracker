import os
import django
from django.core.asgi import get_asgi_application
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount
from starlette.applications import Starlette

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Convert Django ASGI app
django_asgi_app = get_asgi_application()

# Combine Django and FastAPI inside Starlette
application = Starlette(
    routes=[
        # Mount("/fastapi", app=expenseapp),  # ✅ FastAPI should now be mounted at /fastapi
        Mount("/", app=WSGIMiddleware(django_asgi_app)),  # ✅ Django handles everything else
    ]
)
