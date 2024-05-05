from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from .models import Reclamo, Vecino, Personal, Rubro, Desperfecto, Barrio

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email

        if self.user.user_type == 1:
            vecino = Vecino.objects.get(usuario=self.user)
            data['nombre'] = vecino.nombre
            data['apellido'] = vecino.apellido
        else:
            personal = Personal.objects.get(usuario=self.user)
            data['nombre'] = personal.nombre
            data['apellido'] = personal.apellido


        return data

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
        model = Reclamo
        fields = '__all__'