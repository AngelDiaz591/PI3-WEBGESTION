# Generated by Django 4.2.6 on 2023-10-17 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0034_rename_estatus_mov_proveedores_status_mov'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajes',
            name='status',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='mensajes',
            name='status_mov',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
