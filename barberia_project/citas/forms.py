# citas/forms.py
from django import forms
from .models import Cita, Servicio

class ServicioModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nombre} ({obj.duracion_minutos} min) - ${obj.precio:.2f}"

class CitaForm(forms.ModelForm):
    servicios = ServicioModelChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona los servicios que deseas",
        required=True
    )
    
    fecha_hora_inicio = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )

    class Meta:
        model = Cita
        fields = [
            'nombre_cliente', 
            'telefono_cliente', 
            'servicios', 
            'fecha_hora_inicio'
        ]
        
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'placeholder': 'Escribe tu nombre completo'}),
            'telefono_cliente': forms.TextInput(attrs={'placeholder': 'Tu número de teléfono'}),
        }
        labels = {
            'nombre_cliente': 'Tu Nombre',
            'telefono_cliente': 'Teléfono',
        }