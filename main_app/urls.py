from django.urls import re_path
from .views import VecinoRegisterView,VecinoLoginView

urlpatterns = [
    re_path('registro', VecinoRegisterView.as_view()),
    re_path('vecino/login', VecinoLoginView.as_view()),
]
