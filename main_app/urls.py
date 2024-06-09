from django.urls import re_path
from .views import (VecinoRegisterView, VecinoLoginView, PersonalLoginView,
                    ReclamoView, GetReclamosView, VecinoSetPasswordView,
                    SendCodeForChangePasswordView, ChangePasswordView,)
urlpatterns = [
    re_path('registro', VecinoRegisterView.as_view()),
    re_path('vecino/login', VecinoLoginView.as_view()),
    re_path('personal/login/', PersonalLoginView.as_view()),
    re_path('reclamo', ReclamoView.as_view()),
    re_path('reclamos', GetReclamosView.as_view()),
    re_path('vecino/set-password', VecinoSetPasswordView.as_view()),
    re_path('vecino/send-code-for-change-password', SendCodeForChangePasswordView.as_view()),
    re_path('vecino/change-password', ChangePasswordView.as_view()),

]
