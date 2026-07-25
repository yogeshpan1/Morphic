from django.urls import path

from .views import ConvertFileView

urlpatterns = [
    path('convert/', ConvertFileView.as_view(), name='convert-file'),
]