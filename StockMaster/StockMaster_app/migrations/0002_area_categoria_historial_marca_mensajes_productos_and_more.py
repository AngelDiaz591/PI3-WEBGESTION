# Generated by Django 4.2.6 on 2023-11-13 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('StockMaster_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('movi', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('fech_cate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('categoria_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('movi', models.CharField(max_length=255, null=True)),
                ('username', models.CharField(max_length=255, null=True)),
                ('fech_cate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('idhistorial', models.AutoField(primary_key=True, serialize=False)),
                ('movimiento', models.CharField(max_length=255)),
                ('usuario', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('nombre', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('marca_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('movi', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('fech_cate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mensajes',
            fields=[
                ('idcomentario', models.AutoField(primary_key=True, serialize=False)),
                ('comentario', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('tiempo_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('respuestascomentarios', models.CharField(max_length=255, null=True)),
                ('admincont', models.CharField(max_length=255, null=True)),
                ('tiem_res', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('idproducts', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.PositiveBigIntegerField()),
                ('cantPro', models.CharField(max_length=255)),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('hora_baja', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('username', models.CharField(max_length=255, null=True)),
                ('status', models.BooleanField(default=True)),
                ('fecha_edit', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('useredit', models.CharField(max_length=255, null=True)),
                ('movimiento', models.CharField(max_length=255, null=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('idProveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('contacto', models.CharField(max_length=50)),
                ('telefono', models.PositiveBigIntegerField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('calle', models.CharField(default='', max_length=100)),
                ('noExt', models.CharField(default='', max_length=50, null=True)),
                ('noInt', models.CharField(default='', max_length=50, null=True)),
                ('colonia', models.CharField(default='', max_length=100)),
                ('cp', models.PositiveBigIntegerField(default='', max_length=5)),
                ('municipio', models.CharField(default='', max_length=100)),
                ('estado', models.CharField(default='', max_length=100)),
                ('pais', models.CharField(default='', max_length=100)),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
                ('hora_baja', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('username', models.CharField(max_length=255, null=True)),
                ('fecha_edit', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('useredit', models.CharField(max_length=255, null=True)),
                ('movimiento', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RolExtra',
            fields=[
                ('grupo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.group')),
                ('principal', models.BooleanField(default=False)),
                ('inventario', models.BooleanField(default=False)),
                ('productos', models.BooleanField(default=False)),
                ('proveedores', models.BooleanField(default=False)),
                ('etiquetas', models.BooleanField(default=False)),
                ('area', models.BooleanField(default=False)),
                ('productosRecuperacion', models.BooleanField(default=False)),
                ('proveedoresRecuperacion', models.BooleanField(default=False)),
                ('etiquetasRecuperacion', models.BooleanField(default=False)),
                ('designadoRecuperacion', models.BooleanField(default=False)),
                ('usuarios', models.BooleanField(default=False)),
                ('roles', models.BooleanField(default=False)),
                ('soporte', models.BooleanField(default=False)),
                ('contra', models.BooleanField(default=False)),
                ('historialGeneral', models.BooleanField(default=False)),
                ('historialModificaciones', models.BooleanField(default=False)),
                ('historialMovimientos', models.BooleanField(default=False)),
                ('historialEliminados', models.BooleanField(default=False)),
                ('movi', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('fech_cate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('calle', models.CharField(max_length=255)),
                ('colonia', models.CharField(max_length=255)),
                ('num_ext', models.IntegerField()),
                ('num_int', models.IntegerField(null=True)),
                ('cp', models.IntegerField(null=True)),
                ('col_mun', models.CharField(max_length=255)),
                ('pais', models.CharField(max_length=255)),
                ('num_tel', models.IntegerField(null=True)),
                ('mun_cel', models.CharField(max_length=10)),
                ('curp', models.CharField(max_length=18)),
                ('t_sangre', models.CharField(max_length=4)),
                ('rfc', models.CharField(max_length=13)),
                ('n_seg_social', models.CharField(max_length=11)),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('permiso', models.BooleanField(default=True)),
                ('cambio', models.BooleanField(default=True)),
                ('comen', models.CharField(max_length=150)),
                ('id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.AddField(
            model_name='productos',
            name='id_Proveedores',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.proveedores'),
        ),
        migrations.AddField(
            model_name='productos',
            name='id_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.area'),
        ),
        migrations.AddField(
            model_name='productos',
            name='id_categorias',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.categoria'),
        ),
        migrations.AddField(
            model_name='productos',
            name='id_marca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.marca'),
        ),
    ]
