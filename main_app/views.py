import random
import string
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, VecinoSerializer, PersonalSerializer, RubroSerializer, DesperfectoSerializer, BarrioSerializer, ReclamoSerializer, ImagenReclamoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import Personal, Reclamo, Vecino, ImagenReclamo, ImagenPromocion, Promocion, Barrio, UserRegisterCode
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
    '''
    Permite a un vecino registrarse en la aplicación.
    Este endpoint debe ser utilizado para los vecinos que aún no tienen una cuenta.
    Una vez se verifica que el vecino existe en la base de datos
    se crea el usuario pero se espera a que sea aceptado por el municipio.
    Una vez el municipio lo acepta, se genera una clave de
    8 dígitos la cual es enviada al email que el vecino indicó al momento de registrarse
    '''

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
                user.user_type = 1
                user.save()
                vecino.usuario = user
                vecino.save()

                UserRegisterCode.objects.create(user=user, code=password)

                mail = 'fedesolanes1@gmail.com'
                em = EmailMessage()
                em['From'] = mail
                em['To'] = user.email
                em['Subject'] = 'Configura tu contraseña'
                em.set_content(f'Su clave para configurar contraseña es: {password}')

                context = ssl.create_default_context()

                password=os.getenv('EMAIL_PASSWORD')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(mail, password)
                    server.sendmail(mail, user.email, em.as_string())

                return Response(
                    {'detail': 'Registro exitoso'},
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VecinoSetPasswordView(APIView):
    '''
    Permite a un vecino configurar su contraseña.
    Este endpoint requiere que el vecino haya sido aceptado previamente por el municipio.
    '''

    def post(self, request):
        data = request.data
        try:
            code = UserRegisterCode.objects.get(code=data['code'])
        except UserRegisterCode.DoesNotExist:
            return Response(
                {'detail': 'No existe un código de registro con este valor'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not code.used:
            user = code.user
            user.set_password(data['password'])
            user.save()
            code.used = True
            code.save()
            return Response(
                {'detail': 'Contraseña configurada correctamente'},
                status=status.HTTP_200_OK
            )


class SendCodeForChangePasswordView(APIView):
    '''
    Permite a un vecino solicitar un código para cambiar su contraseña.
    Este endpoint requiere que el vecino haya sido aceptado previamente por el municipio.
    '''

    def post(self, request):
        data = request.data
        try:
            user = get_user_model().objects.get(email=data['email'])
            if user.user_type == 1:
                code = generar_clave()
                UserRegisterCode.objects.create(user=user, code=code)
                mail = 'fedesolanes1@gmail.com'
                em = EmailMessage()
                em['From'] = mail
                em['To'] = user.email
                em['Subject'] = 'Configura tu contraseña'
                em.set_content(f'Su clave para configurar contraseña es: {password}')
            else:
                return Response(
                    {'detail': 'Acceso denegado para este tipo de usuario'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except get_user_model().DoesNotExist:
            return Response(
                {'detail': 'No existe un usuario con este email'},
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePasswordView(APIView):
    '''
    Endpoint de cambio de contraseña: solo necesita contraseña nueva sin código, autentica con el token
    '''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        user.set_password(data['password'])
        user.save()
        return Response(
            {'detail': 'Contraseña cambiada correctamente'},
            status=status.HTTP_200_OK
        )


class VecinoLoginView(TokenObtainPairView):
    '''
    Permite a un vecino iniciar sesión en la aplicación.
    Este endpoint requiere que el vecino tenga una
    cuenta registrada y aceptada previamente por el municipio.
    '''

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
    '''
    Permite a un inspector iniciar sesión en la aplicación.
    Este endpoint requiere que el inspector tenga una cuenta registrada.
    '''
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
    '''Vista para crear o obtener un reclamo'''
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
        return Response({'reclamo': reclamo_serializer.data,
                         'imagenes': imagenes_serializer.data},
                          status=status.HTTP_200_OK
                        )


class GetReclamosView(APIView):
    '''Vista para obtener todos los reclamos de un vecino'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reclamos = Reclamo.objects.filter(vecino__usuario=user)
        serializer = ReclamoSerializer(reclamos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
