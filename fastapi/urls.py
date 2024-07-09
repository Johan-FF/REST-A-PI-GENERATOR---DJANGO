from django.urls import path
from .views import download_file, downloadFileNest

urlpatterns = [
    path('fastapi/download', download_file),
    path('nestapi/downloadNest', downloadFileNest),
]
