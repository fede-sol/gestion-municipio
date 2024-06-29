import random
import string
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, VecinoSerializer, PersonalSerializer, RubroSerializer, DesperfectoSerializer, BarrioSerializer, ReclamoSerializer, ImagenReclamoSerializer, DenunciaSerializer, DenunciaImagenSerializer, PromocionSerializer, PromocionImagenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import Personal, Reclamo, Vecino, ImagenReclamo, ImagenPromocion, Promocion, Barrio, UserRegisterCode, UserVecino, UserPersonal, Denuncia, DenunciaImagen, Notification
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

                try:
                    user_vecino = UserVecino.objects.create(user=user, vecino=vecino)
                except:
                    return Response(
                        {'detail': 'Error interno'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

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
                try:
                    user_personal = UserPersonal.objects.create(user=user, personal=personal)
                except:
                    return Response(
                        {'detail': 'Error interno'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

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


class ReclamoAddImage(APIView):
    '''Vista para agregar una imagen a un reclamo'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            reclamo = Reclamo.objects.get(id=data['numero_reclamo'])
        except Reclamo.DoesNotExist:
            return Response(
                {'detail': 'No existe un reclamo con ese número.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if ImagenReclamo.objects.filter(reclamo=reclamo).count() >= 7:
            return Response(
                {'detail': 'El usuario vecino llegó al límite de 7 imágenes.'},
                status=status.HTTP_403_FORBIDDEN
            )

        imagen = data['imagen']
        try:
            ImagenReclamo.objects.create(reclamo=reclamo, imagen=imagen)
        except:
            return Response(
                {'detail': 'Error interno'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'La imagen se agregó exitosamente.'},
            status=status.HTTP_201_CREATED
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


class CrearDenunciaView(APIView):
    '''Vista para crear una denuncia'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = DenunciaSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DenunciaImagenView(APIView):
    '''Vista para agregar una imagen a una denuncia'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            denuncia = Denuncia.objects.get(id=data['numero_denuncia'])
        except Denuncia.DoesNotExist:
            return Response(
                {'detail': 'No existe una denuncia con ese número.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if DenunciaImagenView.objects.filter(denuncia=denuncia).count() >= 7:
            return Response(
                {'detail': 'El usuario vecino llegó al límite de 7 imágenes.'},
                status=status.HTTP_403_FORBIDDEN
            )

        imagen = data['imagen']
        try:
            DenunciaImagen.objects.create(denuncia=denuncia, imagen=imagen)
        except:
            return Response(
                {'detail': 'Error interno'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'La imagen se agregó exitosamente.'},
            status=status.HTTP_201_CREATED
        )


class GetDenunciaView(APIView):
    '''Vista para obtener una denuncia por pk'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            denuncia = Denuncia.objects.get(id=pk)
        except Denuncia.DoesNotExist:
            return Response(
                {'detail': 'No existe esa denuncia'},
                status=status.HTTP_404_NOT_FOUND
            )

        denuncia_serializer = DenunciaSerializer(denuncia)
        imagenes = DenunciaImagen.objects.filter(denuncia=denuncia)
        imagenes_serializer = DenunciaImagenSerializer(imagenes, many=True)
        return Response({'denuncia': denuncia_serializer.data,
                         'imagenes': imagenes_serializer.data},
                          status=status.HTTP_200_OK
                        )


class GetDenunciasListView(APIView):
    '''Permite obtener una lista de todas las denuncias registradas, tanto las generadas por el mismo usuario, como las que le fueron generadas en su contra; para controlar esto se pasa un parámetro llamado "tipo". Este endpoint requiere que el usuario esté autenticado.'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tipo = request.query_params.get('tipo')
        user = request.user

        if tipo == 'generadas':
            denuncias = Denuncia.objects.filter(denunciante__usuario=user)
        elif tipo == 'recibidas':
            denuncias = Denuncia.objects.filter(denunciado__usuario=user)
        else:
            return Response(
                {'detail': 'Parámetro "tipo" no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DenunciaSerializer(denuncias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePromocionView(APIView):
    '''Vista para crear una promoción'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = PromocionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PromocionImagenView(APIView):
    '''Vista para agregar una imagen a una promoción'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            promocion = Promocion.objects.get(id=data['numero_promocion'])
        except Promocion.DoesNotExist:
            return Response(
                {'detail': 'No existe una promoción con ese número.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if ImagenPromocion.objects.filter(promocion=promocion).count() >= 7:
            return Response(
                {'detail': 'El usuario vecino llegó al límite de 7 imágenes.'},
                status=status.HTTP_403_FORBIDDEN
            )

        imagen = data['imagen']
        try:
            ImagenPromocion.objects.create(promocion=promocion, imagen=imagen)
        except:
            return Response(
                {'detail': 'Error interno'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'La imagen se agregó exitosamente.'},
            status=status.HTTP_201_CREATED
        )


class GetPromocionView(APIView):
    '''Vista para obtener una promoción por pk'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            promocion = Promocion.objects.get(id=pk)
        except Promocion.DoesNotExist:
            return Response(
                {'detail': 'No existe esa promoción'},
                status=status.HTTP_404_NOT_FOUND
            )

        promocion_serializer = PromocionSerializer(promocion)
        imagenes = ImagenPromocion.objects.filter(promocion=promocion)
        imagenes_serializer = PromocionImagenSerializer(imagenes, many=True)
        return Response({'promocion': promocion_serializer.data,
                         'imagenes': imagenes_serializer.data},
                          status=status.HTTP_200_OK
                        )


class GetPromocionListView(APIView):
    '''Obtiene una lista de todas las promociones registradas. Este endpoint está disponible para cualquier usuario, incluso sin autenticación.'''

    def get(self, request):
        promociones = Promocion.objects.all()
        serializer = PromocionSerializer(promociones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetNotifications(APIView):
    '''Obtiene todas las notificaciones de un usuario'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)