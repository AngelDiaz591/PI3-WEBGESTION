from django.contrib.auth.decorators import login_required, user_passes_test
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
from .models import Productos, Mensajes, Categoria
from django.http.response import JsonResponse
import base64
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField()
    
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='signin')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            user.email = email
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            is_superuser = form.cleaned_data.get('is_superuser')
            if is_superuser is not None and is_superuser.isdigit():
                user.is_superuser = bool(int(is_superuser))
            if 'user_img' in request.FILES:
                user.user_img = request.FILES['user_img']
                        # Guarda la imagen de usuario

            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            return redirect('/usuarios')
        else:
            # Maneja los errores específicos y agrega mensajes de error según corresponda
            if 'email' in form.errors:
                messages.error(request, 'error en la escritura de gmail recomendacion "@gmail.com" "@hotmail.com" "outlook.com"')
            
            if 'username' in form.errors:
                messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            else:
                messages.error(request, 'La contraseña debe de tener más de 8 caracteres y no deben ser numeros continuos')
            # Agrega otros mensajes de error personalizados según tus necesidades
            if 'is_superuser' in form.errors:
                messages.error(request, 'error de admin')
    else:
        form = CustomUserCreationForm()

    return render(request, 'StockMaster_app/registro.html', {'form': form})

def eliminaruser(request, id):
    try:
        user_to_delete = User.objects.get(id=id)
        user_to_delete.delete()
        return redirect('/usuarios')
    except User.DoesNotExist:
        # Maneja el caso en que el usuario con el ID especificado no existe
        # Puedes mostrar un mensaje de error o realizar alguna otra acción aquí
        pass
    
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
def productos(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    return render(request, 'StockMaster_app/actividades.html', {'Mensajes': mensajes, 'cantidad_mensajes':cantidad_mensajes, 'Productos':ProductosListados,'CategoriaListados':CategoriaListados})

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

@login_required(login_url='signin')
def usuarios(request):
    if request.user.is_superuser:
        mensajes = Mensajes.objects.all()
        cantidad_mensajes =mensajes.count()
        form = User.objects.all()  # Agrega los paréntesis para instanciar el formulario
        return render(request, 'StockMaster_app/usuarios.html', {'Usuarios': form, 'Mensajes':mensajes,'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/actividades')
    
@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('/actividades')

@login_required(login_url='signin')
def pro(request):
    if request.user.is_superuser:
        mensajes = Mensajes.objects.all()
        cantidad_mensajes =mensajes.count()
        ProductosListados = Productos.objects.all()
        CategoriaListados = Categoria.objects.all() 
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)
        return render(request, 'StockMaster_app/productos.html', { "Productos": ProductosListados,"Categoria": CategoriaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/actividades')
    
def get_imagen_url(imagen_binaria):
    imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
    return f"data:image/jpeg;base64,{imagen_base64}"

@login_required(login_url='signin')
def registrarProducto(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    precio = request.POST['NumPrecio']
    marca = request.POST['NomMarca']
    cantPro = request.POST['CantPro'] 
    imagen = request.FILES['imagen'] 
    categoria_id = request.POST['categoria']
    fecha_edit = timezone.now()

    # Comprobar si el producto ya existe
    if Productos.objects.filter(codigo=codigo).exists():
        messages.error(request, '¡El producto con este código ya existe!')
    elif Productos.objects.filter(marca=marca, nombre=nombre).exists():
        messages.error(request, 'Este producto ya existe!')
    else:
        # Leer los datos de la imagen como bytes
        imagen_bytes = imagen.read()
        
        # Crear una instancia de Producto con los datos proporcionados, incluyendo la imagen como bytes
        producto = Productos(codigo=codigo, nombre=nombre, precio=precio, marca=marca, cantPro=cantPro, imagen=imagen_bytes, id_categorias_id=categoria_id,username=request.user.username,fecha_edit = timezone.now(),movimiento='Producto creado')
        # Guardar la instancia en la base de datos
        producto.save()
        messages.success(request, '¡Producto registrado!')
    return redirect('/productos/')

@login_required(login_url='signin')
def edicioninventario(request, idproducts):
    productos = Productos.objects.get(idproducts= idproducts)
    CategoriaListados = Categoria.objects.all() 
    imagen_url = get_imagen_url(productos.imagen)
    return render(request, "StockMaster_app/edicioninventario.html", {"productos": productos, "imagen_url": imagen_url, "Categoria": CategoriaListados})

@login_required(login_url='signin')
def editarProducto(request):
    idproducts = request.POST.get('idproducts')
    codigo = request.POST.get('txtCodigo')
    nombre = request.POST.get('txtNombre')
    precio = request.POST.get('NumPrecio')
    marca = request.POST.get('NomMarca')
    cantPro = request.POST.get('CantPro')
    nueva_imagen = request.FILES.get('imagen') 
    categoria_id = request.POST.get('categoria') 

    productos = Productos.objects.get(idproducts=idproducts)

    productos.codigo = codigo
    productos.nombre = nombre
    productos.precio = precio
    productos.marca = marca
    productos.cantPro = cantPro
    productos.username = request.user.username
    productos.movimiento = 'Edicion de Producto'
    productos.fecha_edit = timezone.now()
    productos.id_categorias_id = categoria_id
    if nueva_imagen:
        productos.imagen = nueva_imagen.read()
    productos.save()

    messages.success(request, '¡Producto Editado!')
    return redirect('/productos/')

@login_required(login_url='signin')
def eliminaInventario(request, idproducts):
    productos = Productos.objects.get(idproducts=idproducts)
    productos.delete()
    messages.success(request, '¡Producto Eliminado!')
    return redirect('/recuperar_producto')

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

def cambio_status(request, idproducts):
    producto = Productos.objects.get(idproducts=idproducts)
    messages.success(request, '¡Producto Eliminado!')
    if producto.status != 0:
        producto.status = 0

        producto.fecha_edit = timezone.now()
        producto.username = request.user.username
        producto.movimiento = 'Eliminacion de Producto'
        producto.save()
    return redirect('/productos')
def cambio_statusre(request, idproducts):
    producto = Productos.objects.get(idproducts=idproducts)
    if producto.status != 1:
        producto.status = 1

        producto.fecha_edit = timezone.now()
        producto.username = request.user.username
        producto.movimiento = 'Recuperacion de Producto'
        producto.save()
    messages.success(request, '¡Producto recuperado¡')
    return redirect('/recuperar_producto')
#mio gael
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
        mensaje.save()
        return redirect('/soporte/')  # Redirigir a la página de soporte o a donde corresponda

    return render(request, 'StockMaster_app/soporte.html', {'mensaje': mensaje})

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
    for producto in ProductosListados:
        producto.imagen_url = get_imagen_url(producto.imagen)

    return render(request, 'StockMaster_app/inventario.html', {"Productos": ProductosListados, "Categoria": CategoriaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})

@login_required(login_url='signin')
def configuraciones(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    CategoriaListados = Categoria.objects.all()
    return render(request, 'StockMaster_app/configuraciones.html',{"Categoria": CategoriaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})

@login_required(login_url='signin')
def recuperar_producto(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    return render(request, 'StockMaster_app/recuperar_producto.html', { "Productos": ProductosListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes})

@login_required(login_url='signin')
def registrar_categoria(request):
        
    nombre = request.POST['txtNombreCat']

        # Comprobar si la categoría ya existe
    if Categoria.objects.filter(nombre=nombre).exists():
        messages.error(request, '¡Esta categoría ya existe!')
    else:
            # Crear una nueva instancia de Categoria con el nombre proporcionado
        categoria = Categoria(nombre=nombre)
            
            # Guardar la instancia en la base de datos
        categoria.save()
            
        messages.success(request, '¡Categoría registrada con éxito!')

    # Redireccionar a la página de categorías después del registro
    return redirect('configuraciones77')

@login_required(login_url='signin')
def edicion_categoria(request, categoria_id):
    categoria = Categoria.objects.get(categoria_id= categoria_id)
    return render(request, "StockMaster_app/edicion_categoria.html", {"categoria": categoria})

@login_required(login_url='signin')
def editarCat(request):
    categoria_id = request.POST.get('idCat')
    nombre = request.POST.get('txtNombreCat')

    categoria = Categoria.objects.get(categoria_id= categoria_id)
    if Categoria.objects.filter(nombre=nombre).exists():
        messages.error(request, '¡Esta categoría no recibio cambios!')
    else:
        categoria.nombre = nombre

        categoria.save()

        messages.success(request, '¡Categoria  Editada!')
    return redirect('configuraciones77')

@login_required(login_url='signin')
def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)
    categoria.delete()
    messages.success(request, '¡Categoría Eliminada!')
    return redirect('configuraciones77')  # O redirige a donde desees después de la eliminación

@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('home')