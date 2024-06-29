from django.urls import re_path
from . import views
urlpatterns = [
    re_path('registro', views.VecinoRegisterView.as_view()),
    re_path('vecino/login', views.VecinoLoginView.as_view()),
    re_path('personal/login/', views.PersonalLoginView.as_view()),
    re_path('personal/register/', views.PersonalRegisterView.as_view()),
    re_path('reclamo', views.ReclamoView.as_view()),
    re_path('reclamos', views.GetReclamosView.as_view()),
    re_path('vecino/set-password', views.VecinoSetPasswordView.as_view()),
    re_path('vecino/send-code-for-change-password', views.SendCodeForChangePasswordView.as_view()),
    re_path('vecino/change-password', views.ChangePasswordView.as_view()),
    re_path('reclamo/agregar-imagen', views.ReclamoAddImage.as_view()),
    re_path('denunica/crear', views.CrearDenunciaView.as_view()),
    re_path('denuncia/agregar-imagen', views.DenunciaImagenView.as_view()),
    re_path('denuncia', views.GetDenunciaView.as_view()),
    re_path('denuncias', views.GetDenunciasListView.as_view()),
    re_path('promocion/crear', views.CreatePromocionView.as_view()),
    re_path('promocion/agregar-imagen', views.PromocionImagenView.as_view()),
    re_path('promocion', views.GetPromocionView.as_view()),
    re_path('promociones', views.GetPromocionListView.as_view()),

]
