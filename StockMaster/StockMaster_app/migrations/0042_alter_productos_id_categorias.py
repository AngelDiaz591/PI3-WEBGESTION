# Generated by Django 4.2.6 on 2023-10-31 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0041_remove_productos_marca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='id_categorias',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='StockMaster_app.categoria'),
        ),
    ]