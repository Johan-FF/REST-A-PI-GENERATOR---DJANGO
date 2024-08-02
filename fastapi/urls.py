from django.urls import path
from .views import download_fast_api, download_file_nest

urlpatterns = [
    path('fastapi/download', download_fast_api),
    path('nestapi/download', download_file_nest),
]
