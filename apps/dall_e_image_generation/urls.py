from django.urls import path
from .views import ImageGenerationView

urlpatterns = [
    path('strings/', ImageGenerationView.as_view(), name='image-generation'),
]
