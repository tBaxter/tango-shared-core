from django.urls import path
from django.views.generic import TemplateView

from .models import Gallery

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
]