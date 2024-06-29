from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import string

def generar_clave(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE,
                               db_column='codigo_barrio')

    def __str__(self):
        return self.nombre + ' ' + self.apellido


class UserVecino(models.Model):
    user = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    vecino = models.ForeignKey(Vecino, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


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
    class Meta:
        verbose_name_plural = 'Personal'

    legajo = models.CharField(primary_key=True, max_length=30)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    sector = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    fechaIngreso = models.DateField()

    def __str__(self):
        return f"{self.legajo} {self.nombre} {self.apellido}"

class UserPersonal(models.Model):
    user = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


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
    vecino = models.ForeignKey(Vecino, on_delete=models.CASCADE, db_column='documento')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    desperfecto = models.ForeignKey(Desperfecto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.PositiveSmallIntegerField(choices=estados_reclamo,default=1)
    idReclamoUnificado = models.IntegerField()
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='legajo')

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
    denunciante = models.ForeignKey(Vecino, on_delete=models.CASCADE, db_column='documento')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.PositiveSmallIntegerField(choices=estados_denuncia,
                                              default=1)
    aceptaResponsabilidad = models.BooleanField(default=False)

    def __str__(self):
        return f"Denuncia #{self.id}"

class DenunciadoReclamo(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)
    denunciado = models.ForeignKey(Vecino, on_delete=models.CASCADE)

    def __str__(self):
        return f"Denunciado #{self.id}"


class DenunciaImagen(models.Model):
    imagen = models.ImageField(upload_to='denuncias/')
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)

class MovimientoDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=150)
    causa = models.CharField(max_length=4000)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento #{self.id}"

class Promocion(models.Model):
    class Meta:
        verbose_name_plural = 'Promociones'
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
    class Meta:
        verbose_name_plural = 'Imagen promociones'

    imagen = models.ImageField(upload_to='promociones/')
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)


class UserRegisterCode(models.Model):
    user = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def save(self, *args, **kwargs):
        UserRegisterCode.objects.filter(user=self.user, used=False).delete()
        while UserRegisterCode.objects.filter(code=self.code).exists():
            self.code = generar_clave()
        return super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(GMUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.title}"


# Define clear and descriptive messages for each notification
NOTIFICATION_MESSAGES = {
    'Reclamo': {
        1: "Su reclamo ha sido enviado para revisión.",
        2: "Su reclamo ha sido abierto y está siendo procesado.",
        3: "Su reclamo ha sido cerrado.",
    },
    'Denuncia': {
        1: "Su denuncia ha sido registrada.",
        2: "Su denuncia ha sido cerrada.",
    },
}


@receiver(post_save, sender=Reclamo)
def create_reclamo_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for the Reclamo owner when its state changes.

    Args:
        sender (Model): The Reclamo model class.
        instance (Reclamo): The Reclamo instance being saved.
        created (bool): Whether the instance is newly created.
        kwargs (dict): Additional arguments passed to the signal handler.
    """

    if created:
        return  # Don't create notification for initial creation

    old_state = Reclamo.objects.filter(pk=instance.pk).get().estado
    new_state = instance.estado

    if old_state != new_state:
        message = NOTIFICATION_MESSAGES['Reclamo'].get(new_state)
        Notification.objects.create(
            user=instance.vecino.user,
            title="Actualización de su reclamo",
            message=message,
        )


@receiver(post_save, sender=Denuncia)
def create_denuncia_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for the Denuncia owner when its state changes.

    Args:
        sender (Model): The Denuncia model class.
        instance (Denuncia): The Denuncia instance being saved.
        created (bool): Whether the instance is newly created.
        kwargs (dict): Additional arguments passed to the signal handler.
    """

    if created:
        return  # Don't create notification for initial creation

    old_state = Denuncia.objects.filter(pk=instance.pk).get().estado
    new_state = instance.estado

    if old_state != new_state:
        message = NOTIFICATION_MESSAGES['Denuncia'].get(new_state)
        Notification.objects.create(
            user=instance.denunciante.user,
            title="Actualización de su denuncia",
            message=message,
        )