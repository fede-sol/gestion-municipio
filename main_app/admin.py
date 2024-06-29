from django.contrib import admin
from .models import Barrio, Desperfecto, Rubro, Vecino, GMUser, Personal, Sitio, Reclamo, ImagenReclamo, ImagenPromocion, Promocion, UserRegisterCode

admin.site.register(Barrio)
admin.site.register(Desperfecto)
admin.site.register(Rubro)
admin.site.register(Vecino)
admin.site.register(Personal)
admin.site.register(Sitio)
admin.site.register(Reclamo)
admin.site.register(ImagenReclamo)
admin.site.register(ImagenPromocion)
admin.site.register(Promocion)
admin.site.register(UserRegisterCode)


class GMUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_user_type', 'get_user_info')

    def get_user_type(self, obj):
        return obj.get_user_type_display()
    get_user_type.short_description = 'User Type'

    def get_user_info(self, obj):
        if obj.user_type == 1:  # Vecino
            vecino = Vecino.objects.filter(usuario=obj).first()
            if vecino:
                return f"Documento: {vecino.documento}, Nombre: {vecino.nombre}"
        elif obj.user_type == 2:  # Personal
            personal = Personal.objects.filter(usuario=obj).first()
            if personal:
                return f"Legajo: {personal.legajo}, Nombre: {personal.nombre}"
        return "-"
    get_user_info.short_description = 'User Info'

admin.site.register(GMUser, GMUserAdmin)