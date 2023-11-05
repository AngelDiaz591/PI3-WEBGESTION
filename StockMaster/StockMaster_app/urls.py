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
    path('logout/', views.exit, name='exit'),
    
    #paths Registro
    path('cambio_password/', views.cambio_password, name='cambio_password'),
    path('usuarios/eliminaruser/<int:id>', views.eliminaruser, name="eliminaruser"),

    #paths Productos
    path('productos/', views.pro, name='productos'),
    path('registrarProducto/', views.registrarProducto),
    path('productos/edicioninventario2/<int:idproducts>/', views.edicioninventario2, name='edicioninventario2'),
    path('editarProducto2/', views.editarProductoMod),

    path('productos/status/<int:idproducts>/', views.cambio_status, name='cambio_status'),
    path('recuperar_producto/statusre/<int:idproducts>/', views.cambio_statusre, name='recuperar_producto/statusre'),
    path('recuperar_producto/eliminaInventario/<idproducts>', views.eliminaInventario),
    
    #paths Proveedores
    path('prov/', views.prov, name='prov'),
    path('registrarProv/', views.registrarProv),
    path('prov/edicionProveedor2/<int:idProveedor>', views.edicionProveedor2, name='edicionProveedor2'),
    path('editarProveedor2/', views.editarProveedorMod),

    path('prov/cambio_statuspro/<int:idProveedor>',views.cambio_statuspro, name='cambio_statuspro'),
    path('recuperar_proveedor/cambio_statusrepro/<int:idProveedor>', views.cambio_statusrepro, name='recuperar_proveedor/cambio_statusrepro/'),
    path('eliminaProveedor/<idProveedor>', views.eliminaProveedor),

    #paths Categorias
    path('config/', views.configuraciones, name='configuraciones77'),
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

    path('recuperar_marca/cambio_statusremar1/<int:marca_id>/', views.cambio_statusremar, name="recuperar_marca/cambio_statusremar1"),
    path('cambio_statusmar/<int:marca_id>/', views.cambio_statusmar, name='cambio_statusmar'),
    path('eliminar-marca/<int:marca_id>/', views.eliminar_marca, name='eliminarmarcas'),

    #paths comentarios
    path('actividades/eliminarcomentarios/<int:idcomentario>/', views.eliminarcomentarios, name='eliminar_comentario'),
    path('contestarcomentarios/<int:idcomentario>/', views.contestarcomentarios, name='contestarcomentarios'),

    #paths funciones
    path('get_char/', views.get_char, name='get_char'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('editarcant/<int:idproducts>/', views.editarcant, name='editarcant'),

    #paths html
    path('actividades/',views.productos,name='actividades'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('historial/', views.historial, name='historial'),
    path('soporte/', views.soporte, name='soporte'),
    path('inventario/', views.example_view, name='inventario'),
    path('comentario/',views.comentario),
    path('recuperar_producto/', views.recuperar_producto, name='recuperar_producto'),

    #nueva idea, ¿confirmación? del caso contrario solo elimine
    path('recuperar_marca/', views.recuperar_marca, name='recuperar_marca'),
    path('recuperar_proveedor/', views.recuperar_proveedor, name='recuperar_proveedor'),
    path('recuperar_categoria/', views.recuperar_categoria, name='recuperar_categoria'),

    #nueva idea pt2, ¿confirmación? del caso contrario solo elimine
    path('historial_eliminacion/', views.historial_eliminacion, name='historial_eliminacion'),
    path('historial_edición/', views.historial_edicion, name='historial_edicion'),
    path('historial_recuperacion/', views.historial_recuperacion, name='historial_recuperacion'),
    path('historial_registro/', views.historial_registro, name='historial_registro'),
    ]