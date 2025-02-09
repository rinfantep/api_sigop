# Generated by Django 5.0.7 on 2024-09-26 20:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('descriptions', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Subsidiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='api.role')),
            ],
            options={
                'db_table': 'CustomUser',
                'permissions': [('can_view_dashboard', 'Can view dashboard'), ('can_edit_profile', 'Can edit profile')],
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subsidiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.subsidiary')),
            ],
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.IntegerField()),
                ('date', models.DateField()),
                ('estado', models.BooleanField(default=True)),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.office')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.subsidiary')),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.office')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transaction')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transactiontype')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cantidad_venta', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=100)),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venta', to='api.entrega')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ci', models.CharField(max_length=11, unique=True)),
                ('cargo', models.CharField(max_length=100)),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.office')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.subsidiary')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('monto_invertido', models.IntegerField()),
                ('descripcion', models.CharField(max_length=500)),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inversion', to='api.entrega')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inversion', to='api.worker')),
            ],
        ),
        migrations.AddField(
            model_name='entrega',
            name='p_entrega',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personas_entregan', to='api.worker'),
        ),
        migrations.AddField(
            model_name='entrega',
            name='p_recibe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personas_reciben', to='api.worker'),
        ),
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_invertido', models.IntegerField(default=0, editable=False)),
                ('monto_no_invertido', models.IntegerField(editable=False)),
                ('monto_venta', models.IntegerField(default=0, editable=False)),
                ('ganancia', models.IntegerField(default=0, editable=False)),
                ('devolucion', models.IntegerField(default=0, editable=False)),
                ('date', models.DateField()),
                ('efectivo_devolver', models.FloatField(default=0)),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dev', to='api.entrega')),
                ('monto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devoluciones', to='api.entrega')),
                ('p_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrega', to='api.worker')),
                ('p_recibe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recibe', to='api.worker')),
            ],
        ),
    ]
