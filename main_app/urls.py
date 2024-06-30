from django.urls import re_path, path
from . import views
urlpatterns = [
    path('registro', views.VecinoRegisterView.as_view()),
    path('vecino/login', views.VecinoLoginView.as_view()),
    path('personal/login/', views.PersonalLoginView.as_view()),
    path('personal/register/', views.PersonalRegisterView.as_view()),
    path('reclamo/agregar-imagen', views.ReclamoAddImage.as_view()),
    path('reclamos', views.GetReclamosView.as_view()),
    re_path('reclamo/(?P<pk>.+)/$', views.ReclamoView.as_view()),
    path('reclamo/crear', views.CreateReclamoView.as_view()),
    path('vecino/set-password', views.VecinoSetPasswordView.as_view()),
    path('vecino/send-code-for-change-password', views.SendCodeForChangePasswordView.as_view()),
    path('vecino/change-password', views.ChangePasswordView.as_view()),
    path('denuncia/crear', views.CrearDenunciaView.as_view()),
    path('denuncia/agregar-imagen', views.DenunciaImagenView.as_view()),
    re_path('denuncia/(?P<pk>.+)/$', views.GetDenunciaView.as_view()),
    path('denuncias', views.GetDenunciasListView.as_view()),
    path('promocion/crear', views.CreatePromocionView.as_view()),
    path('promocion/agregar-imagen', views.PromocionImagenView.as_view()),
    re_path('promocion/(?P<pk>.+)/$', views.GetPromocionView.as_view()),
    path('promociones', views.GetPromocionListView.as_view()),
    path('desperfectos', views.ListaDesperfectos.as_view()),

]
