from django.urls import path
from .views import download_fast_api, downloadFileNest

urlpatterns = [
    path('fastapi/download', download_fast_api),
    path('nestapi/downloadNest', downloadFileNest),
]
