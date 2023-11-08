# Generated by Django 4.2.6 on 2023-11-05 00:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0045_alter_usuario_mun_cel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('idRoles', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('inventario', models.PositiveBigIntegerField(max_length=2)),
                ('movi', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('fech_cate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('status', models.BooleanField(default=True)),
                ('status_mov', models.BooleanField(default=True)),
            ],
        ),
    ]