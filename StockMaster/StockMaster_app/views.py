from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages as men
from django.contrib.auth.decorators import user_passes_test
from django.core.files import File
from .models import Productos, Mensajes, Categoria, Proveedores, Historial, Marca, Usuario, RolExtra
from django.http.response import JsonResponse
import base64
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.db.models.functions import TruncMonth
import pytz

# Create your views here.



#____________________________________________________________________________________________________________________________________
 
#--------------------------------------------------------------- L O G I N --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________
    
def signin(request):
    if request.user.is_authenticated:
        return redirect('/actividades')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('actividades')
        else:
            form = AuthenticationForm(request.POST)
            if not User.objects.filter(username=username).exists():
                # Agrega un mensaje de error con la etiqueta 'signin'
                messages.error(request, 'Usuario no Registrado', extra_tags='signin')
            else:
                messages.error(request, 'Contraseña Incorrecta', extra_tags='signin')
        return render(request, 'registration/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    
def home(request):
    if request.user.is_authenticated:
        return redirect('/actividades')
    return render(request, 'registration/login.html')

@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('home')
@login_required(login_url='signin')

def exit(request):
    logout(request)
    return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#--------------------------------------------------------- U S U A R I O S --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def usuarios(request):
    if request.user.has_perm('StockMaster_app.view_usuario'):
        mensajes = Mensajes.objects.all()
        cantidad_mensajes = mensajes.count()
        usuario = Usuario.objects.all()
        roles = RolExtra.objects.all()
        form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
        grupos = Group.objects.all()  # Obtiene todos los grupos
        for Usuarios in usuario:
            Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/usuarios.html', { 'Roles':roles, 'Usuarios': form, 'Mensajes':mensajes,'cantidad_mensajes':cantidad_mensajes,'usuario':usuario, 'grupos': grupos})
    else:
        return redirect('/actividades')

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField()

def is_superuser(user):
    return user.is_authenticated and user.is_superuser
@user_passes_test(is_superuser)
@login_required(login_url='signin')
def get_imagen_url(imagen_binaria):
    imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
    return f"data:image/jpeg;base64,{imagen_base64}"
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            user.email = email
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')

            user.save()
            # Agrega el grupo al usuario
            grupo = Group.objects.get(name=request.POST['grupo'])
            user.groups.add(grupo)
            # Resto del código para agregar el usuario al grupo, guardar información adicional, etc.
            calle = request.POST['calle']
            colonia = request.POST['colonia']
            num_ext = request.POST['num_ext']
            cp = request.POST['cp']
            col_mun = request.POST['col_mun']
            pais = request.POST['pais']
            num_tel = request.POST['num_tel']
            mun_cel = request.POST['mun_cel']
            curp = request.POST['curp']
            t_sangre = request.POST['t_sangre']
            rfc = request.POST['rfc']
            n_seg_social = request.POST['n_seg_social']
            imagen = request.FILES['imagen'] 
            permiso = 0
            cambio = 0 

            imagen_bytes = imagen.read()
            usuario = Usuario(calle=calle, colonia=colonia, num_ext=num_ext, cp=cp, col_mun= col_mun, pais=pais,  num_tel=num_tel, mun_cel= mun_cel, curp=curp, t_sangre=t_sangre, rfc=rfc, n_seg_social=n_seg_social, imagen=imagen_bytes,id_id=user.id,permiso = permiso, cambio= cambio)
            username = user.username  # Asignar el valor del nombre de usuario del usuario actual
#<-----------------Guarda en el Historial------------------------->
            historial= Historial.objects.all()
            historial = Historial(movimiento='Nuevo Usuario',usuario=request.user.username, fecha=timezone.now(),nombre=username)
            historial.save()
            usuario.save()

            # Envío de correo de bienvenida
            subject = 'Bienvenido a nuestra aplicación'
            from_email = 'stockmaster404@gmail.com'
            recipient_list = [email]

            accept_link = 'http://127.0.0.1:8000/signin/?next=/actividades/'

            # Crear el mensaje en formato HTML
            message_html = render_to_string('StockMaster_app/Correo.html', {'accept_link': accept_link})

            try:
                send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message_html)
                messages.success(request, 'Usuario registrado y correo de bienvenida enviado correctamente.')
            except Exception as e:
                print(f'Error al enviar el correo de bienvenida: {e}')
                messages.error(request, f'Error al enviar el correo de bienvenida: {e}')

            # Agregar entrada al historial
            username = user.username
            historial = Historial(movimiento='Nuevo Usuario', usuario=request.user.username, fecha=timezone.now(), nombre=username)
            historial.save()

            return redirect('/usuarios')
        else:
         if 'email' in form.errors:
                messages.error(request, 'error en la escritura de gmail recomendacion "@gmail.com" "@hotmail.com" "outlook.com"')
            
         if 'username' in form.errors:
                messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
         else:
                messages.error(request, 'La contraseña debe de tener más de 8 caracteres y no deben ser numeros continuos')
         if 'is_superuser' in form.errors:
                messages.error(request, 'error de admin')
        return redirect('/usuarios')  
            

    else:
        form = CustomUserCreationForm()

    return render(request, 'StockMaster_app/usuarios.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect('/actividades')
    return render(request, 'registration/login.html')

@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('home')
@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#--------------------------------------------------------- U S U A R I O S --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#ya cambia la contra
@login_required(login_url='signin')
def cambio_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Actualiza la sesión del usuario para evitar que se cierre la sesión después de cambiar la contraseña
            update_session_auth_hash(request, user)
            return redirect('/actividades')  # Reemplaza 'perfil' con la URL a la que deseas redirigir al usuario después de cambiar la contraseña
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'StockMaster_app/cambio_contraseña.html', {'form': form})

def eliminaruser(request, id):
    try:
        user_to_delete = User.objects.get(id=id)
        user_to_delete.delete()
        return redirect('/usuarios')
    except User.DoesNotExist:
        # Maneja el caso en que el usuario con el ID especificado no existe
        # Puedes mostrar un mensaje de error o realizar alguna otra acción aquí
        pass

#____________________________________________________________________________________________________________________________________

#---------------------------------------------------------- P R O D U C T O S ------------------------------------------------------>
#____________________________________________________________________________________________________________________________________

