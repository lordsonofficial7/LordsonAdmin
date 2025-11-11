import sys
import traceback

try:
    from django.core.wsgi import get_wsgi_application
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LordsonBackend.settings')

    application = get_wsgi_application()
    app = application
except Exception as e:
    print("🔥 Django WSGI startup error:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)
