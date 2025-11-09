"""
URL configuration for LordsonBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lordsonApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.http import HttpResponse

def empty_favicon(request):
    return HttpResponse(status=204)  # Empty response, no error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('lordson/', include('lordsonApp.urls')),
    path('favicon.ico', empty_favicon),  # ✅ Add this line
]


# 👇 Serve uploaded media files (like banner images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

