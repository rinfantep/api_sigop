from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, permissions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Province, Municipality, Subsidiary, Office, Worker, CustomUser, Entrega, Devolucion, Inversion, Role, Venta, Unidad, EntregaEfectivo, CantidadVenta
from .serializers import (MunicipalitySerializer, MunicipalityProvinceSerializer, 
                           ProvinceSerializer, SubsidiarySerializer, SubsidiaryListSerializer, 
                            OfficeSerializer, WorkerSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, EntregaSerializer, DevolucionSerializer, InversionSerializer, RoleSerializer, VentaSerializer, UnidadSerializer, EntregaEfectivoSerializer, CantidadVentaSerializer)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from datetime import datetime, timedelta
from calendar import monthrange
from django.db.models import Q

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Usa el serializer personalizado para validar y obtener datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Llama al método `post` de la vista base para obtener los tokens
        response = super().post(request, *args, **kwargs)

        # Agrega datos personalizados a la respuesta
        if response.status_code == status.HTTP_200_OK:
            response_data = response.data.copy()  # Copia la respuesta para modificarla
            response_data['message'] = 'Inicio de sesión exitoso'
            response_data['status'] = status.HTTP_200_OK
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = response.data.copy()  # Copia la respuesta para modificarla
            response_data['message'] = 'Credenciales de inicio de sesión incorrectas'
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # Uncomment this if you want to enforce authentication and permissions globally
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure only admin can create users
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only admin users can create new users.")
        serializer.save()

    def get_queryset(self):
        # Optionally, filter users based on request user permissions
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"detail": "Contraseña cambiada con éxito."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all().order_by('name')
    serializer_class = ProvinceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all().order_by('name')
    serializer_class = MunicipalitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SubsidiaryViewSet(viewsets.ModelViewSet):
    queryset = Subsidiary.objects.all().order_by('name')
    serializer_class = SubsidiarySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SubsidiaryListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subsidiary.objects.all().order_by('name')
    serializer_class = SubsidiaryListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

###Modulo Presupuesto###
class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

    
class InversionViewSet(viewsets.ModelViewSet):
    queryset = Inversion.objects.all()
    serializer_class = InversionSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class DevolucionViewSet(viewsets.ModelViewSet):
    queryset = Devolucion.objects.all()
    serializer_class = DevolucionSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]


###***Role***###
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

###***Role***###
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

###***Modulo Por concepto de Ventas***###
class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class EntregaEfectivoViewSet(viewsets.ModelViewSet):
    queryset = EntregaEfectivo.objects.all()
    serializer_class = EntregaEfectivoSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class CantidadVentaViewSet(viewsets.ModelViewSet):
    queryset = CantidadVenta.objects.all()
    serializer_class = CantidadVentaSerializer
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]


###***Reportes***###

###***UEB***###
class EntregaReporteView(APIView):
    def get(self, request):
        subsidiaries = Subsidiary.objects.all()

        report_data = []
        for subsidiary in subsidiaries:
            # Total efectivo entregado
            total_entregado = Entrega.objects.filter(ueb=subsidiary).aggregate(Sum('monto'))['monto__sum'] or 0
            
            # Total efectivo invertido
            total_invertido = Devolucion.objects.filter(monto__ueb=subsidiary).aggregate(Sum('monto_invertido'))['monto_invertido__sum'] or 0
            
            # Total efectivo no invertido
            total_no_invertido = Devolucion.objects.filter(monto__ueb=subsidiary).aggregate(Sum('monto_no_invertido'))['monto_no_invertido__sum'] or 0
            
            # Total ventas
            total_ventas = Devolucion.objects.filter(monto__ueb=subsidiary).aggregate(Sum('monto_venta'))['monto_venta__sum'] or 0
            
            # Total ganancia
            total_ganancias = Devolucion.objects.filter(monto__ueb=subsidiary).aggregate(Sum('ganancia'))['ganancia__sum'] or 0

            report_data.append({
                'subsidiary': subsidiary.name,
                'total_entregado': total_entregado,
                'total_invertido': total_invertido,
                'total_no_invertido': total_no_invertido,
                'total_ventas': total_ventas,
                'total_ganancias': total_ganancias,
            })

        return Response(report_data)

