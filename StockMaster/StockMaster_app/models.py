from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    movi = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    fech_cate = models.DateTimeField(default=timezone.now, null=True)
    status = models.BooleanField(default=True)
    status_mov = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    marca_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    movi = models.CharField(max_length=100, null= True)
    username = models.CharField(max_length=100, null=True)
    fech_cate= models.DateTimeField(default=timezone.now, null= True)
    status= models.BooleanField(default=True)
    status_mov = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

#Modelo de proveedores

class Proveedores(models.Model):    
    idProveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    contacto = models.CharField(max_length=50)
    telefono = models.PositiveBigIntegerField(max_length=10)
    email = models.CharField(max_length=100)
    calle = models.CharField(max_length=100, default="")
    noExt = models.CharField(max_length=50, null=True, default="")
    noInt = models.CharField(max_length=50, null=True, default="")
    colonia = models.CharField(max_length=100, default="")
    cp = models.PositiveBigIntegerField(max_length=5, default="")
    municipio = models.CharField(max_length=100, default="")
    estado = models.CharField(max_length=100, default="")
    pais = models.CharField(max_length=100, default="")
    imagen = models.BinaryField(null=True, blank=True)
    status = models.BooleanField(default=True)
    status_mov = models.BooleanField(default=True)
    hora_baja = models.DateTimeField(default=timezone.now, null=True)
    username = models.CharField(max_length=255, null=True)
    fecha_edit = models.DateTimeField(default=timezone.now, null=True)
    useredit = models.CharField(max_length=255, null=True)
    movimiento = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    idproducts = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    precio = models.PositiveBigIntegerField()
    cantPro = models.CharField(max_length=255)
    imagen = models.BinaryField(null=True, blank=True)

    id_categorias = models.ForeignKey(Categoria, on_delete=models.CASCADE, null= True)
    id_Proveedores = models.ForeignKey(Proveedores, on_delete=models.CASCADE, null = True)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null= True)


    hora_baja = models.DateTimeField(default=timezone.now, null=True)
    username = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=True)
    fecha_edit = models.DateTimeField(default=timezone.now, null=True)
    useredit = models.CharField(max_length=255, null=True)
    movimiento = models.CharField(max_length=255, null=True)
    status_mov = models.BooleanField(default=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.precio)
    
class Mensajes(models.Model):
    idcomentario = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    tiempo_creacion = models.DateTimeField(default=timezone.now)
    respuestascomentarios=models.CharField(max_length=255, null=True)
    admincont= models.CharField(max_length=255,null=True)
    tiem_res = models.DateTimeField(default=timezone.now, null=True)
    status = models.BooleanField(default=True)
    status_mov = models.BooleanField(default=True)

    def __str__(self):
        return self.comentario
class Historial(models.Model):
    idhistorial = models.AutoField(primary_key=True)
    movimiento = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now, null=True)
    nombre = models.CharField(max_length=255, null=True)