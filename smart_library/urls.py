from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Daftarkan semua URL dari api_app ke awalan /api/
    path('api/', include('api_app.urls')), 
]
