from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main_app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT) + staticfiles_urlpatterns()

