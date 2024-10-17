from django.contrib import admin
from .models import (Province, Municipality, Subsidiary, Office,  Worker, CustomUser, Entrega, Devolucion, Inversion, Role, Venta, Unidad, EntregaEfectivo, CantidadVenta)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id','name',) 
    search_fields = ('name',) 
    ordering = ('name',)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('id','name', )
    search_fields = ('name', )  
    ordering = ('name',)

@admin.register(Subsidiary)
class SubsidiaryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',) 
    list_filter = ('name',)
    ordering = ('name',)
    #autocomplete_fields = ['municipality']  

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'subsidiary')
    search_fields = ('name', 'subsidiary__name')  
    list_filter = ('subsidiary',)
    ordering = ('name',)
    autocomplete_fields = ['subsidiary']  




@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ci','cargo', 'office','ueb','user')
    search_fields = ('name', 'ci','cargo', 'office__name')  
    list_filter = ('office',)  
    ordering = ('name',)
    autocomplete_fields = ['office']  
    list_display_links = ('name',)  

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'office':
            kwargs['queryset'] = Office.objects.select_related('subsidiary').order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# admin.py
@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('username',)
    list_display = ('id', 'username', 'name', 'email','role', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'name', 'email','role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email','role', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    
    search_fields = ('username',)
    filter_horizontal = ('user_permissions',)
    
    

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('monto', 'p_entrega','p_recibe','date', 'estado', 'office','ueb',)
    search_fields = ('monto', 'p_entrega')  
    list_filter = ('p_entrega',)
    ordering = ('monto',)

@admin.register(Inversion)
class InversionAdmin(admin.ModelAdmin):
    list_display = ('monto_invertido', 'trabajador','date','descripcion')
    search_fields = ('monto_invertido', 'trabajador','descripcion')  
    list_filter = ('trabajador',)
    ordering = ('monto_invertido',)

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista
    list_display = ('id', 'p_entrega', 'p_recibe', 'get_monto_value', 'monto_invertido', 'monto_no_invertido', 'monto_venta', 'ganancia', 'date', 'devolucion')
    
    # Filtros laterales
    list_filter = ('p_entrega', 'p_recibe', 'date')
    
    # Campos que se pueden buscar en la barra de búsqueda
    search_fields = ('p_entrega__name', 'p_recibe__name', 'monto__id')
    
    # Campos que serán solo de lectura en el formulario de admin
    readonly_fields = ('monto_no_invertido', 'ganancia', 'date', 'devolucion')
    
    # Ordenar por fecha, descendente
    ordering = ('-date',)

    # Mostrar el valor del monto en lugar del id
    def get_monto_value(self, obj):
        if obj.monto:
            return f"ID: {obj.monto.id} - Valor: {obj.monto.monto}"  # Muestra el ID y el valor del monto
        return 'No monto asignado'
    
    get_monto_value.short_description = 'Monto (ID y Valor)'


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id','cantidad_venta', 'entrega','date','descripcion')
    search_fields = ('cantidad_venta',)
    ordering = ('cantidad_venta',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name','descriptions', )
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ueb']
    search_fields = ['name']
    list_filter = ['ueb']

@admin.register(EntregaEfectivo)
class EntregaEfectivoAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'p_entrega', 'p_recibe', 'efectivo', 'unidad']
    search_fields = ['efectivo', 'p_entrega__name', 'p_recibe__name']
    list_filter = ['unidad', 'date']

@admin.register(CantidadVenta)
class CantidadVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'efectivo', 'entrega_efectivo', 'unidad']
    search_fields = ['name', 'efectivo']
    list_filter = ['unidad', 'entrega_efectivo']





   

