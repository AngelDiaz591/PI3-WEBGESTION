# Generated by Django 4.2.6 on 2023-10-16 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0021_proveedores_remove_productos_usernamere'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='id_Proveedores',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.proveedores'),
        ),
    ]