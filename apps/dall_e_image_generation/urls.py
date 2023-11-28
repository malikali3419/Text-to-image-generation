from django.urls import path
from .views import ImageGenerationView

urlpatterns = [
    path("generate-image/", ImageGenerationView.as_view(), name='image-generation'),
]
