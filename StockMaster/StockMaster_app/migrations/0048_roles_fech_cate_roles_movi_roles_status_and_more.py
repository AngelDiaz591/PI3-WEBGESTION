# Generated by Django 4.2.6 on 2023-11-05 01:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('StockMaster_app', '0047_remove_roles_fech_cate_remove_roles_movi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roles',
            name='fech_cate',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='movi',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='status_mov',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]