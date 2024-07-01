from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from .models import Reclamo, Vecino, Personal, Rubro, Desperfecto, Barrio, Denuncia, DenunciaImagen, Promocion, ImagenReclamo, ImagenPromocion, Notification, UserVecino, UserPersonal, MovimientoReclamo, MovimientoDenuncia, Sitio, PersonalRubro

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email

        if self.user.user_type == 1:
            vecino = UserVecino.objects.get(user=self.user).vecino
            data['nombre'] = vecino.nombre
            data['apellido'] = vecino.apellido
            data['documento'] = vecino.documento
        else:
            personal = UserPersonal.objects.get(user=self.user).personal
            data['nombre'] = personal.nombre
            data['apellido'] = personal.apellido
            data['legajo'] = personal.legajo

            try:
                rubro = PersonalRubro.objects.get(personal=personal)
                data['especialidad'] = rubro.rubro.descripcion
                data['especialidad_id'] = rubro.rubro.id
            except PersonalRubro.DoesNotExist:
                data['especialidad'] = None


        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        if user.user_type == 1:
            vecino = UserVecino.objects.get(user=user).vecino
            token['nombre'] = vecino.nombre
            token['apellido'] = vecino.apellido
            token['documento'] = vecino.documento
            token['direccion'] = vecino.direccion
            token['rol'] = 'vecino'
        else:
            personal = UserPersonal.objects.get(user=user).personal
            token['nombre'] = personal.nombre
            token['apellido'] = personal.apellido
            token['legajo'] = personal.legajo
            token['rol'] = 'personal'

            try:
                rubro = PersonalRubro.objects.get(personal=personal)
                token['especialidad'] = rubro.rubro.descripcion
                token['especialidad_id'] = rubro.rubro.id
            except PersonalRubro.DoesNotExist:
                token['especialidad'] = None


        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ['id', 'email', 'username', 'password']

class VecinoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Vecino
        fields = '__all__'

class PersonalSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Personal
        fields = '__all__'

class RubroSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Rubro
        fields = '__all__'

class DesperfectoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Desperfecto
        fields = '__all__'

class BarrioSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Barrio
        fields = '__all__'

class ReclamoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Reclamo
        fields = ['id', 'descripcion', 'estado', 'vecino', 'personal', 'desperfecto', 'sitio','idReclamoUnificado','nombre_vecino','nombre_sitio','ubicacion','nombre_personal']

class ImagenReclamoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ImagenReclamo
        fields = '__all__'


class DenunciaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Denuncia
        fields = ['id', 'descripcion', 'estado', 'sitio','nombre_denunciado','nombre_sitio','ubicacion','denunciante','aceptaResponsabilidad']


class DenunciaImagenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DenunciaImagen
        fields = '__all__'


class PromocionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Promocion
        fields = ['id', 'nombre','titulo', 'horarios' , 'vecino', 'descripcion', 'validado', 'medioDeContacto','rubro','ubicacion','nombre_vecino','nombre_rubro','nombre_ubicacion', 'banner', 'calles']


class PromocionImagenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ImagenPromocion
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Notification
        fields = '__all__'

class MovimientoReclamoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = MovimientoReclamo
        fields = '__all__'

class MovimientoDenunciaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = MovimientoDenuncia
        fields = '__all__'

class SitioSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Sitio
        fields = '__all__'