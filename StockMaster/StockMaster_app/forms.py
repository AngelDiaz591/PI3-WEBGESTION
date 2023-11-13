from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'contrasena', 'genero', 'numero_telefono']