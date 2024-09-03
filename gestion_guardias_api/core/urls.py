from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, GuardiaViewSet, DisponibilidadViewSet, NotificacionViewSet, EstadisticaViewSet, asignar_guardias_view, obtener_estadisticas

# Configuración del router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'guardias', GuardiaViewSet)
router.register(r'disponibilidades', DisponibilidadViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'estadisticas', EstadisticaViewSet)

# Definición de las rutas de la aplicación
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas registradas por el router
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Ruta para obtener el token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Ruta para refrescar el token JWT
    path('asignar_guardias/', asignar_guardias_view, name='asignar_guardias'),  # Ruta para la asignación de guardias
    path('api/estadisticas/', obtener_estadisticas, name='obtener_estadisticas'),  # Ruta para obtener estadísticas de guardias
    path('api/disponibilidades/eliminar_por_fecha/', DisponibilidadViewSet.as_view({'delete': 'eliminar_por_fecha'}), name='eliminar_por_fecha')
]
