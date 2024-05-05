import random
import string
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, VecinoSerializer, PersonalSerializer, RubroSerializer, DesperfectoSerializer, BarrioSerializer, ReclamoSerializer, ImagenReclamoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import Personal, Reclamo, Vecino, ImagenReclamo, ImagenPromocion, Promocion, Barrio
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from email.message import EmailMessage
from dotenv import load_dotenv
import ssl
import smtplib
import os

load_dotenv()

def generar_clave(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class VecinoRegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                vecino = Vecino.objects.get(documento=data['documento'])

                if vecino.usuario:
                    return Response(
                        {'detail': 'Ya existe un vecino con este documento'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Vecino.DoesNotExist:
                return Response(
                    {'detail': 'No existe un vecino con este documento'},
                    status=status.HTTP_404_NOT_FOUND
                )
            with transaction.atomic():
                serializer.save()
                user = get_user_model().objects.get(email=request.data['email'])
                password = generar_clave()
                user.set_password(password)
                user.user_type = 1
                user.save()
                vecino.usuario = user
                vecino.save()

                mail = 'fedesolanes1@gmail.com'
                em = EmailMessage()
                em['From'] = mail
                em['To'] = user.email
                em['Subject'] = 'Clave de acceso'
                em.set_content(f'Su clave de acceso es: {password}')

                context = ssl.create_default_context()

                password=os.getenv('EMAIL_PASSWORD')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(mail, password)
                    server.sendmail(mail, user.email, em.as_string())

                return Response({'detail': 'Registro exitoso'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VecinoLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.data['email'])
            if user.user_type == 1:
                response = super().post(request, *args, **kwargs)
            else:
                response = Response(
                    {'detail': 'Acceso denegado para este tipo de usuario'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except get_user_model().DoesNotExist:
            response = Response(
                {'detail': 'No existe un usuario con este email'},
                status=status.HTTP_404_NOT_FOUND
            )

        return response

class PersonalRegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                personal = Personal.objects.get(legajo=data['legajo'])

                if personal.usuario:
                    return Response(
                        {'detail': 'Ya existe un inspector con este legajo'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Personal.DoesNotExist:
                return Response(
                    {'detail': 'No existe un inspector con este legajo'},
                    status=status.HTTP_404_NOT_FOUND
                )
            with transaction.atomic():
                serializer.save()
                user = get_user_model().objects.get(email=request.data['email'])
                user.set_password(request.data['password'])
                user.user_type = 2
                user.save()
                personal.usuario = user
                personal.save()
                token = CustomTokenObtainPairSerializer().get_token(user)
                return Response({
                    'access': str(token.access_token),
                    'user_id': user.id,
                    'email': user.email,
                    'nombre': personal.nombre,
                    'apellido': personal.apellido,
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(email=request.data['email'])
            if user.user_type == 2:
                response = super().post(request, *args, **kwargs)
            else:
                response = Response(
                    {'detail': 'Access denied for this user type.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except get_user_model().DoesNotExist:
            response = Response(
                {'detail': 'No user with this email exists.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return response

class ReclamoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ReclamoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            reclamo = Reclamo.objects.get(id=pk)
        except Reclamo.DoesNotExist:
            return Response(
                {'detail': 'No existe ese reclamo'},
                status=status.HTTP_404_NOT_FOUND
            )

        reclamo_serializer = ReclamoSerializer(reclamo)
        imagenes = ImagenReclamo.objects.filter(reclamo=reclamo)
        imagenes_serializer = ImagenReclamoSerializer(imagenes, many=True)
        return Response({'reclamo': reclamo_serializer.data, 'imagenes': imagenes_serializer.data}, status=status.HTTP_200_OK)

class ReclamosView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reclamos = Reclamo.objects.filter(vecino__user=user)
        serializer = ReclamoSerializer(reclamos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)