from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .models import Guardia, Disponibilidad, Notificacion, Estadistica
from .serializers import UserSerializer, GuardiaSerializer, DisponibilidadSerializer, NotificacionSerializer, EstadisticaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.http import JsonResponse
from collections import defaultdict
import random

# Vista para el modelo User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        # Este endpoint devuelve los datos del usuario autenticado
        user_data = self.get_serializer(request.user).data
        user_data['is_superuser'] = request.user.is_superuser  # Añadir el campo is_superuser al JSON de respuesta
        return Response(user_data)

# Vista para el modelo Guardia
class GuardiaViewSet(viewsets.ModelViewSet):
    queryset = Guardia.objects.all()
    serializer_class = GuardiaSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    @action(detail=True, methods=['patch'], url_path='cambiar_fecha')
    def cambiar_fecha(self, request, pk=None):
        """
        Cambiar la fecha de una guardia.
        """
        guardia = self.get_object()
        nueva_fecha = request.data.get('fecha')

        if not nueva_fecha:
            return Response({'detail': 'Fecha es requerida.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar la fecha de la guardia
        guardia.fecha = nueva_fecha
        guardia.save()

        # Notificar a los usuarios afectados (opcional)
        Notificacion.objects.create(
            usuario=guardia.usuario,
            tipo='email',
            mensaje=f"Tu guardia ha sido movida al {nueva_fecha}.",
            estado='pendiente'
        )

        return Response({'detail': 'Guardia actualizada correctamente.'}, status=status.HTTP_200_OK)

# Vista para el modelo Disponibilidad
class DisponibilidadViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def create(self, request, *args, **kwargs):
        """
        Sobrescribir el método create para asegurar que una disponibilidad no se
        duplique para un usuario en una misma fecha.
        """
        usuario = request.user
        fecha = request.data.get('fecha')

        # Verificar si ya existe una disponibilidad para esta fecha y usuario
        if Disponibilidad.objects.filter(usuario=usuario, fecha=fecha).exists():
            return Response(
                {'detail': 'La disponibilidad ya está registrada para esta fecha.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Preparar los datos para crear la disponibilidad
        data = {
            'usuario': usuario.id,
            'fecha': fecha
        }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Filtrar las disponibilidades solo para el usuario autenticado.
        También permite filtrar por mes y año si se proporcionan en la URL.
        """
        usuario = self.request.user
        mes = self.request.query_params.get('mes')
        año = self.request.query_params.get('año')
        queryset = Disponibilidad.objects.filter(usuario=usuario)
        
        if mes and año:
            queryset = queryset.filter(fecha__year=año, fecha__month=mes)
        
        return queryset

    @action(detail=False, methods=['delete'], url_path='eliminar_por_fecha')
    def eliminar_por_fecha(self, request):
        usuario = request.user
        fecha = request.query_params.get('fecha')

        if not fecha:
            return Response({'detail': 'Fecha es requerida.'}, status=status.HTTP_400_BAD_REQUEST)

        # Eliminar la disponibilidad
        eliminadas, _ = Disponibilidad.objects.filter(usuario=usuario, fecha=fecha).delete()

        if eliminadas:
            return Response({'detail': 'Disponibilidad eliminada.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Disponibilidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

# Vista para el modelo Notificacion
class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_queryset(self):
        # Filtrar las notificaciones solo para el usuario autenticado
        usuario = self.request.user
        return Notificacion.objects.filter(usuario=usuario).order_by('-fecha_envio')

    @action(detail=True, methods=['patch'], url_path='marcar_leida')
    def marcar_leida(self, request, pk=None):
        # Marcar una notificación como leída
        notificacion = self.get_object()
        notificacion.estado = 'enviado'
        notificacion.save()
        return Response({'detail': 'Notificación marcada como leída.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='eliminar')
    def eliminar(self, request, pk=None):
        # Eliminar una notificación
        notificacion = self.get_object()
        notificacion.delete()
        return Response({'detail': 'Notificación eliminada.'}, status=status.HTTP_204_NO_CONTENT)


# Vista para el modelo Estadistica
class EstadisticaViewSet(viewsets.ModelViewSet):
    queryset = Estadistica.objects.all()
    serializer_class = EstadisticaSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

# Función para asignar guardias
def asignar_guardias(start_date_str, end_date_str):
    # Convertir las fechas de string a datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    # Obtener todos los médicos, incluyendo al administrador
    medicos = list(User.objects.all())  # Incluye a todos los usuarios, incluyendo al administrador
    
    # Diccionario para llevar la cuenta del número de guardias por día de la semana para cada médico
    guardias_por_dia = defaultdict(lambda: defaultdict(int))
    
    # Obtener las estadísticas existentes
    estadisticas = Estadistica.objects.all()
    
    for estadistica in estadisticas:
        guardias_por_dia[estadistica.usuario.id] = {
            0: estadistica.guardias_lunes,
            1: estadistica.guardias_martes,
            2: estadistica.guardias_miercoles,
            3: estadistica.guardias_jueves,
            4: estadistica.guardias_viernes,
            5: estadistica.guardias_sabado,
            6: estadistica.guardias_domingo
        }
    
    # Diccionario para llevar la cuenta del último día que se asignó guardia a cada médico
    ultimo_dia_guardia = {medico.id: None for medico in medicos}
    
    delta = timedelta(days=1)
    
    while start_date <= end_date:
        medicos_disponibles = [
            medico for medico in medicos 
            if not Disponibilidad.objects.filter(usuario=medico, fecha=start_date).exists()
        ]
        
        # Ordenar médicos por la menor cantidad de guardias en el día específico de la semana
        random.shuffle(medicos_disponibles)  # Para romper empates aleatoriamente
        medicos_disponibles.sort(key=lambda medico: guardias_por_dia[medico.id][start_date.weekday()])
        
        for medico in medicos_disponibles:
            if ultimo_dia_guardia[medico.id] is None or (start_date - ultimo_dia_guardia[medico.id]).days > 1:
                # Asignar guardia
                Guardia.objects.create(usuario=medico, fecha=start_date, hora_inicio='15:00', hora_fin='09:00')
                
                # Obtener o crear la estadística
                estadistica, created = Estadistica.objects.get_or_create(usuario=medico)
                estadistica.total_guardias += 1
                if start_date.weekday() == 0:
                    estadistica.guardias_lunes += 1
                elif start_date.weekday() == 1:
                    estadistica.guardias_martes += 1
                elif start_date.weekday() == 2:
                    estadistica.guardias_miercoles += 1
                elif start_date.weekday() == 3:
                    estadistica.guardias_jueves += 1
                elif start_date.weekday() == 4:
                    estadistica.guardias_viernes += 1
                elif start_date.weekday() == 5:
                    estadistica.guardias_sabado += 1
                elif start_date.weekday() == 6:
                    estadistica.guardias_domingo += 1
                estadistica.save()
                
                # Crear notificación
                Notificacion.objects.create(
                    usuario=medico,
                    tipo='email',
                    mensaje=f"Se te ha asignado una guardia el {start_date.strftime('%Y-%m-%d')}.",
                    estado='pendiente'
                )
                
                guardias_por_dia[medico.id][start_date.weekday()] += 1
                ultimo_dia_guardia[medico.id] = start_date
                break  # Asignar una guardia por día
                
        start_date += delta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def asignar_guardias_view(request):
    # Obtener las fechas desde los parámetros GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        return JsonResponse({'error': 'start_date y end_date son requeridos'}, status=400)
    
    asignar_guardias(start_date, end_date)
    return JsonResponse({'status': 'Guardias asignadas correctamente'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_estadisticas(request):
    usuario = request.user

    # Obtener todas las estadísticas acumuladas del usuario actual
    estadisticas = Estadistica.objects.filter(usuario=usuario)

    # Serializar los datos
    serializer = EstadisticaSerializer(estadisticas, many=True)
    return Response(serializer.data)

