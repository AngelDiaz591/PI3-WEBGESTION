from django.db import models
from django.contrib.auth.models import User
from PIL import Image  
from django.utils import timezone
# Create your models here.
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Productos(models.Model):
    idproducts = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    precio = models.PositiveBigIntegerField()
    marca = models.CharField(max_length=255)
    cantPro = models.CharField(max_length=255)
    imagen = models.BinaryField(null=True, blank=True)

    id_categorias = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.precio)
    
class Mensajes(models.Model):
    idcomentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    tiempo_creacion = models.DateTimeField(default=timezone.now)
    respuestascomentarios=models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.comentario