# Generated by Django 5.0.7 on 2024-09-27 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_entrega_monto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devolucion',
            name='entrega',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='descripcion',
        ),
    ]
