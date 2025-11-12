# import os
# from django.core.wsgi import get_wsgi_application
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LordsonBackend.settings')
# application = get_wsgi_application()
# app = application



import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

print("🚀 Starting Django on Vercel...", flush=True)

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LordsonBackend.settings")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    application = get_wsgi_application()
    app = application
    print("✅ Django loaded successfully!", flush=True)
except Exception as e:
    print("🔥 Django startup error:", e, flush=True)
    traceback.print_exc()
    sys.exit(1)
