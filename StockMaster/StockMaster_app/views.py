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
from .models import Productos, Mensajes, Categoria, Proveedores, Historial, Marca, Usuario, RolExtra, Area, Ordenes
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
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
# Create your views here.
from django.urls import reverse



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

def terminos(request):
    form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
    return render(request, 'registration/terminos.html', { 'Usuario': form})


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
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        usuario = Usuario.objects.all()
        roles = RolExtra.objects.all()
        form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
        grupos = Group.objects.all()  # Obtiene todos los grupos
        for Usuarios in usuario:
            Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/usuarios.html', { 'Roles':roles, 'Usuario': form, 'Mensajes':mensajes,'cantidad_mensajes':cantidad_mensajes,'usuarios':usuario, 'grupos': grupos})
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
    if request.user.has_perm('StockMaster_app.view_usuario'):
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
                mun_cel = request.POST['mun_cel']
                imagen = request.FILES['imagen'] 
                permiso = 0
                cambio = 0 

                imagen_bytes = imagen.read()
                usuario = Usuario(mun_cel= mun_cel, imagen=imagen_bytes,id_id=user.id,permiso = permiso, cambio= cambio)
                username = user.username  # Asignar el valor del nombre de usuario del usuario actual
                #<-----------------Guarda en el Historial------------------------->
                historial= Historial.objects.all()
                historial = Historial(movimiento='Creacion de Usuario',usuario=request.user.username, fecha=timezone.now(),nombre=username)
                historial.save()
                usuario.save()

                # Envío de correo de bienvenida
                subject = 'Bienvenido a nuestra aplicación'
                from_email = 'stockmaster404@gmail.com'
                recipient_list = [email]

                accept_link = 'http://127.0.0.1:8000/signin/?next=/actividades/'

                # Crear el mensaje en formato HTML
                message_html = render_to_string('StockMaster_app/correos/Correo.html', {'accept_link': accept_link})

                try:
                    send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message_html)
                    messages.success(request, 'Usuario registrado y correo de bienvenida enviado correctamente.')
                except Exception as e:
                    print(f'Error al enviar el correo de bienvenida: {e}')
                    messages.error(request, f'Error al enviar el correo de bienvenida: {e}')

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
    else:
        return redirect('/actividades')





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

#----------------------------------------------- U S U A R I O S  M O V I M I E N T O ---------------------------------------------->
#____________________________________________________________________________________________________________________________________


def cambio(request, uidb64, token):
    try:
        # Decodifica el ID del usuario desde uidb64 y obtiene el usuario
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        user = get_object_or_404(User, id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verifica que el token sea válido y pertenezca al usuario
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Actualiza la sesión del usuario
                messages.success(request, 'Contraseña cambiada exitosamente.')
                new_password = form.cleaned_data.get('new_password2')
                accept_link = 'http://127.0.0.1:8000/signin/?next=/actividades/'
                message_html = render_to_string('StockMaster_app/correos/correo_cambio.html', {'accept_link': accept_link, 'user': request.user,'new_password':new_password})
                
                user = form.save()

                # Actualiza la sesión del usuario para evitar que se cierre la sesión después de cambiar la contraseña
                update_session_auth_hash(request, user)

                # Envia un correo electrónico al usuario notificando el cambio de contraseña
                subject = 'Cambio de Contraseña'
                from_email = 'stockmaster404@gmail.com'
                
                try:
                    send_mail(subject, '', from_email, [user.email], fail_silently=False, html_message=message_html)
                except Exception as e:
                    print(f'Error al enviar el correo de cambio de Contraseña: {e}')
                    messages.error(request, f'Error al enviar el correo de cambio de Contraseña: {e}')

                return redirect('/signin/?next=/actividades/')
            else:
                messages.error(request, 'Error al cambiar la contraseña. Por favor, corrija los errores.')
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, 'Enlace de cambio de contraseña no válido.')
        return redirect('/signin/?next=/actividades/')

    return render(request, 'StockMaster_app/cambio.html', {'form': form})
                   

def permiso(request, id):
        user = get_object_or_404(User, id=id)
        accept_link = f'http://127.0.0.1:8000/cambio/{urlsafe_base64_encode(force_bytes(user.id))}/{default_token_generator.make_token(user)}/'
        message_html = render_to_string('StockMaster_app/correos/correo_cam.html', {'accept_link': accept_link, 'user': request.user})
            # Actualiza la sesión del usuario para evitar que se cierre la sesión después de cambiar la contraseña

            # Envia un correo electrónico al usuario notificando el cambio de contraseña
        subject = 'Cambio de Contraseña'
        from_email = 'stockmaster404@gmail.com'
        messages.success(request, 'Permiso Enviado')
        try:
                send_mail(subject, '', from_email, [user.email], fail_silently=False, html_message=message_html)
        except Exception as e:
                print(f'Error al enviar el correo de cambio de Contraseña: {e}')
                messages.error(request, f'Error al enviar el correo de cambio de Contraseña: {e}')


            
        return redirect('/usuarios')
