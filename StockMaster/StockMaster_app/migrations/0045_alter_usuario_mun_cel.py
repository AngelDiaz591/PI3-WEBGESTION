# Generated by Django 4.2.7 on 2023-11-04 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0044_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='mun_cel',
            field=models.CharField(max_length=10),
        ),
    ]