###***Base Productiva***###
class ReporteBasePView(APIView):
    def get(self, request):
        offices = Office.objects.all()

        report_data = []
        for office in offices:
            # Total efectivo entregado
            total_entregado = Entrega.objects.filter(office=office).aggregate(Sum('monto'))['monto__sum'] or 0
            
            # Total efectivo invertido
            total_invertido = Devolucion.objects.filter(monto__office=office).aggregate(Sum('monto_invertido'))['monto_invertido__sum'] or 0
            
            # Total efectivo no invertido
            total_no_invertido = Devolucion.objects.filter(monto__office=office).aggregate(Sum('monto_no_invertido'))['monto_no_invertido__sum'] or 0
            
            # Total ventas
            total_ventas = Devolucion.objects.filter(monto__office=office).aggregate(Sum('monto_venta'))['monto_venta__sum'] or 0
            
            # Total ganancia
            total_ganancias = Devolucion.objects.filter(monto__office=office).aggregate(Sum('ganancia'))['ganancia__sum'] or 0

            report_data.append({
                'office': office.name,
                'total_entregado': total_entregado,
                'total_invertido': total_invertido,
                'total_no_invertido': total_no_invertido,
                'total_ventas': total_ventas,
                'total_ganancias': total_ganancias,
            })

        return Response(report_data)



###Semanal###
class ReporteSemanalBasePView(APIView):

    def get(self, request):
        now = datetime.now()
        year = now.year
        month = now.month

        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = datetime(year, month, monthrange(year, month)[1])

        days_in_month = (last_day_of_month - first_day_of_month).days + 1
        days_per_week = days_in_month // 4
        extra_days = days_in_month % 4

        weeks = []
        start_day = first_day_of_month
        for i in range(4):
            end_day = start_day + timedelta(days=days_per_week + (1 if i < extra_days else 0) - 1)
            weeks.append({
                'name': f'Semana {i + 1}',
                'start_date': start_day,
                'end_date': end_day
            })
            start_day = end_day + timedelta(days=1)

        # Obtener todas las offices
        offices = Office.objects.all()

        # Recopilar datos organizados por office y por semana
        report_data = []

        for office in offices:
            office_data = {
                'office': office.name,
                'semanas': []
            }

            for week in weeks:
                # Obtener las entregas de esta office para la semana actual
                entregas_semana = (
                    Entrega.objects
                    .filter(date__range=(week['start_date'], week['end_date']), office=office)
                    .aggregate(total_entregado=Sum('monto'))['total_entregado'] or 0
                )

                # Obtener el total invertido para esta office y semana
                total_invertido = (
                    Devolucion.objects
                    .filter(monto__office=office, monto__date__range=(week['start_date'], week['end_date']))
                    .aggregate(Sum('monto_invertido'))['monto_invertido__sum'] or 0
                )

                # Obtener devoluciones asociadas a esta office y semana
                devolucion_data = (
                    Devolucion.objects
                    .filter(monto__office=office, date__range=(week['start_date'], week['end_date']))
                    .aggregate(total_no_invertido=Sum('monto_no_invertido'),
                               total_venta=Sum('monto_venta'),
                               total_ganancia=Sum('ganancia'))
                )

                total_no_invertido = devolucion_data['total_no_invertido'] or 0
                total_venta = devolucion_data['total_venta'] or 0
                total_ganancia = devolucion_data['total_ganancia'] or 0

                # Agregar los datos de la semana a la office
                office_data['semanas'].append({
                    'week': week['name'],
                    'start_date': week['start_date'].strftime('%Y-%m-%d'),
                    'end_date': week['end_date'].strftime('%Y-%m-%d'),
                    'total_entregado': entregas_semana,
                    'total_invertido': total_invertido,
                    'total_no_invertido': total_no_invertido,
                    'total_venta': total_venta,
                    'total_ganancia': total_ganancia,
                })

            report_data.append(office_data)

        return Response(report_data)






        