#ya cambia la contra
@login_required(login_url='signin')       
def cambio_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password2')
            accept_link = 'http://127.0.0.1:8000/signin/?next=/actividades/'
            message_html = render_to_string('StockMaster_app/correos/correo_cambio.html', {'accept_link': accept_link, 'user': request.user,'new_password':new_password})
            
            user = form.save()

            # Actualiza la sesión del usuario para evitar que se cierre la sesión después de cambiar la contraseña
            update_session_auth_hash(request, user)

            # Envia un correo electrónico al usuario notificando el cambio de contraseña
            subject = 'Cambio de Contraseña'
            from_email = 'stockmaster404@gmail.com'
            
            try:
                send_mail(subject, '', from_email, [user.email], fail_silently=False, html_message=message_html)
            except Exception as e:
                print(f'Error al enviar el correo de cambio de Contraseña: {e}')
                messages.error(request, f'Error al enviar el correo de cambio de Contraseña: {e}')


            messages.success(request, 'Cambio la Contraseña')
            return redirect('/cambio_password')  # Reemplaza con la URL deseada después de cambiar la contraseña
            # Código de cambio de contraseña exitoso aquí
        else:
            # El formulario no es válido, renderiza la página con los errores
            if request.user.has_perm('StockMaster_app.delete_mensajes'):
                usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

                # Filtra los mensajes para obtener solo los del usuario actual
                mensajes = Mensajes.objects.filter(username=usuario_actual)

                # Obtiene la cantidad de mensajes del usuario actual
                cantidad_mensajes = mensajes.count()
            else:
                mensajes = Mensajes.objects.all()
                cantidad_mensajes = mensajes.count()
            usuario = Usuario.objects.all()
            roles = RolExtra.objects.all()
            grupos = Group.objects.all()

            for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)

            return render(request, 'StockMaster_app/cambio_contraseña.html', {'form': form, 'Roles': roles, 'Usuarios': form, 'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes, 'usuario': usuario, 'grupos': grupos})
    
    else:
        # Código para manejar la solicitud GET (puede ser igual al que ya tienes)
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        usuario = Usuario.objects.all()
        roles = RolExtra.objects.all()
        grupos = Group.objects.all()

        for Usuarios in usuario:
            Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)

        form = PasswordChangeForm(request.user)
        return render(request, 'StockMaster_app/cambio_contraseña.html', {'form': form, 'Roles': roles, 'Usuarios': form, 'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes, 'usuario': usuario, 'grupos': grupos})

def descripcion(request, id_usuario):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')

        objeto = Usuario.objects.get(id_usuario=id_usuario)
        objeto.descripcion = descripcion
        objeto.save()
        messages.success(request, 'Nueva Descripción')
        return redirect('/cambio_password')


def dar_baja(request, id): 
    baja = User.objects.get(id=id)
    baja.is_active = 0
    baja.save()
    messages.success(request, 'Usuario dado de baja')
    return redirect('/usuarios')


def recuperar(request,id):
    recu = User.objects.get(id=id)
    recu.is_active = 1
    recu.save()
    messages.success(request, 'Usuario Recuperado')
    return redirect('/recuperar_usuario')

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
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        ProveedoresListados = Proveedores.objects.all()
        MarcaListados = Marca.objects.all() 
        AreaListado = Area.objects.all()
        form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
        usuario = Usuario.objects.all()
        cantidad_marcas = MarcaListados.count()
        cantidad_productos = ProductosListados.count()
        cantidad_categorias = CategoriaListados.count()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
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
            'Area':AreaListado
        })    
    else:
        return redirect('/actividades')
    
def get_imagen_url(imagen_binaria):
    imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
    return f"data:image/jpeg;base64,{imagen_base64}"
#Registrar Poducto

@login_required(login_url='signin')
def registrarProducto(request):
    if request.user.has_perm('StockMaster_app.view_productos'):
        codigo = request.POST['txtCodigo']
        nombre = request.POST['txtNombre']
        precio = request.POST['NumPrecio']
        cantPro = request.POST['CantPro'] 
        imagen = request.FILES['imagen'] 
        categoria_id = request.POST['categoria']
        idProveedor = request.POST['proveedor']
        marca_id = request.POST['marca']
        area_id = request.POST['area']

        # Comprobar si el producto ya existe marca=marca
        if Productos.objects.filter(codigo=codigo).exists():
            messages.error(request, '¡El producto con este código ya existe!')
        elif Productos.objects.filter( nombre=nombre).exists():
            messages.error(request, 'Este producto ya existe!')
        else:
            # Leer los datos de la imagen como bytes
            imagen_bytes = imagen.read()
            
            # Crear una instancia de Producto con los datos proporcionados, incluyendo la imagen como bytes
            producto = Productos(codigo=codigo, nombre=nombre, precio=precio, cantPro=cantPro, imagen=imagen_bytes, id_categorias_id=categoria_id, id_area_id=area_id,username=request.user.username,fecha_edit = timezone.now(),movimiento='Creacion de Producto', id_Proveedores_id=idProveedor, id_marca_id= marca_id)
            # Guardar la instancia en la base de datos
            historial= Historial.objects.all()
            historial = Historial(movimiento='Creacion de Producto',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
            historial.save()
            producto.save()
            messages.success(request, '¡Producto registrado con exito!')
        return redirect('/productos/')
    else:
        return redirect('/actividades')

#Editar Producto
@login_required(login_url='signin')
def editarProductoMod(request):
    if request.user.has_perm('StockMaster_app.view_productos'):
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
            area_id = request.POST.get('area')
            
            try:
                productos = Productos.objects.get(idproducts=idproducts)
            except ObjectDoesNotExist:
                messages.error(request, 'El producto no se encontró o no existe.')
                return redirect('/productos/')  # Puedes redirigir a donde desees
            if Productos.objects.filter(nombre=nombre, codigo=codigo, precio=precio, cantPro=cantPro, id_categorias_id=categoria_id, id_Proveedores_id=idProveedor, id_marca_id=marca_id, id_area_id = area_id).exists():
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
                    productos.id_area_id= area_id
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
                productos.id_marca_id = marca_id
                productos.id_area_id= area_id
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
    else:
        return redirect('/actividades')
    
@login_required(login_url='signin')
def edicioninventario2(request, idproducts):
    if request.user.has_perm('StockMaster_app.view_productos'):
        productos = Productos.objects.get(idproducts=idproducts)
        ProveedorListados = Proveedores.objects.all()
        MarcaListado = Marca.objects.all()
        AreaListado = Area.objects.all()
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
            "Marca": [{"id_marca": c.marca_id, "nombre": c.nombre} for c in MarcaListado],
            "Area": [{"area_id": c.area_id, "nombre": c.nombre} for c in AreaListado]
        }
        return JsonResponse(data)
        return render(request, 'StockMaster_app/productos.html', data)
    else:
        return redirect('/actividades')

#Recuperar Producto
@login_required(login_url='signin')
def cambio_statusre(request, idproducts):
    if request.user.has_perm('StockMaster_app.delete_productos'):
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
    else:
        return redirect('/actividades')

#Eliminar Producto
@login_required(login_url='signin')
def cambio_status(request, idproducts):
    if request.user.has_perm('StockMaster_app.view_productos'):
        producto = Productos.objects.get(idproducts=idproducts)
        messages.success(request, '¡Producto Eliminado!')
        if producto.status != 0:
            producto.status = 0
            if producto.status_mov !=1:
                producto.status_mov = 1
            producto.fecha_edit = timezone.now()
            producto.username = request.user.username
            producto.movimiento = 'Producto Dado de Baja'
            historial= Historial.objects.all()
            historial = Historial(movimiento='Producto Dado de Baja',usuario=request.user.username,fecha=timezone.now(),nombre=producto.nombre)
            historial.save()
            producto.save()
        return redirect('/productos')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminaInventario(request, idproducts):
    if request.user.has_perm('StockMaster_app.delete_productos'):
        productos = Productos.objects.get(idproducts=idproducts)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Producto',usuario=request.user.username,fecha=timezone.now(),nombre=productos.nombre)
        historial.save()
        productos.delete()
        messages.success(request, '¡Producto Eliminado!')
        return redirect('/recuperar_producto')
    else:
        return redirect('/actividades')
    
#____________________________________________________________________________________________________________________________________

#---------------------------------------------------------- P R O V E E D O R E S -------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Proveedor
@login_required(login_url='signin')
def prov(request):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProveedoresListados = Proveedores.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        for proveedor in ProveedoresListados:
            proveedor.imagen_url = get_imagen_url(proveedor.imagen)
        return render(request, 'StockMaster_app/proveedor.html', { "Proveedor": ProveedoresListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

#Registrar Proveedor
@login_required(login_url='signin')
def registrarProv(request):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
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
            prov = Proveedores(nombre=nombreProv, contacto=contactoProv, telefono=telefonoProv, email=emailProv, calle=calle, noExt=noExt, noInt=noInt, colonia=colonia, cp=cp, municipio=municipio, estado=estado, pais=pais, imagen=imagen_bytes,username=request.user.username,movimiento='Creacion de Proveedor',status_mov=status_mov)
            # Guardar la instancia en la base de datos
            historial= Historial.objects.all()
            historial = Historial(movimiento='Creacion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=prov.nombre)
            historial.save()
            prov.save()
            messages.success(request, '¡Proveedor registrado!')
        return redirect('/prov/')
    else:
        return redirect('/actividades')

#Editar Proveedor
@login_required(login_url='signin')
def editarProveedorMod(request):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
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
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def edicionProveedor2(request, idProveedor):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
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
    else:
        return redirect('/actividades')

#Recuperar Proveedor
@login_required(login_url='signin')
def cambio_statusrepro(request,idProveedor):
    if request.user.has_perm('StockMaster_app.delete_proveedores'):
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
    else:
        return redirect('/actividades')

#Eliminar Proveedor
@login_required(login_url='signin')
def cambio_statuspro(request, idProveedor):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
        proveedor = Proveedores.objects.get(idProveedor=idProveedor)
        messages.success(request, '¡Proveedor Eliminado!')
        if proveedor.status != 0:
            proveedor.status = 0
            if proveedor.status_mov !=1:
                proveedor.status_mov = 1
            proveedor.fecha_edit = timezone.now()
            proveedor.username = request.user.username
            proveedor.movimiento = 'Proveedor Dado de Baja'
            historial= Historial.objects.all()
            historial = Historial(movimiento='Proveedor Dado de Baja',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
            historial.save()
            proveedor.save()
        return redirect('/prov')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminaProveedor(request, idProveedor):
    if request.user.has_perm('StockMaster_app.delete_proveedores'):
        proveedor = Proveedores.objects.get(idProveedor=idProveedor)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Proveedor',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
        historial.save()
        Productos.objects.filter(id_Proveedores=proveedor).update(id_Proveedores=None)
        proveedor.delete()
        messages.success(request, '¡Proveedor Eliminado!')
        return redirect('/recuperar_proveedor')
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#----------------------------------------------------------------- A R E A S ------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Area
@login_required(login_url='signin')
def area(request):
    if request.user.has_perm('StockMaster_app.view_area'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        AreaListado = Area.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/area.html', { "Area": AreaListado, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

#Registrar Areas
@login_required(login_url='signin')
def registrar_area(request):
    if request.user.has_perm('StockMaster_app.view_area'):
        nombre = request.POST['nombreArea']
        # Comprobar si la categoría ya existe
        if Area.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡Esta Area ya existe!')
        else:
                # Crear una nueva instancia de Categoria con el nombre proporcionado
            area = Area(nombre=nombre,username=request.user.username,fech_cate=timezone.now(),movi='Creacion de Area')
            historial= Historial.objects.all()
            historial = Historial(movimiento='Creacion de Area',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
            historial.save() 
                # Guardar la instancia en la base de datos
            area.save()
                
            messages.success(request, '¡Area registrada con éxito!')

        # Redireccionar a la página de categorías después del registro
        return redirect('/area/')
    else:
        return redirect('/actividades')
    
#Editar Areas
@login_required(login_url='signin')
def editarAreaMod(request):
    if request.user.has_perm('StockMaster_app.view_area'):
        try:
            area_id = request.POST.get('productId')
            nombre = request.POST.get('nombre')
            try:
                area = Area.objects.get(area_id= area_id)
            except ObjectDoesNotExist:
                messages.error(request, 'El area no se encontró o no existe.')
                return redirect('/area/')  # Puedes redirigir a donde desees
            
            if Area.objects.filter(nombre=nombre).exists():
                messages.error(request, '¡Esta area no recibio cambios!')
                return redirect('/area/') 
            else:
                area.nombre = nombre

                area.username = request.user.username
                area.movi = 'Edicion de Area'
                area.fech_cate = timezone.now()
                if area.status_mov !=1:
                    area.status_mov = 1 
                historial= Historial.objects.all()
                historial = Historial(movimiento='Edicion de Area',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
                historial.save()
                area.save()

                messages.success(request, '¡Area Editada!')
                return redirect('/area/') 
        except ObjectDoesNotExist:
            messages.error(request, 'El Area no se encontró o no existe.')
            return redirect('/area/')  # Puedes redirigir a donde desees
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def edicionArea2(request, area_id):
    if request.user.has_perm('StockMaster_app.view_area'):
        area = Area.objects.get(area_id=area_id)

        data = {
            "nombre" : area.nombre,
        }

        #return JsonResponse(data)    
        #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
        return JsonResponse(data)
        return render(request, 'StockMaster_app/area.html', data)
    else:
        return redirect('/actividades')

#Recuperar Areas
@login_required(login_url='signin')
def status_areare(request,area_id):
    if request.user.has_perm('StockMaster_app.delete_area'):
        area = Area.objects.get(area_id=area_id)
        if area.status !=1:
                area.status=1
                area.fech_cate = timezone.now()
                area.movi = 'Recuperacion de Area'
                area.username = request.user.username
                if area.status_mov != 1:
                    area.status_mov = 1
                historial= Historial.objects.all()
                historial = Historial(movimiento='Recuperacion de Area',usuario=request.user.username,fecha=timezone.now(),nombre=area.nombre)
                historial.save()
                area.save()
                messages.success(request, '¡Area Recuperada!')
        return redirect('/recuperar_designaciones')
    else:
        return redirect('/actividades')

#Eliminar Areas
@login_required(login_url='signin')
def status_area(request,area_id):
    if request.user.has_perm('StockMaster_app.view_area'):
        area = Area.objects.get(area_id=area_id)
        if area.status !=0:
            area.status=0
            area.fech_cate = timezone.now()
            area.movi = 'Area Dado de Baja'
            area.username = request.user.username
            if area.status_mov != 1:
                area.status_mov = 1
            historial= Historial.objects.all()
            historial = Historial(movimiento='Area Dado de Baja',usuario=request.user.username,fecha=timezone.now(),nombre=area.nombre)
            historial.save()
            area.save()
            messages.success(request, '¡Area Eliminada!')
        return redirect('/area')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminar_area(request, area_id):
    if request.user.has_perm('StockMaster_app.delete_area'):
        area = Area.objects.get(area_id=area_id)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Area',usuario=request.user.username,fecha=timezone.now(),nombre=area.nombre)
        historial.save()
        Productos.objects.filter(id_area=area_id).update(id_area=None)
        area.delete()
        messages.success(request, '¡Area Eliminada!')
        return redirect('/recuperar_designaciones')  # O redirige a donde desees después de la eliminación
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#---------------------------------------------------------- C A T E G O R I A S ---------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Categoria
@login_required(login_url='signin')
def configuraciones(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        CategoriaListados = Categoria.objects.all().order_by('-categoria_id')
        MarcaListados = Marca.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/configuraciones.html',{"Categoria": CategoriaListados,"Marca":MarcaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

#Registrar Categoria
@login_required(login_url='signin')
def registrar_categoria(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        nombre = request.POST['txtNombreCat']
        # Comprobar si la categoría ya existe
        if Categoria.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡Esta categoría ya existe!')
        else:
                # Crear una nueva instancia de Categoria con el nombre proporcionado
            categoria = Categoria(nombre=nombre,username=request.user.username,fech_cate=timezone.now(),movi='Creacion de Categoria')
            historial= Historial.objects.all()
            historial = Historial(movimiento='Creacion de Categoria',usuario=request.user.username,fecha=timezone.now(),nombre=nombre)
            historial.save() 
                # Guardar la instancia en la base de datos
            categoria.save()
                
            messages.success(request, '¡Categoría registrada con éxito!')

        # Redireccionar a la página de categorías después del registro
        return redirect('etiquetas')
    else:
        return redirect('/actividades')

#Editar Categoria
@login_required(login_url='signin')
def editarCategoriaMod(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
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
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def edicionCategoria2(request, categoria_id):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        categoria = Categoria.objects.get(categoria_id=categoria_id)

        data = {
            "nombre" : categoria.nombre,
        }

        #return JsonResponse(data)    
        #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
        return JsonResponse(data)
        return render(request, 'StockMaster_app/configuraciones.html', data)
    else:
        return redirect('/actividades')

#Recuperar Categoria
@login_required(login_url='signin')
def status_categoriare(request,categoria_id):
    if request.user.has_perm('StockMaster_app.delete_categoria'):
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
        return redirect('/recuperar_etiquetas')
    else:
        return redirect('/actividades')

#Eliminar Categoria
@login_required(login_url='signin')
def status_categoria(request,categoria_id):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        categoria = Categoria.objects.get(categoria_id=categoria_id)
        if categoria.status !=0:
            categoria.status=0
            categoria.fech_cate = timezone.now()
            categoria.movi = 'Categoria Dado de Baja'
            categoria.username = request.user.username
            if categoria.status_mov != 1:
                categoria.status_mov = 1
            historial= Historial.objects.all()
            historial = Historial(movimiento='Categoria Dado de Baja',usuario=request.user.username,fecha=timezone.now(),nombre=categoria.nombre)
            historial.save()
            categoria.save()
            messages.success(request, '¡Categoría Eliminada!')
        return redirect('/config')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminar_categoria(request, categoria_id):
    if request.user.has_perm('StockMaster_app.delete_categoria'):
        categoria = Categoria.objects.get(categoria_id=categoria_id)
        Productos.objects.filter(id_categorias=categoria).update(id_categorias=None)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Categoria',usuario=request.user.username,fecha=timezone.now(),nombre=categoria.nombre)
        historial.save()
        Productos.objects.filter(id_categorias=categoria).update(id_categorias=None)
        categoria.delete()
        messages.success(request, '¡Categoría Eliminada!')
        return redirect('/recuperar_etiquetas')  # O redirige a donde desees después de la eliminación
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#-------------------------------------------------------------- M A R C A S -------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

#Visualizar Marca
@login_required(login_url='signin')
def MarcaView(request):
    if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
    else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
    MarcaListados = Marca.objects.all()
    CategoriaListados = Categoria.objects.all()
    form = User.objects.all()  
    usuario = Usuario.objects.all()
    for Usuarios in usuario:
            Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
    return render(request, 'StockMaster_app/configuraciones.html', {"Marca": MarcaListados,"Categoria": CategoriaListados,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes,'Usuario':form,'usuarios':usuario})

#Registrar Marca
@login_required(login_url='signin')
def registrar_marca(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        nombre = request.POST['txtMarcaNew']
            
        if Marca.objects.filter(nombre=nombre).exists():
            messages.error(request, 'La marca ya está registrada.')
        else:
            marca = Marca(nombre=nombre, username=request.user.username, fech_cate=timezone.now(), movi='Creación de Marca')
            historial = Historial(movimiento='Creacion de Marca', usuario=request.user.username, fecha=timezone.now(), nombre=nombre)
            historial.save()
            marca.save()
            messages.success(request, '¡Marca registrada con éxito!')
        return HttpResponseRedirect('/config/')  # Redirige a la URL deseada después de procesar el formulario
    else:
        return redirect('/actividades')

#Editar Marca
@login_required(login_url='signin')
def editarMarcaMod(request):
    if request.user.has_perm('StockMaster_app.view_categoria'):
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
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def edicionMarca2(request, marca_id):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        marca = Marca.objects.get(marca_id= marca_id)
        
        data = {
            "nombre" : marca.nombre,
        }

        #return JsonResponse(data)    
        #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
        return JsonResponse(data)
        return render(request, 'StockMaster_app/configuraciones.html', data)
    else:
        return redirect('/actividades')

#Recuperar Marca
@login_required(login_url='signin')
def cambio_statusremar(request,marca_id):
    if request.user.has_perm('StockMaster_app.delete_categoria'):
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
    else:
        return redirect('/actividades')

#Eliminar Marca
@login_required(login_url='signin')
def cambio_statusmar(request,marca_id):
    if request.user.has_perm('StockMaster_app.view_categoria'):
        marca = Marca.objects.get(marca_id= marca_id)
        if marca.status != 0:
            marca.status = 0
            if marca.status_mov !=1:
                marca.status_mov = 1
            marca.fech_cate = timezone.now()
            marca.username = request.user.username
            marca.movi = "Marca Dado de Baja"
            historial = Historial.objects.all()
            historial = Historial(movimiento='Marca Dado de Baja',usuario=request.user.username,fecha=timezone.now(),nombre=marca.nombre)
            historial.save()
            marca.save()
        messages.success(request, '¡Marca Eliminada¡')
        return redirect('/config')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminar_marca(request, marca_id):
    if request.user.has_perm('StockMaster_app.delete_categoria'):
        marca = Marca.objects.get(marca_id=marca_id)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Marca',usuario=request.user.username,fecha=timezone.now(),nombre=marca.nombre)
        historial.save()
        Productos.objects.filter(id_marca=marca).update(id_marca=None)
        marca.delete()
        messages.success(request, '¡Marca Eliminada!')
        return redirect('/recuperar_etiquetas')  # O redirige a donde desees después de la eliminación
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#----------------------------------------------------------------- R O L E S ------------------------------------------------------->
#____________________________________________________________________________________________________________________________________


def get_principal(request):
    return request.POST.get('principal') == 'on'
def get_inventario(request):
    return request.POST.get('inventario') == 'on'
def get_productos(request):
    return request.POST.get('productos') == 'on'
def get_proveedores(request):
    return request.POST.get('proveedores') == 'on'
def get_etiquetas(request):
    return request.POST.get('etiquetas') == 'on'
def get_area(request):
    return request.POST.get('area') == 'on'
def get_pedidos(request):
    return request.POST.get('pedidos') == 'on'
def get_prodRecu(request):
    return request.POST.get('productosRecuperacion') == 'on'
def get_provRecu(request):
    return request.POST.get('proveedoresRecuperacion') == 'on'
def get_etiqRecu(request):
    return request.POST.get('etiquetasRecuperacion') == 'on'
def get_degRecu(request):
    return request.POST.get('designadoRecuperacion') == 'on'
def get_usuRecu(request):
    return request.POST.get('usuarioRecuperacion') == 'on'
def get_usuarios(request):
    return request.POST.get('usuarios') == 'on'
def get_roles(request):
    return request.POST.get('roles') == 'on'
def get_soporte(request):
    return request.POST.get('soporte') == 'on'
def get_soporteenviar(request):
    return request.POST.get('soporteenviar') == 'on'
def get_contra(request):
    return request.POST.get('contra') == 'on'
def get_histGen(request):
    return request.POST.get('historialGeneral') == 'on'
def get_histMod(request):
    return request.POST.get('historialModificaciones') == 'on'
def get_histMov(request):
    return request.POST.get('historialMovimientos') == 'on'
def get_histEli(request):
    return request.POST.get('historialEliminados') == 'on'
#Visualizar Rol
@login_required(login_url='signin')
def RolView(request):
    if request.user.has_perm('StockMaster_app.view_rolextra'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        roles = Group.objects.all() 
        roles_con_status_1 = [rol for rol in roles if RolExtra.objects.get(grupo=rol).status == 1]
        return render(request, 'StockMaster_app/roles.html', {"Roles": roles_con_status_1,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

#Registrar Rol
@login_required(login_url='signin')
def registrar_rol(request):
    if request.user.has_perm('StockMaster_app.view_rolextra'):
        nombre = request.POST['RolNew']
        principal = get_principal(request)
        pedidos = get_pedidos(request)
        inventario = get_inventario(request)
        productos = get_productos(request)
        proveedores = get_proveedores(request)
        etiquetas = get_etiquetas(request)
        area = get_area(request)
        productosRecuperacion = get_prodRecu(request)
        proveedoresRecuperacion = get_provRecu(request)
        etiquetasRecuperacion = get_etiqRecu(request)
        designadoRecuperacion = get_degRecu(request)
        usuarios = get_usuarios(request)
        roles = get_roles(request)
        contra = get_contra(request)
        historialGeneral = get_histGen(request)
        historialModificaciones = get_histMod(request)
        historialMovimientos = get_histMov(request)
        historialEliminados = get_histEli(request)
        soporte = get_soporte(request)
        soporteenviar = get_soporteenviar(request)
        usuarioRecuperacion = get_usuRecu(request)

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
            rol_extra.etiquetas = etiquetas
            rol_extra.area = area
            rol_extra.pedidos = pedidos
            rol_extra.productosRecuperacion = productosRecuperacion 
            rol_extra.proveedoresRecuperacion = proveedoresRecuperacion 
            rol_extra.etiquetasRecuperacion = etiquetasRecuperacion
            rol_extra.designadoRecuperacion = designadoRecuperacion
            rol_extra.usuarios = usuarios
            rol_extra.usuariosRecuperacion = usuarioRecuperacion
            rol_extra.roles = roles
            rol_extra.soporte = soporte 
            rol_extra.soporteenviar = soporteenviar 
            rol_extra.contra = contra 
            rol_extra.movi = 'Creacion de Rol'
            rol_extra.historialGeneral = historialGeneral 
            rol_extra.historialModificaciones = historialModificaciones 
            rol_extra.historialMovimientos = historialMovimientos 
            rol_extra.historialEliminados = historialEliminados 

            if principal:
                rol.permissions.add(Permission.objects.get(codename='view_marca'))
            if inventario:
                rol.permissions.add(Permission.objects.get(codename='delete_marca'))
            if productos:
                rol.permissions.add(Permission.objects.get(codename='view_productos'))
            if proveedores:
                rol.permissions.add(Permission.objects.get(codename='view_proveedores'))
            if etiquetas:
                rol.permissions.add(Permission.objects.get(codename='view_categoria'))
            if area:
                rol.permissions.add(Permission.objects.get(codename='view_area'))
            if pedidos:
                rol.permissions.add(Permission.objects.get(codename='add_productos'))
            if productosRecuperacion:
                rol.permissions.add(Permission.objects.get(codename='delete_productos'))
            if proveedoresRecuperacion:
                rol.permissions.add(Permission.objects.get(codename='delete_proveedores'))
            if etiquetasRecuperacion:
                rol.permissions.add(Permission.objects.get(codename='delete_categoria'))
            if designadoRecuperacion:
                rol.permissions.add(Permission.objects.get(codename='delete_area'))
            if usuarioRecuperacion:
                rol.permissions.add(Permission.objects.get(codename='delete_usuario'))
            if usuarios:
                rol.permissions.add(Permission.objects.get(codename='view_usuario'))
            if roles:
                rol.permissions.add(Permission.objects.get(codename='view_rolextra'))
            if soporte:
                rol.permissions.add(Permission.objects.get(codename='view_mensajes'))
            if soporteenviar:
                rol.permissions.add(Permission.objects.get(codename='delete_mensajes'))
            if contra:
                rol.permissions.add(Permission.objects.get(codename='delete_rolextra'))
            if historialGeneral:
                rol.permissions.add(Permission.objects.get(codename='view_historial'))
            if historialModificaciones:
                rol.permissions.add(Permission.objects.get(codename='add_historial'))
            if historialMovimientos:
                rol.permissions.add(Permission.objects.get(codename='change_historial'))
            if historialEliminados:
                rol.permissions.add(Permission.objects.get(codename='delete_historial'))
            
            rol_extra.save()
            historial = Historial(movimiento='Creacion de Rol', usuario=request.user.username, fecha=timezone.now(), nombre=rol.name)
            historial.save()
            
            messages.success(request, '¡Rol registrado con éxito!')
        return HttpResponseRedirect('/rol/')  # Redirige a la URL deseada después de procesar el formulario
    else:
        return redirect('/actividades')

#Editar Rol
@login_required(login_url='signin')
def editarRolMod(request):
    if request.user.has_perm('StockMaster_app.view_rolextra'):
        try:
            id = request.POST.get('productId')
            nombre = request.POST.get('nombre')
            principal = get_principal(request)
            inventario = get_inventario(request)
            productos = get_productos(request)
            proveedores = get_proveedores(request)
            etiquetas = get_etiquetas(request)
            area = get_area(request)
            productosRecuperacion = get_prodRecu(request)
            proveedoresRecuperacion = get_provRecu(request)
            etiquetasRecuperacion = get_etiqRecu(request)
            designadoRecuperacion = get_degRecu(request)
            usuarios = get_usuarios(request)
            roles = get_roles(request)
            contra = get_contra(request)
            historialGeneral = get_histGen(request)
            historialModificaciones = get_histMod(request)
            historialMovimientos = get_histMov(request)
            historialEliminados = get_histEli(request)
            soporte = get_soporte(request)
            soporteenviar = get_soporteenviar(request)
            usuarioRecuperacion = get_usuRecu(request)
            pedidos = get_pedidos(request)

            try:
                rol = Group.objects.get(id= id)
                rol_extra = RolExtra.objects.get(grupo=rol)
            except RolExtra.DoesNotExist:
                messages.error(request, 'El Rol no se encontró o no existe.')
                return redirect('/rol/')  # Puedes redirigir a donde desees
            if Group.objects.filter(name=nombre).exists() and RolExtra.objects.filter(principal=principal, inventario=inventario,
                productos=productos, proveedores=proveedores, etiquetas=etiquetas, area=area, productosRecuperacion=productosRecuperacion,
                proveedoresRecuperacion=proveedoresRecuperacion, etiquetasRecuperacion=etiquetasRecuperacion, designadoRecuperacion=designadoRecuperacion,
                usuariosRecuperacion=usuarioRecuperacion, usuarios=usuarios, roles=roles, soporte=soporte, soporteenviar=soporteenviar,
                contra=contra, historialGeneral=historialGeneral, historialModificaciones=historialModificaciones, historialMovimientos=historialMovimientos,
                historialEliminados=historialEliminados, pedidos=pedidos).exists():

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
                rol_extra.area = area
                rol_extra.productosRecuperacion = productosRecuperacion
                rol_extra.proveedoresRecuperacion = proveedoresRecuperacion
                rol_extra.etiquetasRecuperacion = etiquetasRecuperacion
                rol_extra.designadoRecuperacion = designadoRecuperacion
                rol_extra.usuariosRecuperacion = usuarioRecuperacion
                rol_extra.usuarios = usuarios
                rol_extra.pedidos = pedidos
                rol_extra.roles = roles
                rol_extra.soporte = soporte
                rol_extra.soporteenviar = soporteenviar 
                rol_extra.contra = contra 
                rol_extra.movi = 'Edicion de Rol'
                rol_extra.historialGeneral = historialGeneral 
                rol_extra.historialModificaciones = historialModificaciones 
                rol_extra.historialMovimientos = historialMovimientos 
                rol_extra.historialEliminados = historialEliminados 

                if principal:
                    rol.permissions.add(Permission.objects.get(codename='view_marca'))
                else:
                    permiso = Permission.objects.get(codename='view_marca')
                    rol.permissions.remove(permiso)
                if inventario:
                    rol.permissions.add(Permission.objects.get(codename='delete_marca'))
                else:
                    permiso = Permission.objects.get(codename='delete_marca')
                    rol.permissions.remove(permiso)
                if productos:
                    rol.permissions.add(Permission.objects.get(codename='view_productos'))
                else:
                    permiso = Permission.objects.get(codename='view_productos')
                    rol.permissions.remove(permiso)
                if proveedores:
                    rol.permissions.add(Permission.objects.get(codename='view_proveedores'))
                else:
                    permiso = Permission.objects.get(codename='view_proveedores')
                    rol.permissions.remove(permiso)
                if etiquetas:
                    rol.permissions.add(Permission.objects.get(codename='view_categoria'))
                else:
                    permiso = Permission.objects.get(codename='view_categoria')
                    rol.permissions.remove(permiso)
                if area:
                    rol.permissions.add(Permission.objects.get(codename='view_area'))
                else:
                    permiso = Permission.objects.get(codename='view_area')
                    rol.permissions.remove(permiso)
                if pedidos:
                    rol.permissions.add(Permission.objects.get(codename='add_productos'))
                else:
                    permiso = Permission.objects.get(codename='add_productos')
                    rol.permissions.remove(permiso)
                if productosRecuperacion:
                    rol.permissions.add(Permission.objects.get(codename='delete_productos'))
                else:
                    permiso = Permission.objects.get(codename='delete_productos')
                    rol.permissions.remove(permiso)
                if proveedoresRecuperacion:
                    rol.permissions.add(Permission.objects.get(codename='delete_proveedores'))
                else:
                    permiso = Permission.objects.get(codename='delete_proveedores')
                    rol.permissions.remove(permiso)
                if etiquetasRecuperacion:
                    rol.permissions.add(Permission.objects.get(codename='delete_categoria'))
                else:
                    permiso = Permission.objects.get(codename='delete_categoria')
                    rol.permissions.remove(permiso)
                if designadoRecuperacion:
                    rol.permissions.add(Permission.objects.get(codename='delete_area'))
                else:
                    permiso = Permission.objects.get(codename='delete_area')
                    rol.permissions.remove(permiso)
                if usuarioRecuperacion:
                    rol.permissions.add(Permission.objects.get(codename='delete_usuario'))
                else:
                    permiso = Permission.objects.get(codename='delete_usuario')
                    rol.permissions.remove(permiso)
                if usuarios:
                    rol.permissions.add(Permission.objects.get(codename='view_usuario'))
                else:
                    permiso = Permission.objects.get(codename='view_usuario')
                    rol.permissions.remove(permiso)
                if roles:
                    rol.permissions.add(Permission.objects.get(codename='view_rolextra'))
                else:
                    permiso = Permission.objects.get(codename='view_rolextra')
                    rol.permissions.remove(permiso)
                if soporte:
                    rol.permissions.add(Permission.objects.get(codename='view_mensajes'))
                else:
                    permiso = Permission.objects.get(codename='view_mensajes')
                    rol.permissions.remove(permiso)
                if soporteenviar:
                    rol.permissions.add(Permission.objects.get(codename='delete_mensajes'))
                else:
                    permiso = Permission.objects.get(codename='delete_mensajes')
                    rol.permissions.remove(permiso)
                if contra:
                    rol.permissions.add(Permission.objects.get(codename='delete_rolextra'))
                else:
                    permiso = Permission.objects.get(codename='delete_rolextra')
                    rol.permissions.remove(permiso)
                if historialGeneral:
                    rol.permissions.add(Permission.objects.get(codename='view_historial'))
                else:
                    permiso = Permission.objects.get(codename='view_historial')
                    rol.permissions.remove(permiso)
                if historialModificaciones:
                    rol.permissions.add(Permission.objects.get(codename='add_historial'))
                else:
                    permiso = Permission.objects.get(codename='add_historial')
                    rol.permissions.remove(permiso)
                if historialMovimientos:
                    rol.permissions.add(Permission.objects.get(codename='change_historial'))
                else:
                    permiso = Permission.objects.get(codename='change_historial')
                    rol.permissions.remove(permiso)
                if historialEliminados:
                    rol.permissions.add(Permission.objects.get(codename='delete_historial'))
                else:
                    permiso = Permission.objects.get(codename='delete_historial')
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

                messages.success(request, '¡Rol  Editado!')
                return redirect('/rol/') 
        except ObjectDoesNotExist:
            messages.error(request, 'El rol no se encontró o no existe.')
            return redirect('/rol/')  # Puedes redirigir a donde desees
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def edicionRol2(request, id):
    if request.user.has_perm('StockMaster_app.view_rolextra'):
        rol = Group.objects.get(id= id)
        rol_extra = RolExtra.objects.get(grupo=rol)
        data = {
            "nombre" : rol.name,
            "principal": rol_extra.principal,
            "inventario": rol_extra.inventario,
            "productos":rol_extra.productos,
            "proveedores":rol_extra.proveedores,
            "etiquetas":rol_extra.etiquetas,
            "area":rol_extra.area,
            "productosRecuperacion":rol_extra.productosRecuperacion,
            "proveedoresRecuperacion":rol_extra.proveedoresRecuperacion,
            "etiquetasRecuperacion":rol_extra.etiquetasRecuperacion,
            "designadoRecuperacion":rol_extra.designadoRecuperacion,
            "usuarioRecuperacion":rol_extra.usuariosRecuperacion,
            "usuarios":rol_extra.usuarios,
            "roles": rol_extra.roles,
            "pedidos": rol_extra.pedidos,
            "soporte":rol_extra.soporte,
            "soporteenviar":rol_extra.soporteenviar,
            "contra":rol_extra.contra,
            "historialGeneral":rol_extra.historialGeneral,
            "historialModificaciones":rol_extra.historialModificaciones,
            "historialMovimientos":rol_extra.historialMovimientos,
            "historialEliminados":rol_extra.historialEliminados,
        }

        #return JsonResponse(data)    
        #return render(request, 'Stockmaster_app/productos.html', { idproducts : idproducts})
        return JsonResponse(data)
        return render(request, 'StockMaster_app/roles.html', data)
    else:
        return redirect('/actividades')

#Recuperar Rol
@login_required(login_url='signin')
def cambio_statusrolre(request,id):
    if request.user.has_perm('StockMaster_app.delete_area'):
        rol = Group.objects.get(id= id)
        rol_extra = RolExtra.objects.get(grupo=rol)
        if rol_extra.status != 1:
            rol_extra.status = 1
            if rol_extra.status_mov !=1:
                rol_extra.status_mov = 1
            rol_extra.fech_cate = timezone.now()
            rol_extra.username = request.user.username
            rol_extra.movi = 'Recuperacion de Rol'
            historial= Historial.objects.all()
            historial = Historial(movimiento='Recuperacion de Rol',usuario=request.user.username,fecha=timezone.now(), nombre=rol.name)
            historial.save()
            rol_extra.save()
        messages.success(request, '¡Rol Recuperado¡')
        return redirect('/recuperar_designaciones')
    else:
        return redirect('/actividades')

#Eliminar Rol
@login_required(login_url='signin')
def cambio_statusrol(request,id):
    if request.user.has_perm('StockMaster_app.view_rolextra'):
        rol = Group.objects.get(id= id)
        rol_extra = RolExtra.objects.get(grupo=rol)
        if rol_extra.status != 0:
            rol_extra.status = 0
            if rol_extra.status_mov !=1:
                rol_extra.status_mov = 1
            rol_extra.fech_cate = timezone.now()
            rol_extra.username = request.user.username
            rol_extra.movi = "Rol Dado de Baja"
            historial = Historial.objects.all()
            historial = Historial(movimiento='Rol Dado de Baja',usuario=request.user.username,fecha=timezone.now(), nombre=rol.name)
            historial.save()
            rol.save()
            rol_extra.save()
        messages.success(request, '¡Rol Eliminado¡')
        return redirect('/rol/')
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def eliminar_rol(request, id):
    if request.user.has_perm('StockMaster_app.delete_area'):
        rol = Group.objects.get(id= id)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Eliminacion de Rol',usuario=request.user.username,fecha=timezone.now(),nombre=rol.name)
        historial.save()
        rol.delete()
        messages.success(request, '¡Rol Eliminado¡')
        return redirect('/recuperar_designaciones')  # O redirige a donde desees después de la eliminación
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#----------------------------------------------------- C O M E N T A R I O S ------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def soporte(request):
    if request.user.has_perm('StockMaster_app.view_mensajes'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/soporte.html', {'Mensajes': mensajes,  'cantidad_mensajes': cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def soporteEnviar(request):
    if request.user.has_perm('StockMaster_app.delete_mensajes'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/soporteEnviar.html', {'Mensajes': mensajes,  'cantidad_mensajes': cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

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

    return redirect('/soporteEnviar')


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
    if request.user.has_perm('StockMaster_app.view_historial'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        RolListados = RolExtra.objects.all()
        historial = Historial.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/historial.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"Mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial,'Usuario':form,'usuarios':usuarios})
    else:
        return redirect('/actividades')
    
@login_required(login_url='signin')
def historialModificaciones(request):
    if request.user.has_perm('StockMaster_app.add_historial'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        RolListados = RolExtra.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        historial = Historial.objects.filter(movimiento__in=[
        "Edicion de Producto", "Edicion de Proveedor", "Edicion de Area", "Edicion de Categoria", "Edicion de Marca", "Edicion de Rol"
        "Creacion de Producto", "Creacion de Proveedor", "Creacion de Area", "Creacion de Categoria", "Creacion de Marca", "Creacion de Rol", "Creacion de Usuario"
        ])

        return render(request, 'StockMaster_app/historialModificaciones.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"Mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def historialMovimientos(request):
    if request.user.has_perm('StockMaster_app.change_historial'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        RolListados = RolExtra.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        historial = Historial.objects.filter(movimiento__in=[
        "Recuperacion de Producto", "Recuperacion de Proveedor", "Recuperacion de Area", "Recuperacion de Categoria", "Recuperacion de Marca","Recuperacion de Rol"
        ])

        return render(request, 'StockMaster_app/historialMovimientos.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"Mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def historialEliminados(request):
    if request.user.has_perm('StockMaster_app.delete_historial'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        RolListados = RolExtra.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        historial = Historial.objects.filter(movimiento__in=[
        "Eliminacion de Producto", "Eliminacion de Proveedor", "Eliminacion de Producto", "Eliminacion de Area", "Eliminacion de Marca", "Eliminacion de Categoria", "Eliminacion de Rol",
        "¡Producto Dado de Baja!", "¡Proveedor Dado de Baja!", "¡Rol Dado de Baja!", "¡Area Dado de Baja!", "¡Categoria Dado de Baja!", "¡Marca Dado de Baja!"
        ])
        
        return render(request, 'StockMaster_app/historialEliminados.html', { "Productos": ProductosListados, "Roles": RolListados,"Categoria": CategoriaListados,"Mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

#____________________________________________________________________________________________________________________________________

#------------------------------------------------------- R E C U P E R A C I O N --------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def recuperar_producto(request):
    if request.user.has_perm('StockMaster_app.delete_productos'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        ProveedoresListados = Proveedores.objects.all()
        MarcaListados = Marca.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen) 
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)
        return render(request, 'StockMaster_app/recuperar_producto.html', { "Productos": ProductosListados, "Categoria": CategoriaListados,'marca': MarcaListados, 'Proveedor' : ProveedoresListados,'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def recuperar_proveedor(request):
    if request.user.has_perm('StockMaster_app.delete_proveedores'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        proveedores = Proveedores.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/recuperar_proveedor.html', { "mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"proveedores":proveedores,'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def recuperar_etiquetas(request):
    if request.user.has_perm('StockMaster_app.delete_categoria'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        CategoriaListados = Categoria.objects.all() 
        RolListados = RolExtra.objects.all()
        MarcaListados = Marca.objects.all() 
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/recuperar_etiquetas.html', { "Categoria": CategoriaListados, "Marca":MarcaListados, "Roles": RolListados, "mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,'Usuario':form, 'usuarios':usuario})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def recuperar_designaciones(request):
    if request.user.has_perm('StockMaster_app.delete_area'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        AreasListado = Area.objects.all()
        roles = Group.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        rolextra = RolExtra.objects.all()
        roles_con_status_1 = [rol for rol in roles if RolExtra.objects.get(grupo=rol).status == 0]
        return render(request, 'StockMaster_app/recuperar_designaciones.html', { "Area":AreasListado, "RolExtra":rolextra, "Roles": roles_con_status_1, "mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,'Usuario':form, 'usuarios':usuario})
    else:
        return redirect('/actividades')

def recuperar_usuario(request):
    if request.user.has_perm('StockMaster_app.delete_usuario'):

        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        AreasListado = Area.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        for Usuarios in usuario:
            Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/recuperar_usuario.html', { "Area":AreasListado, "Mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes, 'Usuario':form,'usuarios':usuario})
    else:
        return redirect('/actividades')
#____________________________________________________________________________________________________________________________________

#------------------------------------------------------- F U N C I O N E S --------------------------------------------------------->
#____________________________________________________________________________________________________________________________________

@login_required(login_url='signin')
def productos(request):
    if request.user.has_perm('StockMaster_app.view_marca'):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        ProveedoresListados = Proveedores.objects.all()
        RolListados = RolExtra.objects.all()
        MarcaListados = Marca.objects.all()
        
        cantidad_marcas = MarcaListados.count()
        cantidad_productos = ProductosListados.count()
        cantidad_proveedores =  ProveedoresListados.count()
        cantidad_categorias = CategoriaListados.count()
        productos_por_mes = Productos.objects.annotate(month=TruncMonth('hora_baja', tzinfo=pytz.UTC)).values('month').annotate(cantidad=Sum('cantPro')).order_by('month')
        productos_por_categoria = []
        for categoria in CategoriaListados:
            cantidad_productos_categoria = Productos.objects.filter(id_categorias=categoria).count()
            productos_por_categoria.append(cantidad_productos_categoria)
        cantidad_productos_cate = [] 
        productos_por_categori = Productos.objects.values('id_categorias').annotate(cantidad=Sum('cantPro')).order_by('id_categorias')
        cantidad_productos_cate.extend(productos_por_categori)
        # Crear listas para las etiquetas y datos de la gráfica
        labels = [mes['month'].strftime('%b') for mes in productos_por_mes]
        data = [mes['cantidad'] if mes['cantidad'] is not None else 0 for mes in productos_por_mes]
        labels = [mes['month'].strftime('%b') for mes in productos_por_mes]
        data = [mes['cantidad'] for mes in productos_por_mes]
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
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
            'ProveedoresListados' : ProveedoresListados,
            'productos_por_categoria': productos_por_categoria,
            'cantidad_productos_cate':cantidad_productos_cate
            })
    else:
        return redirect('/actividades')

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
    if request.user.has_perm('StockMaster_app.delete_marca'):
        productos = []  # Inicializar una lista vacía para productos
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()

        categoria_seleccionada = request.GET.get('categoria') # Obtener la categoría seleccionada por el usuario
        if categoria_seleccionada:
            productos = Productos.objects.filter(id_categorias__nombre=categoria_seleccionada)
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all()
        MarcaListados = Marca.objects.all()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)

        return render(request, 'StockMaster_app/inventario.html', {"Productos": ProductosListados, "Categoria": CategoriaListados,"Marca":MarcaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes, 'usuarios':usuario, 'Usuario':form})
    else:
        return redirect('/actividades')

@login_required(login_url='signin')
def acercaDe(request):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/acercaDe.html', {'Usuario':form, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes, 'usuarios':usuario, 'Usuario':form})

@login_required(login_url='signin')
def terminosYcondiones(request):
        if request.user.has_perm('StockMaster_app.delete_mensajes'):
            usuario_actual = request.user  # Asegúrate de ajustar esto según tu implementación

            # Filtra los mensajes para obtener solo los del usuario actual
            mensajes = Mensajes.objects.filter(username=usuario_actual)

            # Obtiene la cantidad de mensajes del usuario actual
            cantidad_mensajes = mensajes.count()
        else:
            mensajes = Mensajes.objects.all()
            cantidad_mensajes = mensajes.count()
        form = User.objects.all()  
        usuario = Usuario.objects.all()
        for Usuarios in usuario:
                Usuarios.imagen_url = get_imagen_url(Usuarios.imagen)
        return render(request, 'StockMaster_app/TerminosDe.html', {'Usuario':form, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes, 'usuarios':usuario, 'Usuario':form})

def enviar_correo(request):
    send_mail(
        'Asunto del Correo',
        'Cuerpo del Correo',
        'stockmaster404@gmail.com',         # Reemplaza con tu dirección de correo
        ['mayelomonti1@gmail.com'],  # Reemplaza con la dirección del destinatario
        fail_silently=False,
    )
    return HttpResponse('Correo enviado correctamente.')

########################################### Views de Pedidos ###################################################################################################################################################################################################
@login_required(login_url='signin')
def ordenes(request):
    if request.user.is_superuser:
        OrdenesListados = Ordenes.objects.all()
        ProductosListados = Productos.objects.all()
        mensajes = Mensajes.objects.all()
        cantidad_mensajes = mensajes.count()
        ProveedoresListados = Proveedores.objects.all()
        Ordenes
        return render(request, 'StockMaster_app/ordenes.html', {'Ordenes': OrdenesListados, 'Proveedor': ProveedoresListados, 'Producto': ProductosListados,'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/ordenes')

@login_required(login_url='signin')
def nuevaOrden(request):
    if request.user.has_perm('StockMaster_app.view_proveedores'):
        proveedorId = request.POST['proveedor']
        productoId = request.POST['producto']
        producto = get_object_or_404(Productos, idproducts=productoId)
        proveedor = get_object_or_404(Proveedores, idProveedor=proveedorId)
        nombreProducto = producto.nombre
        fecha_formateada = timezone.now().strftime('%Y%m%d%H%M%S')
        no_Orden = fecha_formateada
        fechaPedido = timezone.now()
        codigoProd = producto.codigo
        precioUnitario = producto.precio
        cantPedido = int(request.POST['cantPedido'])
        operacionPedido = precioUnitario * cantPedido
        totalPedido = float(operacionPedido)
        nombreProv = proveedor.nombre 
        dirProveedor = f"{proveedor.calle} {proveedor.noExt} {proveedor.noInt}, {proveedor.colonia}, {proveedor.cp}, {proveedor.municipio}, {proveedor.estado}, {proveedor.pais}"
        telefonoProv = proveedor.telefono
        emailProv = proveedor.email
        calle = request.POST['calle']
        noExt = request.POST['noExt']
        noInt = request.POST['noInt']
        colonia = request.POST['colonia']
        cp = request.POST['cp']
        municipio = request.POST['municipio']
        estado = request.POST['estado']
        dirEntrega = f"{calle} {noExt} {noInt}, {colonia}, {cp}, {municipio}, {estado}"
        metodoPago = "N/A"
        status = "Pedido Enviado"
        
        # Crear una instancia de Producto con los datos proporcionados, incluyendo la imagen como bytes
        orden = Ordenes(no_Orden=no_Orden, fechaPedido=fechaPedido, nombreProd=nombreProducto, codigoProd=codigoProd, cantSolicitada=cantPedido, precioUnitario=precioUnitario, totalPedido=totalPedido, nombreProv=nombreProv, dirProveedor=dirProveedor, telefonoProv=telefonoProv, emailProv=emailProv, dirEntrega=dirEntrega, metodoPago=metodoPago, status=status)
        # Guardar la instancia en la base de datos
        historial= Historial.objects.all()
        historial = Historial(movimiento='Creacion de Pedido',usuario=request.user.username,fecha=timezone.now(),nombre=no_Orden)
        historial.save()
        orden.save()
        messages.success(request, '¡Pedido Enviado!')

        subject = f"Pedido de Inventario {nombreProducto}"
        from_email = 'stockmaster404@gmail.com'
        recipient_list = [emailProv]

        # Crear el mensaje en formato HTML
        pedido_html = render_to_string('StockMaster_app/CorreoPedidos.html', {'proveedor': proveedor, 'producto': producto, 'cantPedido': cantPedido, 'username': request.user.username, 'fechaEntrega': timezone.now(), 'dirEntrega': dirEntrega})
        try:
            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=pedido_html)
        except Exception as e:
            print(f'Error al enviar el correo: {e}')
            messages.error(request, f'Error al enviar el correo: {e}')
        return redirect('/ordenes')
    # Envío de correo de bienvenida
    else:
        return redirect('/ordenes')

def eliminarOrden(request, id_Orden):
    if request.user.has_perm('StockMaster_app.view_productos'):
        orden = Ordenes.objects.get(id_Orden=id_Orden)
        historial= Historial.objects.all()
        historial = Historial(movimiento='Orden Cancelada',usuario=request.user.username,fecha=timezone.now(),nombre=orden.no_Orden)
        historial.save()
        orden.delete()
        messages.success(request, '¡Orden Cancelada!')
        historial= Historial.objects.all()
        historial = Historial(movimiento='Orden Cancelada',usuario=request.user.username,fecha=timezone.now(),nombre=orden.no_Orden)
        return redirect('/ordenes')
    else:
        return redirect('/actividades')