from django.db import models
from django.contrib.auth.models import User 

class InformacionGeneral(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion_corta = models.CharField(max_length=250, help_text="Descripción para la sección de encabezado.")
    texto_principal = models.TextField(help_text="Texto largo para la sección 'Sobre Nosotros' o 'Nuestra Historia'.")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Información General: {self.titulo}"
    
    class Meta:
        verbose_name = "Información General"
        verbose_name_plural = "Información General"
