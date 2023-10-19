# Generated by Django 4.2.6 on 2023-10-17 03:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0026_historial_mensajes_status_mensajes_status_mov_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='fech_cate',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='movi',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='status_mov',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]