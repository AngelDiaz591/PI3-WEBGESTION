"""
URL configuration for StockMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    
    #paths Login
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('terminos/', views.terminos, name='terminos'),
    path('logout/', views.exit, name='exit'),
    
    #paths Registro
    path('cambio/<str:uidb64>/<str:token>/', views.cambio, name="cambio"),
    path('cambio_password/permiso/<int:id>', views.permiso, name='permiso'),
    path('cambio_password/', views.cambio_password, name='cambio_password'),
    path('recuperar_usuario/eliminaruser/<int:id>', views.eliminaruser, name="eliminaruser"),
    path('usuarios/dar_baja/<int:id>', views.dar_baja, name="dar_baja"),
    path('recuperar_usuario/', views.recuperar_usuario, name="recuperar_usuario"),
    path('recuperar_usuario/recuperar/<int:id>', views.recuperar, name='recuperar'),
    path('cambio_password/descripcion/<int:id_usuario>',views.descripcion, name="descripcion"),

    #paths Productos
    path('productos/', views.pro, name='productos'),
    path('registrarProducto/', views.registrarProducto),
    path('productos/edicioninventario2/<int:idproducts>/', views.edicioninventario2, name='edicioninventario2'),
    path('editarProducto2/', views.editarProductoMod),

    path('productos/status/<int:idproducts>/', views.cambio_status, name='cambio_status'),
    path('statusre/<int:idproducts>/', views.cambio_statusre, name='statusre'),
    path('eliminaInventario/<idproducts>', views.eliminaInventario),
    
    #paths Proveedores
    path('prov/', views.prov, name='prov'),
    path('registrarProv/', views.registrarProv),
    path('prov/edicionProveedor2/<int:idProveedor>', views.edicionProveedor2, name='edicionProveedor2'),
    path('editarProveedor2/', views.editarProveedorMod),

    path('prov/cambio_statuspro/<int:idProveedor>',views.cambio_statuspro, name='cambio_statuspro'),
    path('cambio_statusrepro/<int:idProveedor>', views.cambio_statusrepro, name='cambio_statusrepro'),
    path('eliminaProveedor/<idProveedor>', views.eliminaProveedor),

    #paths Areas
    path('area/', views.area, name='area'),
    path('registraArea/', views.registrar_area),
    path('area/edicionArea2/<int:area_id>', views.edicionArea2, name='edicionArea2'),
    path('editarArea2/', views.editarAreaMod),

    path('status_area/<int:area_id>/',views.status_area,name='status_area'),
    path('status_areare/<int:area_id>/',views.status_areare, name="status_areare"),
    path('eliminar_area/<int:area_id>/', views.eliminar_area, name='eliminar_area'),

    #paths Categorias
    path('config/', views.configuraciones, name='etiquetas'),
    path('registrar_categoria/', views.registrar_categoria, name='registrar_cat'),
    path('config/edicionCategoria2/<int:categoria_id>/', views.edicionCategoria2, name='edicionCategoria2'),
    path('editarCategoria2/', views.editarCategoriaMod),

    path('status_categoria/<int:categoria_id>/',views.status_categoria,name='status_categoria'),
    path('status_categoriare/<int:categoria_id>/',views.status_categoriare, name="status_categoriare"),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminarcategoria'),

    #paths Marcas
    path("MarcaVista/",views.MarcaView, name="marca"),
    path("MarcaAgregada/", views.registrar_marca, name="marcaAgred"),
    path('config/edicionMarca2/<int:marca_id>/', views.edicionMarca2, name='edicionMarca2'),
    path('editarMarca2/', views.editarMarcaMod),

    path('cambio_statusremar/<int:marca_id>/', views.cambio_statusremar, name="cambio_statusremar"),
    path('cambio_statusmar/<int:marca_id>/', views.cambio_statusmar, name='cambio_statusmar'),
    path('eliminar-marca/<int:marca_id>/', views.eliminar_marca, name='eliminarmarcas'),

    #paths Roles
    path("rol/",views.RolView, name="rol"),
    path("registrar_rol/", views.registrar_rol, name="registrar_rol"),
    path('rol/edicionRol2/<int:id>/', views.edicionRol2, name='edicionRol2'),
    path('editarRol2/', views.editarRolMod),

    path('cambio_statusrolre/<int:id>/', views.cambio_statusrolre, name="cambio_statusrolre"),
    path('cambio_statusrol/<int:id>/', views.cambio_statusrol, name='cambio_statusrol'),
    path('eliminar_rol/<int:id>/', views.eliminar_rol, name='eliminarRol'),

    #paths comentarios
    path('actividades/eliminarcomentarios/<int:idcomentario>/', views.eliminarcomentarios, name='eliminar_comentario'),
    path('contestarcomentarios/<int:idcomentario>/', views.contestarcomentarios, name='contestarcomentarios'),

    #paths funciones
    path('get_char/', views.get_char, name='get_char'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('editarcant/<int:idproducts>/', views.editarcant, name='editarcant'),

    #paths html
    path('actividades/',views.productos,name='actividades'),
    path('inventario/', views.example_view, name='inventario'),

    path('recuperar_producto', views.recuperar_producto, name='recuperar_producto'),
    path('recuperar_proveedor', views.recuperar_proveedor, name='recuperar_proveedor'),
    path('recuperar_designaciones', views.recuperar_designaciones, name='recuperar_designaciones'),
    path('recuperar_etiquetas', views.recuperar_etiquetas, name='recuperar_etiquetas'),

    path('historial/', views.historial, name='historial'),
    path('historialModificaciones/', views.historialModificaciones, name='historialModificaciones'),
    path('historialMovimientos/', views.historialMovimientos, name='historialMovimientos'),
    path('historialEliminados/', views.historialEliminados, name='historialEliminados'),

    path('soporte/', views.soporte, name='soporte'),
    path('soporteEnviar/', views.soporteEnviar, name='soporteEnviar'),
    path('comentario/',views.comentario),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('acercaDe/', views.acercaDe, name='acercaDe'),
    path('acercaDe/terminos', views.terminosYcondiones, name='terminosCon'),

    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),
    
    #paths de ordenes
    path('ordenes/', views.ordenes, name='ordenes'),
    path('nuevaOrden/', views.nuevaOrden, name='nueva_orden'),
    path('eliminarOrden/<int:id_Orden>/', views.eliminarOrden, name='eliminar_orden')
    ]