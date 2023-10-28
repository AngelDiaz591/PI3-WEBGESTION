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
from .models import Productos, Mensajes, Categoria, Proveedores, Historial, Marca
from django.http.response import JsonResponse
import base64
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist 
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
    ProveedoresListados = Proveedores.objects.all()
    MarcaListados = Marca.objects.all()
    return render(request, 'StockMaster_app/actividades.html', {'Mensajes': mensajes, 'cantidad_mensajes':cantidad_mensajes,'marca': MarcaListados, ' Productos':ProductosListados,'CategoriaListados':CategoriaListados, 'ProveedoresListados' : ProveedoresListados})

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
        ProveedoresListados = Proveedores.objects.all()
        MarcaListados = Marca.objects.all() 
        for producto in ProductosListados:
            producto.imagen_url = get_imagen_url(producto.imagen)
        return render(request, 'StockMaster_app/productos.html', { "Productos": ProductosListados,"Categoria": CategoriaListados,'marca': MarcaListados, 'Proveedor' : ProveedoresListados,'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
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
    #marca = request.POST['NomMarca']
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





#EDICION DE OTRA PAGINA
@login_required(login_url='signin')
def edicioninventario(request, idproducts):
    productos = Productos.objects.get(idproducts= idproducts)
    CategoriaListados = Categoria.objects.all() 
    ProveedorListados = Proveedores.objects.all()
    MarcaListados = Marca.objects.all()
    imagen_url = get_imagen_url(productos.imagen)
    return render(request, "StockMaster_app/edicioninventario.html", {"productos": productos, "imagen_url": imagen_url, "Categoria": CategoriaListados, 'Proveedor' : ProveedorListados, 'marca' : MarcaListados})
@login_required(login_url='signin')

def editarProducto(request):
    idproducts = request.POST.get('idproducts')
    codigo = request.POST.get('txtCodigo')
    nombre = request.POST.get('txtNombre')
    precio = request.POST.get('NumPrecio')
    #marca = request.POST.get('NomMarca')
    cantPro = request.POST.get('CantPro')
    nueva_imagen = request.FILES.get('imagen') 
    categoria_id = request.POST.get('categoria') 
    idProveedor = request.POST.get('proveedor')
    marca_id = request.POST.get('marca')
    productos = Productos.objects.get(idproducts=idproducts)

    productos.codigo = codigo
    productos.nombre = nombre
    productos.precio = precio
    #productos.marca = marca
    productos.cantPro = cantPro
    productos.username = request.user.username
    productos.movimiento = 'Edicion de Producto'
    productos.fecha_edit = timezone.now()
    productos.id_categorias_id = categoria_id
    productos.id_Proveedores_id= idProveedor
    productos.id_marca_id= marca_id
    if nueva_imagen:
        productos.imagen = nueva_imagen.read()
    productos.save()

    messages.success(request, '¡Producto Editado!')
    return redirect('/productos/')




# EDICON DENTRO DEL MODAL CARGANDO LOS DATOS

#EDICION MODAL
@login_required
def edicioninventario2(request, idproducts):
    productos = Productos.objects.get(idproducts=idproducts)
    CategoriaListados = Categoria.objects.all()
    ProveedorListados = Proveedores.objects.all()
    imagen_url = get_imagen_url(productos.imagen)

    data = {
        "productos": {
            "codigo": productos.codigo,
            "nombre": productos.nombre,
            "precio": productos.precio,
            "marca": productos.marca,
            "cantPro": productos.cantPro,
            "id_categorias": productos.id_categorias.categoria_id,
            "id_Proveedores": productos.id_Proveedores.idProveedor,
        },
        "imagen_url": imagen_url,
        "Categoria": [{"categoria_id": c.categoria_id, "nombre": c.nombre} for c in CategoriaListados],
        "Proveedor": [{"idProveedor": c.idProveedor, "nombre": c.nombre} for c in ProveedorListados],
    }

    
    return JsonResponse(data)      
    #return render(request, 'StockMaster_app/productos.html', data)   

@login_required(login_url='signin')
def editarProductoMod(request):
    try:
        idproducts = request.POST.get('productId')
        codigo = request.POST.get('txtCodigo')
        nombre = request.POST.get('txtNombre')
        precio = request.POST.get('NumPrecio')
        marca = request.POST.get('NomMarca')
        cantPro = request.POST.get('CantPro')
        nueva_imagen = request.FILES.get('imagen') 
        categoria_id = request.POST.get('categoria') 
        idProveedor = request.POST.get('proveedor')

        try:
            productos = Productos.objects.get(idproducts=idproducts)
        except ObjectDoesNotExist:
            messages.error(request, 'El producto no se encontró o no existe.')
            return redirect('/productos/')  # Puedes redirigir a donde desees

        productos.codigo = codigo
        productos.nombre = nombre
        productos.precio = precio
        productos.marca = marca
        productos.cantPro = cantPro
        productos.username = request.user.username
        productos.movimiento = 'Edicion de Producto'
        productos.fecha_edit = timezone.now()
        productos.id_categorias_id = categoria_id
        productos.id_Proveedores_id = idProveedor
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
    return redirect('/recuperar_producto')
    
def elimina_menpro(request, idProveedor):
    proveedores = Proveedores.objects.get(idProveedor=idProveedor)
    if proveedores.status_mov !=0:
        proveedores.status_mov = 0
        proveedores.save()
    return redirect('/actividades')

def elimina_men(request, idproducts):
    productos = Productos.objects.get(idproducts=idproducts)
    if productos.status_mov !=0:
        productos.status_mov = 0
        productos.save()
    return redirect('/actividades')
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
@login_required(login_url='signin')
def status_mov (resquest,idcomentario):
    status=Mensajes.objects.get(idcomentario=idcomentario)
    if status.status_mov != 0:
        status.status_mov = 0
        status.save()
    return redirect('/actividades')

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
    MarcaListados = Marca.objects.all()
    return render(request, 'StockMaster_app/configuraciones.html',{"Categoria": CategoriaListados,"marcas":MarcaListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})

@login_required(login_url='signin')
def recuperar_producto(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    proveedores = Proveedores.objects.all()
    return render(request, 'StockMaster_app/recuperar_producto.html', { "Productos": ProductosListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"proveedores":proveedores})

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
    return redirect('configuraciones77')
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
    return redirect('configuraciones77')

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
    return redirect('/recuperar_producto')

@login_required(login_url='signin')
def status_mov_cate (resquest,categoria_id):
    status_cate=Categoria.objects.get(categoria_id=categoria_id)
    if status_cate.status_mov != 0:
        status_cate.status_mov = 0
        status_cate.save()
    return redirect('/actividades')

@login_required(login_url='signin')
def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(categoria_id=categoria_id)
    categoria.delete()
    messages.success(request, '¡Categoría Eliminada!')
    return redirect('/recuperar_producto')  # O redirige a donde desees después de la eliminación

@login_required(login_url='signin')
def exit(request):
    logout(request)
    return redirect('home')

#Vistas de proveedores

#Para acceder al apartado de proveedores
@login_required(login_url='signin')
def prov(request):
    if request.user.is_superuser:
        mensajes = Mensajes.objects.all()
        cantidad_mensajes = mensajes.count()
        ProveedoresListados = Proveedores.objects.all()
        for proveedor in ProveedoresListados:
            proveedor.imagen_url = get_imagen_url(proveedor.imagen)
        return render(request, 'StockMaster_app/proveedor.html', { "Proveedor": ProveedoresListados, 'Mensajes':mensajes, 'cantidad_mensajes':cantidad_mensajes})
    else:
        return redirect('/prov')

#Registro Proveedores
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

#edicion de proveedores

#para acceder a la pagina de edicion proveedores
@login_required(login_url='signin')
def edicionproveedor(request, idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor) 
    imagen_url = get_imagen_url(proveedor.imagen)
    return render(request, "StockMaster_app/edicionproveedor.html", {"proveedor": proveedor, "imagen_url": imagen_url})

#funcion de editar proveedores
@login_required(login_url='signin')
def editarproveedor(request):
    idProveedor = request.POST.get('idProveedor')
    nombre = request.POST.get('nombre')
    contacto = request.POST.get('contacto')
    telefono = request.POST.get('telefono')
    email = request.POST.get('email')
    calle = request.POST.get('calle')
    noExt = request.FILES.get('noExt') 
    noInt = request.POST.get('noInt') 
    colonia = request.POST.get('colonia')
    cp = request.POST.get('cp')
    municipio = request.POST.get('municipio')
    estado = request.POST.get('estado')
    nueva_imagen = request.FILES.get('imagen') 
    pais = request.POST.get('pais')


    proveedor = Proveedores.objects.get(idProveedor=idProveedor)

    proveedor.nombre = nombre
    proveedor.contacto = contacto
    proveedor.telefono = telefono
    proveedor.email = email
    proveedor.calle = calle
    proveedor.noExt = noExt
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
    return redirect('/prov')
 
 #eliminar proveedor (se cambia el estatus a 0)
@login_required(login_url='signin')
def eliminaProveedor(request, idProveedor):
    proveedor = Proveedores.objects.get(idProveedor=idProveedor)
    historial= Historial.objects.all()
    historial = Historial(movimiento='Proveedor Eliminado',usuario=request.user.username,fecha=timezone.now(),nombre=proveedor.nombre)
    historial.save()
    proveedor.delete()
    messages.success(request, '¡Proveedor Eliminado!')
    return redirect('/recuperar_producto')
@login_required(login_url='signin')
def historial(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes =mensajes.count()
    ProductosListados = Productos.objects.all()
    CategoriaListados = Categoria.objects.all()
    historial = Historial.objects.all()
    return render(request, 'StockMaster_app/historial.html', { "Productos": ProductosListados,"Categoria": CategoriaListados,"mensajes":mensajes,"cantidad_mensajes":cantidad_mensajes,"historial":historial})

@login_required(login_url='signin')
def MarcaView(request):
    mensajes = Mensajes.objects.all()
    cantidad_mensajes = mensajes.count()
    MarcaListados = Marca.objects.all()
    CategoriaListados = Categoria.objects.all()
    return render(request, 'StockMaster_app/configuraciones.html', {"marcas": MarcaListados,"Categoria": CategoriaListados,'Mensajes': mensajes, 'cantidad_mensajes': cantidad_mensajes})

@login_required(login_url='signin')
def registrar_marca(request):
    if request.method == 'POST':
        nombre = request.POST['txtMarcaNew']
        if Marca.objects.filter(nombre=nombre).exists():
            messages.error(request, 'La marca ya está registrada.')
        else:
            marca = Marca(nombre=nombre, username=request.user.username, fech_cate=timezone.now(), movi='Creación de Marca')
            historial = Historial(movimiento='Marca Agregada', usuario=request.user.username, fecha=timezone.now(), nombre=nombre)
            historial.save()
            marca.save()
            messages.success(request, '¡Marca registrada con éxito!')
        return HttpResponseRedirect('/MarcaVista/')  # Redirige a la URL deseada después de procesar el formulario
    return render(request, 'StockMaster_app/configuraciones.html')

@login_required(login_url='signin')
def edicionMarcaView(request, marca_id):
    marca = Marca.objects.get(marca_id= marca_id)
    return render(request, "StockMaster_app/edicion_marca.html", {"marca": marca})

@login_required(login_url='signin')
def editarMarca(request):
    marca_id = request.POST.get('idMarca')
    nombre = request.POST.get('txtMarcaNew')
    marca = Marca.objects.get(marca_id= marca_id)
    if Marca.objects.filter(nombre=nombre).exists():
        messages.error(request, '¡Esta Marca no recibio cambios!')
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
    return redirect('marca')

@login_required(login_url='signin')
def eliminar_marca(request, marca_id):
    marca = Marca.objects.get(marca_id=marca_id)
    marca.delete()
    messages.success(request, '¡Marca Eliminada!')
    return redirect('marca')  # O redirige a donde desees después de la eliminación