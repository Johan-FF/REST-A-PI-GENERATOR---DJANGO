from django.urls import path
from .views import download_file

urlpatterns = [
    path('fastapi/download', download_file),
]
