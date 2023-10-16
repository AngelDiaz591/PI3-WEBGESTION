# Generated by Django 4.2.6 on 2023-10-16 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0020_productos_movimiento'),
    ]

    operations = [
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
                ('estatus', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='productos',
            name='usernamere',
        ),
    ]
