from django.contrib.auth.models import User, Group
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

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
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
    id_area = models.ForeignKey(Area, on_delete=models.CASCADE, null= True)


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
    
class RolExtra(models.Model):
    grupo = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    principal = models.BooleanField(default=False)
    inventario = models.BooleanField(default=False)
    productos = models.BooleanField(default=False)
    proveedores = models.BooleanField(default=False)
    etiquetas = models.BooleanField(default=False)
    area = models.BooleanField(default=False)
    pedidos = models.BooleanField(default=False)
    productosRecuperacion = models.BooleanField(default=False)
    proveedoresRecuperacion = models.BooleanField(default=False)
    etiquetasRecuperacion = models.BooleanField(default=False)
    designadoRecuperacion = models.BooleanField(default=False)
    usuariosRecuperacion = models.BooleanField(default=False)
    usuarios = models.BooleanField(default=False)
    roles = models.BooleanField(default=False)
    soporte = models.BooleanField(default=False)
    soporteenviar = models.BooleanField(default=False)
    contra = models.BooleanField(default=False)
    historialGeneral = models.BooleanField(default=False)
    historialModificaciones = models.BooleanField(default=False)
    historialMovimientos = models.BooleanField(default=False)
    historialEliminados = models.BooleanField(default=False)
    
    movi = models.CharField(max_length=100, null= True)
    username = models.CharField(max_length=100, null=True)
    fech_cate= models.DateTimeField(default=timezone.now, null= True)
    status= models.BooleanField(default=True)
    status_mov = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

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

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    mun_cel = models.CharField(max_length=10)
    imagen = models.BinaryField(null=True, blank=True)
    permiso = models.BooleanField(default=True)
    cambio = models.BooleanField(default=True)
    descripcion = models.CharField(max_length=255, null=True)
    comen = models.CharField(max_length =150)
    id = models.ForeignKey(User, on_delete=models.CASCADE, null= True)

        
######################################### Modelo de Ordenes ##############################################################################
class Ordenes(models.Model):
    id_Orden = models.AutoField(primary_key=True)
    no_Orden = models.CharField(max_length=20)
    fechaPedido = models.DateTimeField(default=timezone.now())
    nombreProd = models.CharField(max_length=20)
    codigoProd = models.CharField(max_length=6)
    cantSolicitada = models.IntegerField()
    precioUnitario = models.IntegerField()
    totalPedido = models.IntegerField()
    nombreProv = models.CharField(max_length=50)
    dirProveedor = models.CharField(max_length=100)
    telefonoProv = models.IntegerField()
    emailProv = models.CharField(max_length=100)
    dirEntrega = models.CharField(max_length=100)
    fechaEntrega = models.DateTimeField(null=True)
    metodoPago = models.CharField(max_length=20)
    status = models.CharField(max_length=20)