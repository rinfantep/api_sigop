from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework import serializers
from django.db.models import Sum

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# models.py

####Role####
class Role(models.Model):
    name = models.CharField(max_length=50)
    descriptions = models.TextField(max_length=500)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo de nombre de usuario es obligatorio.')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Ensuring superuser is active
        
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permite acceso al admin
    is_superuser = models.BooleanField(default=False)  # Permite acceso total a todos los recursos
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE,null=True, blank=True)

    def set_password(self, raw_password):
        super().set_password(raw_password)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'CustomUser'
        permissions = [
            ('can_view_dashboard', 'Can view dashboard'),
            ('can_edit_profile', 'Can edit profile'),
        ]

# Create your models here.


# UEB
class Subsidiary(models.Model):
    name = models.CharField(max_length=100)
    #municipality = models.ForeignKey(Municipality, related_name='subsidiaries', on_delete=models.CASCADE)

    def __str__(self):
        return  self.name
        #'%s (%s, %s)' % (self.municipality.name, self.municipality.province.name)

# Bases Productivas
class Office(models.Model):
    name = models.CharField(max_length=100)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' % (self.name, self.subsidiary)

# Trabajadores
class Worker(models.Model):  
    name = models.CharField(max_length=100) 
    ci = models.CharField(max_length=11, unique=True)  
    cargo = models.CharField(max_length=100)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    ueb = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker')


    def __str__(self):
        return self.name


####Modulo Presupuesto####
class Entrega(models.Model):
    monto = models.IntegerField()
    p_entrega = models.ForeignKey(Worker, related_name='personas_entregan', on_delete=models.CASCADE)
    p_recibe = models.ForeignKey(Worker, related_name='personas_reciben', on_delete=models.CASCADE)
    date = models.DateField( auto_now_add=False)
    estado = models.BooleanField(default=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    ueb = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.monto)

class Inversion(models.Model):
    date = models.DateField( auto_now_add=False)
    monto_invertido = models.IntegerField()
    descripcion = models.CharField(max_length=500)
    trabajador = models.ForeignKey(Worker, related_name='inversion', on_delete=models.CASCADE) 
    entrega = models.ForeignKey(Entrega, related_name='inversion', on_delete=models.CASCADE)  

    def __str__(self):
        return str(self.monto_invertido)



class Venta(models.Model):
    date = models.DateField( auto_now_add=False) 
    cantidad_venta = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=500,null=True, blank=True)
    entrega = models.ForeignKey(Entrega, related_name='venta', on_delete=models.CASCADE)  

    def __str__(self):
        return str(self.cantidad_venta)


class Devolucion(models.Model):
    p_entrega = models.ForeignKey(Worker, related_name='entrega', on_delete=models.CASCADE)
    p_recibe = models.ForeignKey(Worker, related_name='recibe', on_delete=models.CASCADE)
    monto = models.ForeignKey(Entrega, related_name='devoluciones', on_delete=models.CASCADE)
    monto_invertido = models.IntegerField(default=0, editable=False)
    monto_no_invertido = models.IntegerField(editable=False)
    monto_venta = models.IntegerField(default=0, editable=False)  # Cambiar a IntegerField
    ganancia = models.IntegerField(default=0, editable=False)
    devolucion = models.IntegerField(default=0, editable=False)
    date = models.DateField(auto_now_add=False)
    
    efectivo_devolver = models.FloatField(default=0)
    

    def get_monto_value(self):
        if self.monto:
            return self.monto.monto  
        return 'No monto'

    def get_monto_invertido_value(self):
        if self.monto_invertido:
            return self.monto_invertido.monto_invertido  
        return 'No monto'

    def get_monto_venta_value(self):
        if self.monto_venta:
            return self.monto_venta.cantidad_venta  
        return 'No monto' 

    def save(self, *args, **kwargs):
        # Suma todas las ventas relacionadas con la entrega actual
        total_ventas = Venta.objects.filter(entrega=self.monto).aggregate(Sum('cantidad_venta'))['cantidad_venta__sum'] or 0
        self.monto_venta = total_ventas
        
        # Suma todas las inversiones relacionadas con la entrega actual
        total_inversiones = Inversion.objects.filter(entrega=self.monto).aggregate(Sum('monto_invertido'))['monto_invertido__sum'] or 0
        
        # Actualiza el campo `monto_invertido` con el total de inversiones
        self.monto_invertido = total_inversiones  # Cambia esto si necesitas un campo para el total
        
        # Calcula el monto no invertido
        self.monto_no_invertido = (self.monto.monto or 0) - total_inversiones
        
        # Calcula la ganancia y la devolución
        self.ganancia = self.monto_venta - total_inversiones
        self.devolucion = self.monto_venta + self.monto_no_invertido

         # Guarda la devolución
        super(Devolucion, self).save(*args, **kwargs)

        # Cerrar la entrega al crear una devolución
        self.cerrar_entrega()

    def cerrar_entrega(self):
        # Obtener la entrega relacionada con esta devolución
        entrega = self.monto

        # Cambiar el estado de la entrega a cerrado
        entrega.estado = False  # False indica que la entrega está cerrada
        entrega.save()

    
####Por Conceptos de Ventas####
class Unidad(models.Model):
    name = models.CharField(max_length=50)
    ueb = models.ForeignKey(Subsidiary, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class EntregaEfectivo(models.Model):
    date = models.DateField(auto_now=False)
    p_entrega = models.ForeignKey(Worker, related_name='entrega_efectivo', on_delete=models.CASCADE)
    p_recibe = models.ForeignKey(Worker, related_name='recibe_efectivo', on_delete=models.CASCADE)
    efectivo = models.IntegerField(default=0)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.efectivo)
    

class CantidadVenta(models.Model):
    name = models.CharField(max_length=50)
    efectivo = models.IntegerField(default=0)
    entrega_efectivo = models.ForeignKey(EntregaEfectivo, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)







    






    
    






