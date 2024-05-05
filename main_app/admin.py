from django.contrib import admin
from .models import Barrio, Desperfecto, Rubro, Vecino, GMUser, Personal, Sitio, Reclamo, ImagenReclamo, ImagenPromocion, Promocion

admin.site.register(Barrio)
admin.site.register(Desperfecto)
admin.site.register(Rubro)
admin.site.register(Vecino)
admin.site.register(GMUser)
admin.site.register(Personal)
admin.site.register(Sitio)
admin.site.register(Reclamo)
admin.site.register(ImagenReclamo)
admin.site.register(ImagenPromocion)
admin.site.register(Promocion)