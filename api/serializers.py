from .models import (Province, Municipality, Subsidiary, 
                     Office, Worker, CustomUser, Entrega, Devolucion, Inversion, Role, Venta, Unidad, EntregaEfectivo, CantidadVenta)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Llama al método validate del TokenObtainPairSerializer para obtener los tokens
        data = super().validate(attrs)
        # Obtiene el token de actualización (refresh token) para el usuario actual
        refresh_token = self.get_token(self.user)

        # Agrega los datos adicionales del usuario en la respuesta del token
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,  # Nombre de usuario
            'name': self.user.name,  # Nombre completo del usuario
            'email': self.user.email,  # Correo electrónico
            'role': self.user.role.name if self.user.role else None,  # Rol
        }

        # Incluye los datos del trabajador si existe
        if hasattr(self.user, 'worker'):
            worker = self.user.worker
            data['worker'] = {
                'id': worker.id,
                'name': worker.name,
                'ci': worker.ci,
                'cargo': worker.cargo,
                'office': worker.office.name if worker.office else None,
                'ueb': worker.ueb.name if worker.ueb else None,  # Asegúrate de manejar el caso donde ueb podría ser None
            }

        # Incluye los tokens en la respuesta
        data['refresh_token'] = str(refresh_token)
        data['access_token'] = str(refresh_token.access_token)

        return data

class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(slug_field='name', queryset=Role.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'role', 'password', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    # Sobrescribir la validación para controlar la unicidad
    def validate(self, data):
        user = self.instance  # Instancia actual si se está actualizando

        # Validar el username solo si ha cambiado
        username = data.get('username', None)
        if username and user and user.username != username:
            if CustomUser.objects.filter(username=username).exists():
                raise serializers.ValidationError({"username": "A user with this username already exists."})

        # Validar el email solo si ha cambiado
        email = data.get('email', None)
        if email and user and user.email != email:
            if CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Actualizar los campos restantes
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)

        # Solo actualizar la contraseña si se proporciona
        if password:
            validate_password(password, instance)
            instance.set_password(password)

        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})

        return attrs

    def save(self, user):
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()

###***MUNICIPIO***#####
class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ['id','name']

class MunicipalityProvinceSerializer(serializers.ModelSerializer):
    #province = serializers.SlugRelatedField(slug_field='name', queryset=Province.objects.all())  

    class Meta:
        model = Municipality
        fields = ['id','name', ]

###***PROVINCIA***###
class ProvinceSerializer(serializers.ModelSerializer):   

    class Meta:
        model = Province
        fields = ['id','name',]

###***UEB***###
class SubsidiarySerializer(serializers.ModelSerializer):
    #municipality = serializers.SlugRelatedField(slug_field='name', queryset=Municipality.objects.all())  

    class Meta:
        model = Subsidiary
        fields = ['id','name']

class SubsidiaryListSerializer(serializers.ModelSerializer):
    municipality = MunicipalityProvinceSerializer(read_only=True)  # Mostrar detalles de Municipality

    class Meta:
        model = Subsidiary
        fields = ['name', 'municipality']

###***Base Productiva***###
class OfficeSerializer(serializers.ModelSerializer):
    subsidiary = serializers.SlugRelatedField(slug_field='name',queryset=Subsidiary.objects.all())

    class Meta:
        model = Office
        fields = ['id','name', 'subsidiary']

###***Trabajadores***###
from rest_framework import serializers
from .models import Worker, CustomUser

class WorkerSerializer(serializers.ModelSerializer):
    office = serializers.SlugRelatedField(slug_field='name', queryset=Office.objects.all(), allow_null=True, required=False)
    ueb = serializers.SlugRelatedField(slug_field='name', queryset=Subsidiary.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())

    class Meta:
        model = Worker
        fields = ['id', 'name', 'ci', 'cargo', 'office', 'ueb', 'user']

    def validate_user(self, value):
        # Verificar si el usuario ya tiene un Worker asociado
        if Worker.objects.filter(user=value).exists():
            raise serializers.ValidationError("Este usuario ya tiene un trabajador asociado.")
        return value

###***Modulo presupuesto***###
class EntregaSerializer(serializers.ModelSerializer):
    p_entrega = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())
    p_recibe = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())
    office = serializers.SlugRelatedField(slug_field='name', queryset=Office.objects.all(), allow_null=True, 
    required=False)
    ueb = serializers.SlugRelatedField(slug_field='name',queryset=Subsidiary.objects.all())
    
    class Meta:
        model = Entrega
        fields = ['id','monto', 'p_entrega', 'p_recibe', 'date', 'estado','office','ueb',]

