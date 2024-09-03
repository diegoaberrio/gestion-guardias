from django.db import models
from django.contrib.auth.models import User

# Modelo Guardia
class Guardia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.usuario.username} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"

# Modelo Disponibilidad
class Disponibilidad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.usuario.username} no disponible el {self.fecha}"

# Modelo Notificacion
class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('email', 'Correo Electrónico'),
        ('push', 'Notificación Push'),
    ]
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('pendiente', 'Pendiente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        # pylint: disable=no-member
        return f"Notificación para {self.usuario.username} - {self.tipo} - {self.estado}"

# Modelo Estadistica
class Estadistica(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total_guardias = models.IntegerField(default=0)
    guardias_lunes = models.IntegerField(default=0)
    guardias_martes = models.IntegerField(default=0)
    guardias_miercoles = models.IntegerField(default=0)
    guardias_jueves = models.IntegerField(default=0)
    guardias_viernes = models.IntegerField(default=0)
    guardias_sabado = models.IntegerField(default=0)
    guardias_domingo = models.IntegerField(default=0)

    def __str__(self):
        # pylint: disable=no-member
        return f"Estadísticas de {self.usuario.username}"
