from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from .models import Reclamo, Vecino, Personal, Rubro, Desperfecto, Barrio, Denuncia, DenunciadoReclamo, DenunciaImagen, Promocion, ImagenReclamo, ImagenPromocion, Notification

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email

        if self.user.user_type == 1:
            vecino = Vecino.objects.get(usuario=self.user)
            data['nombre'] = vecino.nombre
            data['apellido'] = vecino.apellido
            data['documento'] = vecino.documento
        else:
            personal = Personal.objects.get(usuario=self.user)
            data['nombre'] = personal.nombre
            data['apellido'] = personal.apellido
            data['legajo'] = personal.legajo


        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        if user.user_type == 1:
            vecino = Vecino.objects.get(usuario=user)
            token['nombre'] = vecino.nombre
            token['apellido'] = vecino.apellido
            token['documento'] = vecino.documento
            token['direccion'] = vecino.direccion
            token['rol'] = 'vecino'
        else:
            personal = Personal.objects.get(usuario=user)
            token['nombre'] = personal.nombre
            token['apellido'] = personal.apellido
            token['legajo'] = personal.legajo
            token['rol'] = 'personal'


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
        fields = '__all__'

class ImagenReclamoSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ImagenReclamo
        fields = '__all__'


class DenunciaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Denuncia
        fields = '__all__'


class DenunciaImagenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DenunciaImagen
        fields = '__all__'


class PromocionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Promocion
        fields = '__all__'


class PromocionImagenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ImagenPromocion
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Notification
        fields = '__all__'