class InversionSerializer(serializers.ModelSerializer):
    trabajador = serializers.SlugRelatedField(slug_field='name', queryset=Worker.objects.all())
    entrega = serializers.PrimaryKeyRelatedField(queryset=Entrega.objects.all())
    monto_entrega = serializers.SerializerMethodField()

    class Meta:
        model = Inversion
        fields = ['id', 'date', 'monto_invertido', 'descripcion', 'trabajador', 'entrega', 'monto_entrega']

    def get_monto_entrega(self, obj):
        return obj.entrega.monto  # Aquí puedes retornar otros campos si lo necesitas
        
class DevolucionSerializer(serializers.ModelSerializer):
    # Campos calculados que no se editarán directamente
    monto_no_invertido = serializers.IntegerField(read_only=True)
    devolucion = serializers.IntegerField(read_only=True)
    ganancia = serializers.IntegerField(read_only=True)
    monto_invertido = serializers.IntegerField(read_only=True)
    monto_venta = serializers.IntegerField(read_only=True)

    monto = serializers.PrimaryKeyRelatedField(queryset=Entrega.objects.all())
     # Este campo mostrará el valor real del monto en el frontend
    monto_valor = serializers.SerializerMethodField()

    p_entrega = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())
    p_recibe = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())

    class Meta:
        model = Devolucion
        fields = ['id', 'p_entrega', 'p_recibe','monto_no_invertido',  'ganancia', 'date', 'devolucion','monto_invertido','monto_venta', 'efectivo_devolver','monto_valor','monto']
        read_only_fields = ['monto_no_invertido', 'ganancia','devolucion','monto_invertido','monto_venta']  # Asegura que estos campos no se puedan modificar

    # Método para obtener el valor real del monto
    def get_monto_valor(self, obj):
        return obj.monto.monto  # 'monto' es el campo en la tabla 'Entrega' que contiene el valor del monto

    def get_monto_invertido(self, obj):
        return obj.monto_invertido.monto_invertido

    def create(self, validated_data):
    # Asegúrate de que validated_data contenga un monto válido
        print(validated_data)  # O usar logging
        return Devolucion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.p_entrega = validated_data.get('p_entrega', instance.p_entrega)
        instance.p_recibe = validated_data.get('p_recibe', instance.p_recibe)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.efectivo_devolver = validated_data.get('efectivo_devolver', instance.efectivo_devolver)

        # Guarda la instancia
        instance.save()
        return instance

    #def save(self, **kwargs):
        #devolucion = super().save(**kwargs)
        # Cambiar el estado de la entrega a cerrado
        ##devolucion.entrega.estado = False
        #devolucion.entrega.save()
        #return devolucion

###***Ventas***###
class VentaSerializer(serializers.ModelSerializer):
    entrega = serializers.PrimaryKeyRelatedField(queryset=Entrega.objects.all())
  
    class Meta:
        model = Venta
        fields = ['id','cantidad_venta', 'entrega','date', 'descripcion']

###***Role***###
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','name','descriptions']

####***Por Concepto de Ventas***###
###UnidadSerializer###
class UnidadSerializer(serializers.ModelSerializer):
    ueb = serializers.PrimaryKeyRelatedField(queryset=Subsidiary.objects.all())

    class Meta:
        model = Unidad
        fields = ['id','name', 'ueb']

class EntregaEfectivoSerializer(serializers.ModelSerializer):
    p_entrega = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())
    p_recibe = serializers.SlugRelatedField(slug_field='name',queryset=Worker.objects.all())
    unidad = serializers.SlugRelatedField(slug_field='name',queryset=Unidad.objects.all())

    class Meta:
        model = EntregaEfectivo
        fields = ['id','date','p_entrega', 'p_recibe', 'efectivo', 'unidad']

class CantidadVentaSerializer(serializers.ModelSerializer):
    unidad = serializers.PrimaryKeyRelatedField(queryset=Unidad.objects.all())
    entrega_efectivo = serializers.PrimaryKeyRelatedField(queryset=EntregaEfectivo.objects.all())

    class Meta:
        model = CantidadVenta
        fields = ['id','name','efectivo','entrega_efectivo', 'unidad']