#Visualizar Producto
@login_required(login_url='signin')
def pro(request):
    if request.user.has_perm('StockMaster_app.view_productos'):
        mensajes = Mensajes.objects.all()
        cantidad_mensajes =mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        ProveedoresListados = Proveedores.objects.all()
        MarcaListados = Marca.objects.all() 
        form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
        usuario = form.count()
        cantidad_marcas = MarcaListados.count()
        cantidad_productos = ProductosListados.count()
        cantidad_categorias = CategoriaListados.count()
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)
        return render(request, 'StockMaster_app/productos.html', {
            "Productos": ProductosListados,
            "Categoria": CategoriaListados,
            'marca': MarcaListados,
            'Proveedor': ProveedoresListados,
            'Mensajes': mensajes,
            'cantidad_mensajes': cantidad_mensajes,
            'usuarios': usuario,
            'Usuario': form,
            'cantidad_productos': cantidad_productos,
            'cantidad_categorias': cantidad_categorias,
            'cantidad_marcas': cantidad_marcas,
        })    
    else:
        return redirect('/actividades')
    
def get_imagen_url(imagen_binaria):
    imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
    return f"data:image/jpeg;base64,{imagen_base64}"
#Registrar Poducto

@login_required(login_url='signin')
def registrarProducto(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    precio = request.POST['NumPrecio']
    cantPro = request.POST['CantPro'] 
    imagen = request.FILES['imagen'] 
    categoria_id = request.POST['categoria']
    idProveedor = request.POST['proveedor']
    marca_id = request.POST['marca']

    # Comprobar si el producto ya existe marca=marca
    if Productos.objects.filter(codigo=codigo).exists():
        messages.error(request, '¡El producto con este código ya existe!')
    elif Productos.objects.filter( nombre=nombre).exists():
        messages.error(request, 'Este producto ya existe!')
    else:
        # Leer los datos de la imagen como bytes
        imagen_bytes = imagen.read()
        
        # Crear una instancia de Producto con los datos proporcionados, incluyendo la imagen como bytes
        producto = Productos(codigo=codigo, nombre=nombre, precio=precio, cantPro=cantPro, imagen=imagen_bytes, id_categorias_id=categoria_id,username=request.user.username,fecha_edit = timezone.now(),movimiento='Producto creado', id_Proveedores_id=idProveedor, id_marca_id= marca_id)
        # Guardar la instancia en la base de datos
        historial= Historial.objects.all()
        historial = Historial(movimiento='Producto Creado',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
        historial.save()
        producto.save()
        messages.success(request, '¡Producto registrado!')
    return redirect('/productos/')

#Editar Producto
@login_required(login_url='signin')
def editarProductoMod(request):
    try:
        idproducts = request.POST.get('productId')
        codigo = request.POST.get('txtCodigo')
        nombre = request.POST.get('txtNombre')
        precio = request.POST.get('NumPrecio')
        cantPro = request.POST.get('CantPro')
        nueva_imagen = request.FILES.get('imagen') 
        categoria_id = request.POST.get('categoria') 
        idProveedor = request.POST.get('proveedor')
        marca_id = request.POST.get('marca')
        
        try:
            productos = Productos.objects.get(idproducts=idproducts)
        except ObjectDoesNotExist:
            messages.error(request, 'El producto no se encontró o no existe.')
            return redirect('/productos/')  # Puedes redirigir a donde desees
        if Productos.objects.filter(nombre=nombre, codigo=codigo, precio=precio, cantPro=cantPro, id_categorias_id=categoria_id, id_Proveedores_id=idProveedor, id_marca_id=marca_id).exists():
            if nueva_imagen:
                productos.codigo = codigo
                productos.nombre = nombre
                productos.precio = precio
                productos.cantPro = cantPro
                productos.username = request.user.username
                productos.movimiento = 'Edicion de Producto'
                productos.fecha_edit = timezone.now()
                productos.id_categorias_id = categoria_id
                productos.id_Proveedores_id = idProveedor
                productos.id_marca_id= marca_id
                productos.imagen = nueva_imagen.read()
                historial = Historial(movimiento='Edicion de Producto', usuario=request.user.username, fecha=timezone.now(), nombre=nombre)
                historial.save()
                productos.save()

                messages.success(request, '¡Producto Editado!')
                return redirect('/productos/')
            else:
                messages.error(request, '¡Este Producto no recibio cambios!')
                return redirect('/productos/')
        else:
            productos.codigo = codigo
            productos.nombre = nombre
            productos.precio = precio
            productos.cantPro = cantPro
            productos.username = request.user.username
            productos.movimiento = 'Edicion de Producto'
            productos.fecha_edit = timezone.now()
            productos.id_categorias_id = categoria_id
            productos.id_Proveedores_id = idProveedor
            productos.id_marca_id= marca_id
            if nueva_imagen:
                productos.imagen = nueva_imagen.read()
            historial = Historial(movimiento='Edicion de Producto', usuario=request.user.username, fecha=timezone.now(), nombre=nombre)
            historial.save()
            productos.save()

            messages.success(request, '¡Producto Editado!')
            return redirect('/productos/')
    except ObjectDoesNotExist:
        messages.error(request, 'El producto no se encontró o no existe.')
        return redirect('/productos/')  # Puedes redirigir a donde desees
    
@login_required(login_url='signin')
def edicioninventario2(request, idproducts):

    productos = Productos.objects.get(idproducts=idproducts)
    ProveedorListados = Proveedores.objects.all()
    MarcaListado = Marca.objects.all()
    imagen_url = get_imagen_url(productos.imagen)
    
     # Filtra las categorías con status igual a 1 (activas)
    CategoriaListados = Categoria.objects.filter(status=True)

    # Verifica si el producto tiene una categoría válida
    if productos.id_categorias:
        id_categorias = productos.id_categorias.categoria_id
    else:
        id_categorias = None

    data = {
        "codigo": productos.codigo,
        "nombre": productos.nombre,
        "precio": productos.precio,
        "cantPro": productos.cantPro,
        "id_categorias": productos.id_categorias.categoria_id if productos.id_categorias is not None else None,
        "id_Proveedores": productos.id_Proveedores.idProveedor if productos.id_Proveedores is not None else None,
        "id_marca": productos.id_marca.marca_id if productos.id_marca is not None else None,
        "imagen_url": imagen_url,
        "Categoria": [{"categoria_id": c.categoria_id, "nombre": c.nombre} for c in CategoriaListados],
        "Proveedor": [{"idProveedor": c.idProveedor, "nombre": c.nombre} for c in ProveedorListados],
        "Marca": [{"id_marca": c.marca_id, "nombre": c.nombre} for c in MarcaListado]
    }
    return JsonResponse(data)
    return render(request, 'StockMaster_app/productos.html', data)

#Recuperar Producto
@login_required(login_url='signin')
def cambio_statusre(request, idproducts):
   producto = Productos.objects.get(idproducts=idproducts)
   if producto.status != 1:
        producto.status = 1
        if producto.status_mov !=1:
            producto.status_mov = 1

        producto.fecha_edit = timezone.now()
        producto.username = request.user.username
        producto.movimiento = 'Recuperacion de Producto'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Recuperacion de Producto',usuario=request.user.username,fecha=timezone.now(),nombre=producto.nombre)
        historial.save()
        producto.save()
   messages.success(request, '¡Producto recuperado¡')
   return redirect('/recuperar_producto')

#Eliminar Producto
@login_required(login_url='signin')
def cambio_status(request, idproducts):
    producto = Productos.objects.get(idproducts=idproducts)
    messages.success(request, '¡Producto Eliminado!')
    if producto.status != 0:
        producto.status = 0
        if producto.status_mov !=1:
            producto.status_mov = 1
        producto.fecha_edit = timezone.now()
        producto.username = request.user.username
        producto.movimiento = 'Eliminacion de Producto'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Producto',usuario=request.user.username,fecha=timezone.now(),nombre=producto.nombre)
        historial.save()
        producto.save()
    return redirect('/productos')

@login_required(login_url='signin')
def eliminaInventario(request, idproducts):
    productos = Productos.objects.get(idproducts=idproducts)
    historial= Historial.objects.all()
    historial = Historial(movimiento='¡Producto Eliminado!',usuario=request.user.username,fecha=timezone.now(),nombre=productos.nombre)
    historial.save()
    productos.delete()
    messages.success(request, '¡Producto Eliminado!')
    return redirect('/recuperar_producto')

#____________________________________________________________________________________________________________________________________

#---------------------------------------------------------- P R O V E E D O R E S -------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Proveedor
@login_required(login_url='signin')
def prov(request):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
        mensajes = Mensajes.objects.all()
        cantidad_mensajes = mensajes.count()
        ProveedoresListados = Proveedores.objects.all()
        for proveedor in ProveedoresListados:
            proveedor.imagen_url = get_imagen_url(proveedor.imagen)
        return render(request, 'StockMaster_app/proveedor.html', { "Proveedor": ProveedoresListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/actividades')

#Registrar Proveedor
@login_required(login_url='signin')
def registrarProv(request):
    nombreProv = request.POST['NombreProv']
    contactoProv = request.POST['ContactoProv']
    telefonoProv = request.POST['TelefonoProv']
    emailProv = request.POST['EmailProv'] 
    imagenProv = request.FILES['imagenProv'] 
    calle = request.POST['Calle']
    noExt = request.POST['NoExt']
    noInt = request.POST['NoInt']
    colonia = request.POST['Colonia']
    cp = request.POST['CP']
    municipio = request.POST['Municipio']
    estado = request.POST['Estado']
    pais = request.POST['Pais']
    status_mov = 1

    # Comprobar si el producto ya existe
    if Proveedores.objects.filter(nombre=nombreProv).exists():
        messages.error(request, '¡El proveedor ya esta registrado!')
    else:
        # Leer los datos de la imagen como bytes
        imagen_bytes = imagenProv.read()
        
        # Crear una instancia de Producto con los datos proporcionados, incluyendo la imagen como bytes
        prov = Proveedores(nombre=nombreProv, contacto=contactoProv, telefono=telefonoProv, email=emailProv, calle=calle, noExt=noExt, noInt=noInt, colonia=colonia, cp=cp, municipio=municipio, estado=estado, pais=pais, imagen=imagen_bytes,username=request.user.username,movimiento='Registro de Proveedor',status_mov=status_mov)
        # Guardar la instancia en la base de datos
        historial= Historial.objects.all()
        historial = Historial(movimiento='Registro de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=prov.nombre)
        historial.save()
        prov.save()
        messages.success(request, '¡Proveedor registrado!')
    return redirect('/prov/')

#Editar Proveedor
@login_required(login_url='signin')
def editarProveedorMod(request):
    try:
        idProveedor = request.POST.get('productId')
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        calle = request.POST.get('calle')
        noExt = request.POST.get('noExt') 
        noInt = request.POST.get('noInt') 
        colonia = request.POST.get('colonia')
        cp = request.POST.get('cp')
        municipio = request.POST.get('municipio')
        estado = request.POST.get('estado')
        nueva_imagen = request.FILES.get('imagen') 
        pais = request.POST.get('pais')
        try:
            proveedor = Proveedores.objects.get(idProveedor=idProveedor)
        except ObjectDoesNotExist:
            messages.error(request, 'El producto no se encontró o no existe.')
            return redirect('/prov/')  # Puedes redirigir a donde desees
        if Proveedores.objects.filter(nombre=nombre, contacto=contacto, telefono=telefono, email=email, calle=calle, noExt=noExt, noInt=noInt, colonia=colonia, cp=cp, municipio=municipio, estado=estado, pais=pais).exists():
            if nueva_imagen:
                proveedor.nombre = nombre
                proveedor.contacto = contacto
                proveedor.telefono = telefono
                proveedor.email = email
                proveedor.calle = calle
                proveedor.noExt = noExt
                proveedor.noInt = noInt
                proveedor.colonia = colonia
                proveedor.cp = cp
                proveedor.municipio = municipio
                proveedor.estado = estado
                proveedor.pais = pais

                proveedor.username = request.user.username
                proveedor.fecha_edit = timezone.now()
                proveedor.movimiento = 'Edicion de Proveedor'
                if proveedor.status_mov != 1:
                    proveedor.status_mov = 1
                if nueva_imagen:
                    proveedor.imagen = nueva_imagen.read()
                historial= Historial.objects.all()
                historial = Historial(movimiento='Edicion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
                historial.save()
                proveedor.save()

                messages.success(request, '¡Proveedor Editado!')
                return redirect('/prov/')
            else:
                messages.error(request, '¡Este Proveedor no recibio cambios!')
                return redirect('/prov/') 
        else:
            proveedor.nombre = nombre
            proveedor.contacto = contacto
            proveedor.telefono = telefono
            proveedor.email = email
            proveedor.calle = calle
            proveedor.noExt = noExt
            proveedor.noInt = noInt
            proveedor.colonia = colonia
            proveedor.cp = cp
            proveedor.municipio = municipio
            proveedor.estado = estado
            proveedor.pais = pais

            proveedor.username = request.user.username
            proveedor.fecha_edit = timezone.now()
            proveedor.movimiento = 'Edicion de Proveedor'
            if proveedor.status_mov != 1:
                proveedor.status_mov = 1
            if nueva_imagen:
                proveedor.imagen = nueva_imagen.read()
            historial= Historial.objects.all()
            historial = Historial(movimiento='Edicion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
            historial.save()
            proveedor.save()

            messages.success(request, '¡Proveedor Editado!')
            return redirect('/prov/')
    except ObjectDoesNotExist:
        messages.error(request, 'El proveedor no se encontró o no existe.')
        return redirect('/prov/')  # Puedes redirigir a donde desees
 #eliminar proveedor (se cambia el estatus a 0)

@login_required(login_url='signin')
def edicionProveedor2(request, idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor)
    imagen_url = get_imagen_url(proveedor.imagen)

    data = {

        "nombre" : proveedor.nombre,
        "contacto" : proveedor.contacto,
        "telefono" : proveedor.telefono,
        "email" : proveedor.email,
        "calle" : proveedor.calle,
        "noExt" : proveedor.noExt,
        "noInt" : proveedor.noInt, 
        "colonia" : proveedor.colonia,
        "cp" : proveedor.cp,
        "municipio" : proveedor.municipio,
        "estado" : proveedor.estado,
        "pais" : proveedor.pais,
        "imagen_url": imagen_url,
    }

    #return JsonResponse(data)    
    #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
    return JsonResponse(data)
    return render(request, 'StockMaster_app/proveedor.html', data)

#Recuperar Proveedor
@login_required(login_url='signin')
def cambio_statusrepro(request,idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor)
    if proveedor.status != 1:
        proveedor.status = 1
        if proveedor.status_mov !=1:
            proveedor.status_mov = 1
        proveedor.fecha_edit = timezone.now()
        proveedor.username = request.user.username
        proveedor.movimiento = 'Recuperacion de Proveedor'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Recuperacion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
        historial.save()
        proveedor.save()
    messages.success(request, '¡Proveedor Recuperado¡')
    return redirect('/recuperar_proveedor')

#Eliminar Proveedor
@login_required(login_url='signin')
def cambio_statuspro(request, idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor)
    messages.success(request, '¡Proveedor Eliminado!')
    if proveedor.status != 0:
        proveedor.status = 0
        if proveedor.status_mov !=1:
            proveedor.status_mov = 1
        proveedor.fecha_edit = timezone.now()
        proveedor.username = request.user.username
        proveedor.movimiento = 'Eliminacion de Proveedor'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
        historial.save()
        proveedor.save()
    return redirect('/prov')

@login_required(login_url='signin')
def eliminaProveedor(request, idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor)
    historial= Historial.objects.all()
    historial = Historial(movimiento='¡Proveedor Eliminado!',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
    historial.save()
    Productos.objects.filter(id_Proveedores=proveedor).update(id_Proveedores=None)
    proveedor.delete()
    messages.success(request, '¡Proveedor Eliminado!')
    return redirect('/recuperar_proveedor')

#____________________________________________________________________________________________________________________________________

#---------------------------------------------------------- C A T E G O R I A S ---------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Categoria
@login_required(login_url='signin')
def configuraciones(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        mensajes = Mensajes.objects.all()
        cantidad_mensajes =mensajes.count()
        CategoriaListados = Categoria.objects.all()
        MarcaListados = Marca.objects.all()
        return render(request, 'StockMaster_app/configuraciones.html',{"Categoria": CategoriaListados,"Marca":MarcaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/actividades')

#Registrar Categoria
@login_required(login_url='signin')
def registrar_categoria(request):
        
    nombre = request.POST['txtNombreCat']

        # Comprobar si la categoría ya existe
    if Categoria.objects.filter(nombre=nombre).exists():
        messages.error(request, '¡Esta categoría ya existe!')
    else:
            # Crear una nueva instancia de Categoria con el nombre proporcionado
        categoria = Categoria(nombre=nombre,username=request.user.username,fech_cate=timezone.now(),movi='Creacion de Categoria')
        historial= Historial.objects.all()
        historial = Historial(movimiento='Categoria Agregada',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
        historial.save() 
            # Guardar la instancia en la base de datos
        categoria.save()
            
        messages.success(request, '¡Categoría registrada con éxito!')

    # Redireccionar a la página de categorías después del registro
    return redirect('etiquetas')

#Editar Categoria
@login_required(login_url='signin')
def editarCategoriaMod(request):
    try:
        categoria_id = request.POST.get('productId')
        nombre = request.POST.get('nombre')
        try:
            categoria = Categoria.objects.get(categoria_id= categoria_id)
        except ObjectDoesNotExist:
            messages.error(request, 'El producto no se encontró o no existe.')
            return redirect('/config/')  # Puedes redirigir a donde desees
        
        if Categoria.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡Esta categoría no recibio cambios!')
            return redirect('/config/') 
        else:
            categoria.nombre = nombre

            categoria.username = request.user.username
            categoria.movi = 'Edicion de Categoria'
            categoria.fech_cate = timezone.now()
            if categoria.status_mov !=1:
                categoria.status_mov = 1 
            historial= Historial.objects.all()
            historial = Historial(movimiento='Edicion de Categoria',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
            historial.save()
            categoria.save()

            messages.success(request, '¡Categoria  Editada!')
            return redirect('/config/') 
    except ObjectDoesNotExist:
        messages.error(request, 'La categoria no se encontró o no existe.')
        return redirect('/config/')  # Puedes redirigir a donde desees

@login_required(login_url='signin')
def edicionCategoria2(request, categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)

    data = {
        "nombre" : categoria.nombre,
    }

    #return JsonResponse(data)    
    #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
    return JsonResponse(data)
    return render(request, 'StockMaster_app/configuraciones.html', data)

#Recuperar Categoria
@login_required(login_url='signin')
def status_categoriare(request,categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)
    if categoria.status !=1:
            categoria.status=1
            categoria.fech_cate = timezone.now()
            categoria.movi = 'Recuperacion de Categoria'
            categoria.username = request.user.username
            if categoria.status_mov != 1:
                categoria.status_mov = 1
            historial= Historial.objects.all()
            historial = Historial(movimiento='Recuperacion de Categoria',usuario=request.user.username,fecha=timezone.now(),nombre=categoria.nombre)
            historial.save()
            categoria.save()
            messages.success(request, '¡Categoría Recuperada!')
    """ return redirect('/recuperar_producto') """
    return redirect('/recuperar_categoria')

#Eliminar Categoria
@login_required(login_url='signin')
def status_categoria(request,categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)
    if categoria.status !=0:
        categoria.status=0
        categoria.fech_cate = timezone.now()
        categoria.movi = 'Eliminacion de Categoria'
        categoria.username = request.user.username
        if categoria.status_mov != 1:
            categoria.status_mov = 1
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Categoria',usuario=request.user.username,fecha=timezone.now(),nombre=categoria.nombre)
        historial.save()
        categoria.save()
        messages.success(request, '¡Categoría Eliminada!')
    return redirect('/recuperar_etiquetas')

@login_required(login_url='signin')
def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)
    Productos.objects.filter(id_categorias=categoria).update(id_categorias=None)
    historial= Historial.objects.all()
    historial = Historial(movimiento='¡Categoria Eliminada!',usuario=request.user.username,fecha=timezone.now(),nombre=categoria.nombre)
    historial.save()
    Productos.objects.filter(id_categorias=categoria).update(id_categorias=None)
    categoria.delete()
    messages.success(request, '¡Categoría Eliminada!')
    return redirect('/recuperar_etiquetas')  # O redirige a donde desees después de la eliminación

#____________________________________________________________________________________________________________________________________

#-------------------------------------------------------------- M A R C A S -------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Marca
@login_required(login_url='signin')
def MarcaView(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    MarcaListados = Marca.objects.all()
    CategoriaListados = Categoria.objects.all()
    return render(request, 'StockMaster_app/configuraciones.html', {"Marca": MarcaListados,"Categoria": CategoriaListados,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes})

#Registrar Marca
@login_required(login_url='signin')
def registrar_marca(request):
    nombre = request.POST['txtMarcaNew']
        
    if Marca.objects.filter(nombre=nombre).exists():
        messages.error(request, 'La marca ya está registrada.')
    else:
        marca = Marca(nombre=nombre, username=request.user.username, fech_cate=timezone.now(), movi='Creación de Marca')
        historial = Historial(movimiento='Marca Agregada', usuario=request.user.username, fecha=timezone.now(), nombre=nombre)
        historial.save()
        marca.save()
        messages.success(request, '¡Marca registrada con éxito!')
    return HttpResponseRedirect('/config/')  # Redirige a la URL deseada después de procesar el formulario

#Editar Marca
@login_required(login_url='signin')
def editarMarcaMod(request):
    try:
        marca_id = request.POST.get('productId')
        nombre = request.POST.get('nombre')
        try:
            marca = Marca.objects.get(marca_id= marca_id)
        except ObjectDoesNotExist:
            messages.error(request, 'El producto no se encontró o no existe.')
            return redirect('/config/')  # Puedes redirigir a donde desees
        if Marca.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡Esta Marca no recibio cambios!')
            return redirect('/config/') 
        else:
            marca.nombre = nombre

            marca.username = request.user.username
            marca.movi = 'Edicion de Marca'
            marca.fech_cate = timezone.now()
            if marca.status_mov !=1:
                marca.status_mov = 1 
            historial= Historial.objects.all()
            historial = Historial(movimiento='Edicion de Marca',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
            historial.save()
            marca.save()

            messages.success(request, '¡Marca  Editada!')
            return redirect('/config/') 
    except ObjectDoesNotExist:
        messages.error(request, 'La categoria no se encontró o no existe.')
        return redirect('/config/')  # Puedes redirigir a donde desees

@login_required(login_url='signin')
def edicionMarca2(request, marca_id):
    marca = Marca.objects.get(marca_id= marca_id)
    
    data = {
        "nombre" : marca.nombre,
    }

    #return JsonResponse(data)    
    #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
    return JsonResponse(data)
    return render(request, 'StockMaster_app/configuraciones.html', data)

#Recuperar Marca
@login_required(login_url='signin')
def cambio_statusremar(request,marca_id):
    marca = Marca.objects.get(marca_id= marca_id)
    if marca.status != 1:
        marca.status = 1
        if marca.status_mov !=1:
            marca.status_mov = 1
        marca.fech_cate = timezone.now()
        marca.username = request.user.username
        marca.movi = 'Recuperacion de marca'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Recuperacion de Marca',usuario=request.user.username,fecha=timezone.now(),nombre=marca.nombre)
        historial.save()
        marca.save()
    messages.success(request, '¡Marca Recuperada¡')
    return redirect('/recuperar_etiquetas')

#Eliminar Marca
@login_required(login_url='signin')
def cambio_statusmar(request,marca_id):
    marca = Marca.objects.get(marca_id= marca_id)
    if marca.status != 0:
        marca.status = 0
        if marca.status_mov !=1:
            marca.status_mov = 1
        marca.fech_cate = timezone.now()
        marca.username = request.user.username
        marca.movi = "Eliminacion de Marca"
        historial = Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Marca',usuario=request.user.username,fecha=timezone.now(),nombre=marca.nombre)
        historial.save()
        marca.save()
    messages.success(request, '¡Marca Eliminada¡')
    return redirect('/config')

@login_required(login_url='signin')
def eliminar_marca(request, marca_id):
    marca = Marca.objects.get(marca_id=marca_id)
    historial= Historial.objects.all()
    historial = Historial(movimiento='¡Marca Eliminada!',usuario=request.user.username,fecha=timezone.now(),nombre=marca.nombre)
    historial.save()
    Productos.objects.filter(id_marca=marca).update(id_marca=None)
    marca.delete()
    messages.success(request, '¡Marca Eliminada!')
    return redirect('/recuperar_etiquetas')  # O redirige a donde desees después de la eliminación

#____________________________________________________________________________________________________________________________________

#----------------------------------------------------------------- R O L E S ------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Rol
@login_required(login_url='signin')
def RolView(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    roles = Group.objects.all()
    roles_con_status_1 = [rol for rol in roles if RolExtra.objects.get(grupo=rol).status == 1]
    return render(request, 'StockMaster_app/roles.html', {"Roles": roles_con_status_1,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes})

#Registrar Rol
@login_required(login_url='signin')
def registrar_rol(request):
    nombre = request.POST['RolNew']
    principal = request.POST['principal']
    inventario = request.POST['inventario']
    productos = request.POST['productos']
    proveedores = request.POST['proveedores']
    etiquetas = request.POST['etiquetas']
    productosRecuperacion = request.POST['productosRecuperacion']
    proveedoresRecuperacion = request.POST['proveedoresRecuperacion']
    etiquetasRecuperacion = request.POST['etiquetasRecuperacion']
    usuarios = request.POST['usuarios']
    roles = request.POST['roles']
    soporte = request.POST['soporte']
    if Group.objects.filter(name=nombre).exists():
        messages.error(request, 'El Rol ya está registrado.')
    else:
        rol = Group(name=nombre)
        rol.save()
        rol_extra = RolExtra()
        rol_extra.grupo = rol
        # Aquí es donde agregas los permisos
        rol_extra.principal = principal
        rol_extra.inventario = inventario
        rol_extra.productos = productos
        rol_extra.proveedores = proveedores
        rol_extra.productosRecuperacion = productosRecuperacion 
        rol_extra.proveedoresRecuperacion = proveedoresRecuperacion 
        rol_extra.etiquetasRecuperacion = etiquetasRecuperacion
        rol_extra.usuarios = usuarios
        rol_extra.roles = roles
        rol_extra.soporte = soporte 
        if principal=='1':
            permiso = Permission.objects.get(codename='view_marca')
            rol.permissions.add(permiso)
        if inventario=='1':
            permiso = Permission.objects.get(codename='delete_marca')
            rol.permissions.add(permiso)
        if productos=='1':
            permiso = Permission.objects.get(codename='view_productos')
            rol.permissions.add(permiso)
        if proveedores=='1':
            permiso = Permission.objects.get(codename='view_proveedores')
            rol.permissions.add(permiso)
        if etiquetas=='1':
            permiso = Permission.objects.get(codename='view_categoria')
            rol.permissions.add(permiso)
        if productosRecuperacion=='1':
            permiso = Permission.objects.get(codename='delete_productos')
            rol.permissions.add(permiso)
        if proveedoresRecuperacion=='1':
            permiso = Permission.objects.get(codename='delete_proveedores')
            rol.permissions.add(permiso)
        if etiquetasRecuperacion=='1':
            permiso = Permission.objects.get(codename='delete_categoria')
            rol.permissions.add(permiso)
        if usuarios=='1':
            permiso = Permission.objects.get(codename='view_usuario')
            rol.permissions.add(permiso)
        if roles=='1':
            permiso = Permission.objects.get(codename='view_rolextra')
            rol.permissions.add(permiso)
        if soporte=='1':
            permiso = Permission.objects.get(codename='view_mensajes')
            rol.permissions.add(permiso)
        rol_extra.save()
        historial = Historial(movimiento='Rol Agregado', usuario=request.user.username, fecha=timezone.now(), nombre=rol.name)
        historial.save()
        
        messages.success(request, '¡Rol registrado con éxito!')
    return HttpResponseRedirect('/rol/')  # Redirige a la URL deseada después de procesar el formulario



#Editar Rol
@login_required(login_url='signin')
def editarRolMod(request):
    try:
        id = request.POST.get('productId')
        nombre = request.POST.get('nombre')
        principal = request.POST['principal']
        inventario = request.POST['inventario']
        productos = request.POST['productos']
        proveedores = request.POST['proveedores']
        etiquetas = request.POST['etiquetas']
        productosRecuperacion = request.POST['productosRecuperacion']
        proveedoresRecuperacion = request.POST['proveedoresRecuperacion']
        etiquetasRecuperacion = request.POST['etiquetasRecuperacion']
        usuarios = request.POST['usuarios']
        roles = request.POST['roles']
        soporte = request.POST['soporte']

        try:
            rol = Group.objects.get(id= id)
            rol_extra = RolExtra.objects.get(grupo=rol)
            context = {
                'rol': rol,
                'rol_extra': rol_extra,
            }
        except RolExtra.DoesNotExist:
            messages.error(request, 'El Rol no se encontró o no existe.')
            return redirect('/rol/')  # Puedes redirigir a donde desees
        if Group.objects.filter(name=nombre).exists():
            messages.error(request, '¡Este Rol no recibio cambios!')
            return redirect('/rol/') 
        else:
            rol.name = nombre
            rol.save()
            rol_extra.principal = principal
            rol_extra.inventario = inventario
            rol_extra.productos = productos
            rol_extra.proveedores = proveedores
            rol_extra.etiquetas = etiquetas
            rol_extra.productosRecuperacion = productosRecuperacion
            rol_extra.proveedoresRecuperacion = proveedoresRecuperacion
            rol_extra.etiquetasRecuperacion = etiquetasRecuperacion
            rol_extra.usuarios = usuarios
            rol_extra.roles = roles
            rol_extra.soporte = soporte

            if principal=='1':
                permiso = Permission.objects.get(codename='view_marca')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_marca')
                rol.permissions.remove(permiso)
            if inventario=='1':
                permiso = Permission.objects.get(codename='delete_marca')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='delete_marca')
                rol.permissions.remove(permiso)
            if productos=='1':
                permiso = Permission.objects.get(codename='view_productos')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_productos')
                rol.permissions.remove(permiso)
            if proveedores=='1':
                permiso = Permission.objects.get(codename='view_proveedores')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_proveedores')
                rol.permissions.remove(permiso)
            if etiquetas=='1':
                permiso = Permission.objects.get(codename='view_categoria')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_categoria')
                rol.permissions.remove(permiso)
            if productosRecuperacion=='1':
                permiso = Permission.objects.get(codename='delete_productos')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='delete_productos')
                rol.permissions.remove(permiso)
            if proveedoresRecuperacion=='1':
                permiso = Permission.objects.get(codename='delete_proveedores')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='delete_proveedores')
                rol.permissions.remove(permiso)
            if etiquetasRecuperacion=='1':
                permiso = Permission.objects.get(codename='delete_categoria')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='delete_categoria')
                rol.permissions.remove(permiso)
            if usuarios=='1':
                permiso = Permission.objects.get(codename='view_usuario')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_usuario')
                rol.permissions.remove(permiso)
            if roles=='1':
                permiso = Permission.objects.get(codename='view_roles')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_roles')
                rol.permissions.remove(permiso)
            if soporte=='1':
                permiso = Permission.objects.get(codename='view_mensajes')
                rol.permissions.add(permiso)
            else:
                permiso = Permission.objects.get(codename='view_mensajes')
                rol.permissions.remove(permiso)

            rol_extra.username = request.user.username
            rol_extra.movi = 'Edicion de Marca'
            rol_extra.fech_cate = timezone.now()
            if rol_extra.status_mov !=1:
                rol_extra.status_mov = 1 
            historial= Historial.objects.all()
            historial = Historial(movimiento='Edicion de Rol',usuario=request.user.username,fecha=timezone.now(),nombre=rol.name)
            historial.save()
            rol_extra.save()

            messages.success(request, '¡Marca  Editada!')
            return redirect('/rol/') 
    except ObjectDoesNotExist:
        messages.error(request, 'El rol no se encontró o no existe.')
        return redirect('/rol/')  # Puedes redirigir a donde desees

@login_required(login_url='signin')
def edicionRol2(request, id):
    rol = Group.objects.get(id= id)
    rol_extra = RolExtra.objects.get(grupo=rol)
    data = {
        "nombre" : rol.name,
        "principal": rol_extra.principal,
        "inventario": rol_extra.inventario,
        "productos":rol_extra.productos,
        "proveedores":rol_extra.proveedores,
        "etiquetas":rol_extra.etiquetas,
        "productosRecuperacion":rol_extra.productosRecuperacion,
        "proveedoresRecuperacion":rol_extra.proveedoresRecuperacion,
        "etiquetasRecuperacion":rol_extra.etiquetasRecuperacion,
        "usuarios":rol_extra.usuarios,
        "roles": rol_extra.roles,
        "soporte":rol_extra.soporte
    }

    #return JsonResponse(data)    
    #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
    return JsonResponse(data)
    return render(request, 'StockMaster_app/roles.html', data)

#Recuperar Rol
@login_required(login_url='signin')
def cambio_statusrolre(request,id):
    rol = Group.objects.get(id= id)
    rol_extra = RolExtra.objects.get(grupo=rol)
    if rol_extra.status != 1:
        rol_extra.status = 1
        if rol_extra.status_mov !=1:
            rol_extra.status_mov = 1
        rol_extra.fech_cate = timezone.now()
        rol_extra.username = request.user.username
        rol_extra.movi = 'Recuperacion de marca'
        historial= Historial.objects.all()
        historial = Historial(movimiento='Recuperacion de Rol',usuario=request.user.username,fecha=timezone.now(), nombre=rol.name)
        historial.save()
        rol_extra.save()
    messages.success(request, '¡Rol Recuperado¡')
    return redirect('/recuperar_producto')

#Eliminar Rol
@login_required(login_url='signin')
def cambio_statusrol(request,id):
    rol = Group.objects.get(id= id)
    rol_extra = RolExtra.objects.get(grupo=rol)
    if rol_extra.status != 0:
        rol_extra.status = 0
        if rol_extra.status_mov !=1:
            rol_extra.status_mov = 1
        rol_extra.fech_cate = timezone.now()
        rol_extra.username = request.user.username
        rol_extra.movi = "Eliminacion de Rol"
        historial = Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Rol',usuario=request.user.username,fecha=timezone.now(), nombre=rol.name)
        historial.save()
        rol.save()
        rol_extra.save()
    messages.success(request, '¡Rol Eliminado¡')
    return redirect('/rol/')

@login_required(login_url='signin')
def eliminar_rol(request, id):
    rol = Group.objects.get(id= id)
    historial= Historial.objects.all()
    historial = Historial(movimiento='¡Rol Eliminado!',usuario=request.user.username,fecha=timezone.now(),nombre=rol.name)
    historial.save()
    rol.delete()
    messages.success(request, '¡Rol Eliminado!')
    return redirect('/recuperar_producto')  # O redirige a donde desees después de la eliminación

#____________________________________________________________________________________________________________________________________

#----------------------------------------------------- C O M E N T A R I O S ------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def soporte(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    return render(request, 'StockMaster_app/soporte.html', {'Mensajes': mensajes,  'cantidad_mensajes': cantidad_mensajes})

@login_required(login_url='signin')
def comentario(request):
    if request.method == 'POST':
        comentario = request.POST.get('comentario')  # Corregir la sintaxis para obtener el valor del comentario
        username = request.user.username  # Obtener el nombre de usuario del usuario autenticado

        if comentario and username:  # Verificar que se haya proporcionado un comentario y que el usuario esté autenticado
            comentario_obj = Mensajes(comentario=comentario, username=username)
            historial= Historial.objects.all()
            historial = Historial(movimiento='Nuevo Mensaje',usuario=request.user.username,fecha=timezone.now(),nombre='Mensaje')
            historial.save()
            comentario_obj.save()
            men.success(request, 'Comentario listo!')
        else:
            men.error(request, 'Falta el comentario o el usuario no está autenticado.')

    return redirect('/soporte')

@login_required(login_url='signin')
def eliminarcomentarios(request, idcomentario):
    ecomentario = Mensajes.objects.get(idcomentario=idcomentario)
    ecomentario.delete()
    messages.success(request, '¡Producto Eliminado!')
    return redirect('/soporte')

@login_required(login_url='signin')
def respuesta(request,idcomentario):
    respuesta = Mensajes.objects.get(idcomentario=idcomentario)
    
    return render(request, "StockMaster_app/soporte.html", {"respuesta": respuesta})

@login_required(login_url='signin')
def contestarcomentarios(request,idcomentario):
    mensaje = get_object_or_404(Mensajes, idcomentario=idcomentario)
    messages.success(request, '¡Mensaje Contestado!')
    if request.method == 'POST':
        respuestascomentarios = request.POST.get('respuestascomentarios')
        mensaje.respuestascomentarios = respuestascomentarios
        mensaje.tiem_res = timezone.now()
        mensaje.admincont = request.user.username
        if mensaje.status_mov != 1:
            mensaje.status_mov = 1
        historial= Historial.objects.all()
        historial = Historial(movimiento='Mensaje Contestado',usuario=request.user.username,fecha=timezone.now(),nombre='Mensaje')
        historial.save()
        mensaje.save()
        return redirect('/soporte/')  # Redirigir a la página de soporte o a donde corresponda

    return render(request, 'StockMaster_app/soporte.html', {'mensaje': mensaje})

#____________________________________________________________________________________________________________________________________

#------------------------------------------------------- H I S T O R I A L --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def historial(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    RolListados = RolExtra.objects.all()
    historial = Historial.objects.all()
    return render(request, 'StockMaster_app/historial.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial})

@login_required(login_url='signin')
def historialModificaciones(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    RolListados = RolExtra.objects.all()
    historial = Historial.objects.filter(movimiento__in=["Edicion de Proveedor", "Edicion de Producto", "Edicion de Producto", "Edicion de Marca", "Edicion de Categoria", "Edicion de Rol"])

    return render(request, 'StockMaster_app/historialModificaciones.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial})

@login_required(login_url='signin')
def historialMovimientos(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    RolListados = RolExtra.objects.all()
    historial = Historial.objects.filter(movimiento="Rol Agregado")
    return render(request, 'StockMaster_app/historialMovimientos.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial})

@login_required(login_url='signin')
def historialEliminados(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    RolListados = RolExtra.objects.all()
    historial = Historial.objects.filter(movimiento__in=["Eliminacion de Proveedor", "Eliminacion de Producto", "Eliminacion de Producto", "Eliminacion de Marca", "Eliminacion de Categoria", "Eliminacion de Rol"])
    return render(request, 'StockMaster_app/historialEliminados.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial})


@login_required(login_url='signin')
def recuperar_producto(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    ProductosListados = Productos.objects.all()
    roles = Group.objects.all()
    roles_con_status_1 = [rol for rol in roles if RolExtra.objects.get(grupo=rol).status == 0]
    return render(request, 'StockMaster_app/recuperar_producto.html', {"Productos": ProductosListados, "Roles": roles_con_status_1,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes})

@login_required(login_url='signin')
def recuperar_proveedor(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    proveedores = Proveedores.objects.all()
    return render(request, 'StockMaster_app/recuperar_proveedor.html', { "mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"proveedores":proveedores,})

@login_required(login_url='signin')
def recuperar_etiquetas(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    CategoriaListados = Categoria.objects.all() 
    RolListados = RolExtra.objects.all()
    MarcaListados = Marca.objects.all() 
    return render(request, 'StockMaster_app/recuperar_etiquetas.html', { "Categoria": CategoriaListados, "Marca":MarcaListados, "Roles": RolListados, "mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes})

#____________________________________________________________________________________________________________________________________

#------------------------------------------------------- F U N C I O N E S --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def productos(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    ProveedoresListados = Proveedores.objects.all()
    RolListados = RolExtra.objects.all()
    MarcaListados = Marca.objects.all()
    form = User.objects.all()  
    usuario = form.count()
    cantidad_marcas = MarcaListados.count()
    cantidad_productos = ProductosListados.count()
    cantidad_proveedores =  ProveedoresListados.count()
    cantidad_categorias = CategoriaListados.count()
    productos_por_mes = Productos.objects.annotate(month=TruncMonth('hora_baja', tzinfo=pytz.UTC)).values('month').annotate(cantidad=Count('idproducts')).order_by('month')    # Crear listas para las etiquetas y datos de la gráfica
    labels = [mes['month'].strftime('%b') for mes in productos_por_mes]
    data = [mes['cantidad'] for mes in productos_por_mes]
    for producto in ProductosListados:
        producto.imagen_url = get_imagen_url(producto.imagen)
    return render(request, 'StockMaster_app/actividades.html', {
        "Productos": ProductosListados,
        "Categoria": CategoriaListados,
        'marca': MarcaListados,
        'Proveedor': ProveedoresListados,
        'Mensajes': mensajes,
        'cantidad_mensajes': cantidad_mensajes,
        'usuarios': usuario,
        'Usuario': form,
        'cantidad_productos': cantidad_productos,
        'cantidad_proveedores': cantidad_proveedores,
        'cantidad_categorias': cantidad_categorias,
        'cantidad_marcas': cantidad_marcas,
        "Roles": RolListados,
        'CategoriaListados':CategoriaListados, 
        'labels': labels,
        'data': data,
        'ProveedoresListados' : ProveedoresListados
        })

def editarcant(request, idproducts):
    if request.method == 'POST':
        cantPro = request.POST.get('cantPro')
        producto = Productos.objects.get(idproducts=idproducts)
        producto.cantPro = cantPro
        producto.username = request.user.username
        producto.fecha_edit = timezone.now()
        producto.movimiento = 'Edicion de Cantidad'
        producto.save()
        messages.success(request, '¡Cantidad Editada!')
    return redirect('/actividades')

def buscar_productos(request):
    query = request.GET.get('query', '')

    if query:
        productos = Productos.objects.filter(
            Q(codigo__icontains=query) |  # Buscar en código (contiene)
            Q(nombre__icontains=query) |  # Buscar en nombre (contiene)
            Q(marca__icontains=query) |  # Buscar en marca (contiene)
            Q(id_categorias__nombre__icontains=query)  # Buscar en nombre de categoría (contiene)
        )
    else:
        productos = Productos.objects.all()

    return render(request, 'Stockmaster_app/productos.html', {'productos': productos, 'query': query})

def get_char(_request):
    chart = {}
    return JsonResponse(chart)

@login_required(login_url='signin')
def example_view(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    productos = []  # Inicializar una lista vacía para productos
    mensajes = Mensajes.objects.all()
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    categoria_seleccionada = request.GET.get('categoria')  # Obtener la categoría seleccionada por el usuario
    if categoria_seleccionada:
        productos = Productos.objects.filter(id_categorias__nombre=categoria_seleccionada)
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    MarcaListados = Marca.objects.all() 
    for producto in ProductosListados:
        producto.imagen_url = get_imagen_url(producto.imagen)

    return render(request, 'StockMaster_app/inventario.html', {"Productos": ProductosListados, "Categoria": CategoriaListados,"Marca":MarcaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})

def enviar_correo(request):
    send_mail(
        'Asunto del Correo',
        'Cuerpo del Correo',
        'stockmaster404@gmail.com',         # Reemplaza con tu dirección de correo
        ['mayelomonti1@gmail.com'],  # Reemplaza con la dirección del destinatario
        fail_silently=False,
    )
    return HttpResponse('Correo enviado correctamente.')