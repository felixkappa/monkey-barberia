from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) 
    duracion_minutos = models.IntegerField(default=60, help_text="Duración del servicio en minutos")

    imagen = models.ImageField(
        upload_to='servicios_imagenes/', 
        blank=True,                     
        null=True,     
        help_text="Imagen representativa del servicio/producto"
    )

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
    
    class Meta:
        verbose_name_plural = "Servicios"

class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=15)
    
    servicios = models.ManyToManyField(Servicio)
    
    fecha_hora_inicio = models.DateTimeField()
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='PENDIENTE',
    )

    @property
    def duracion_total_minutos(self):
        if not self.pk:
            return 0
        return sum(s.duracion_minutos for s in self.servicios.all())

    @property
    def fecha_hora_fin(self):
        if self.fecha_hora_inicio and self.pk:
            return self.fecha_hora_inicio + timedelta(minutes=self.duracion_total_minutos)
        return None 

    def __str__(self):
        return f"Cita de {self.nombre_cliente} el {self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')}"
