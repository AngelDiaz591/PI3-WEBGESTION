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
    path('actividades/',views.productos,name='actividades'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/eliminaruser/<int:id>', views.eliminaruser, name="eliminaruser"),
    path('soporte/', views.soporte, name='soporte'),
    path('comentario/',views.comentario),
    path('actividades/eliminarcomentarios/<int:idcomentario>/', views.eliminarcomentarios, name='eliminar_comentario'),
    path('contestarcomentarios/<int:idcomentario>/', views.contestarcomentarios, name='contestarcomentarios'),
    path('inventario/', views.example_view, name='inventario'),
    path('productos/', views.pro, name='productos'),
    path('recuperar_producto', views.recuperar_producto, name='recuperar_producto'),
    path('registrarProducto/', views.registrarProducto),
    path('editarcant/<int:idproducts>/', views.editarcant, name='editarcant'),
    path('productos/edicioninventario/<idproducts>', views.edicioninventario),
    path('editarProducto/', views.editarProducto),
    path('productos/status/<int:idproducts>/', views.cambio_status, name='cambio_status'),
    path('statusre/<int:idproducts>/', views.cambio_statusre, name='cambio_statusre'),
    path('recuperar_producto/eliminaInventario/<idproducts>', views.eliminaInventario),
    path('config', views.configuraciones, name='configuraciones77'),
    path('registrar_categoria/', views.registrar_categoria, name='registrar_cat'),
    path('edicioncategoria/<int:categoria_id>/', views.edicion_categoria, name='edicionicat'),
    path('editarCat/', views.editarCat, name='editar_cat'),
    path('get_char/', views.get_char, name='get_char'),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminarcategoria'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.exit, name='exit'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    ]