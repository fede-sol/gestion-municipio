from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class GMUser(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'vecino'),
      (2, 'inspector'),
    )

    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    is_email_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Barrio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Vecino(models.Model):
    documento = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(GMUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellido



class Rubro(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

class Desperfecto(models.Model):
    descripcion = models.TextField()
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion


class Personal(models.Model):
    legajo = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    fechaIngreso = models.DateField()
    usuario = models.ForeignKey(GMUser, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.legajo} {self.nombre} {self.apellido}"

class Sitio(models.Model):
    latitud = models.DecimalField(max_digits=10, decimal_places=8)
    longitud = models.DecimalField(max_digits=11, decimal_places=8)
    calle = models.CharField(max_length=100)
    numero = models.IntegerField()
    entreCalleA = models.CharField(max_length=100)
    entreCalleB = models.CharField(max_length=100)
    descripcion = models.TextField()
    aCargoDe = models.CharField(max_length=100)
    apertura = models.DateField()
    cierre = models.DateField(null=True, blank=True)
    comentarios = models.TextField()

    def __str__(self):
        return f"{self.calle} {self.numero}"

class Reclamo(models.Model):
    estados_reclamo = (
      (1, 'En revision'),
      (2, 'Abierto'),
      (3, 'Cerrado'),
    )
    vecino = models.ForeignKey(Vecino, on_delete=models.CASCADE)
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    desperfecto = models.ForeignKey(Desperfecto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.PositiveSmallIntegerField(choices=estados_reclamo,default=1)
    idReclamoUnificado = models.IntegerField()
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reclamo #{self.id}"

class MovimientoReclamo(models.Model):
    reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Personal, on_delete=models.CASCADE)
    causa = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento #{self.id}"

class Denuncia(models.Model):
    estados_denuncia = (
      (1, 'Abierta'),
      (2, 'Cerrada'),
    )
    denunciante = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    denunciado = models.ForeignKey(Vecino, on_delete=models.CASCADE)
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.PositiveSmallIntegerField(choices=estados_denuncia,default=1)
    aceptaResponsabilidad = models.BooleanField(default=False)

    def __str__(self):
        return f"Denuncia #{self.id}"

class MovimientoDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=150)
    causa = models.CharField(max_length=4000)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento #{self.id}"

class Promocion(models.Model):
    descripcion = models.CharField(max_length=1000)
    horarios = models.CharField(max_length=30)
    vecino = models.ForeignKey(Vecino, on_delete=models.CASCADE)
    medioDeContacto = models.CharField(max_length=100)
    validado = models.BooleanField(default=False)

    def __str__(self):
        return self.vecino.nombre + ' ' + self.vecino.apellido

class ImagenReclamo(models.Model):
    imagen = models.ImageField(upload_to='reclamos/')
    reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)

class ImagenPromocion(models.Model):
    imagen = models.ImageField(upload_to='promociones/')
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)


class UserRegisterCode(models.Model):
    user = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"
