from django.urls import path, include
from rest_framework import routers
#from rest_framework.documentation import include_docs_urls
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import CustomTokenObtainPairView, EntregaReporteView, ReporteBasePView,ReporteSemanalBasePView

router = routers.DefaultRouter()
router.register(r'province', views.ProvinceViewSet, basename='province')
router.register(r'municipality', views.MunicipalityViewSet, basename='municipality')
router.register(r'subsidiary', views.SubsidiaryViewSet, basename='subsidiary')
router.register(r'subsidiary-list', views.SubsidiaryListViewSet, basename='subsidiary-list')
router.register(r'office', views.OfficeViewSet, basename='office')

router.register(r'worker', views.WorkerViewSet, basename='worker')
router.register(r'users', views.CustomUserViewSet, basename='users')
router.register(r'entrega', views.EntregaViewSet, basename='entrega')
router.register(r'devolucion', views.DevolucionViewSet, basename='devolucion')
router.register(r'inversion', views.InversionViewSet, basename='inversion')
router.register(r'role', views.RoleViewSet, basename='role')
router.register(r'venta', views.VentaViewSet, basename='venta')
router.register(r'unidad', views.UnidadViewSet, basename='unidad')
router.register(r'entregaefectivo', views.EntregaEfectivoViewSet, basename='entrega_efectivo')
router.register(r'cantidadventa', views.CantidadVentaViewSet, basename='cantidad_venta')

# Definición de las rutas
urlpatterns = [
    path("", include(router.urls)), 
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reporte/entregas/', EntregaReporteView.as_view(), name='reporte_entregas'),
    path('reporte/baseproductiva/', ReporteBasePView.as_view(), name='reporte_baseproductiva'),
    path('reporte/semanalbaseproductiva/', ReporteSemanalBasePView.as_view(), name='reporte_semanalbaseproductiva'),
   


]
