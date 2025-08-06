from django.contrib import admin
from django.urls import path ,include
from reports.views import submit_report
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', submit_report, name='submit_report'),
    path('', include('reports.urls')),  # <-- должно быть
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
