from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Guardia, Disponibilidad, Notificacion, Estadistica

# Serializador para el modelo User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Añadido para manejar la contraseña

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Encriptar la contraseña
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Encriptar la nueva contraseña si se proporciona
        instance.save()
        return instance

# Serializador para el modelo Guardia
class GuardiaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Guardia
        fields = ['id', 'usuario', 'fecha', 'hora_inicio', 'hora_fin']

# Serializador para el modelo Disponibilidad
class DisponibilidadSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Permitir la asignación del usuario

    class Meta:
        model = Disponibilidad
        fields = ['id', 'usuario', 'fecha']

    def create(self, validated_data):
        # Asegurarse de que el usuario está presente
        usuario = validated_data.get('usuario')
        if not usuario:
            raise serializers.ValidationError("El usuario es obligatorio.")
        
        return Disponibilidad.objects.create(**validated_data)

# Serializador para el modelo Notificacion
class NotificacionSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Permitir la asignación del usuario

    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'tipo', 'mensaje', 'fecha_envio', 'estado']


# Serializador para el modelo Estadistica
class EstadisticaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Estadistica
        fields = ['id', 'usuario', 'total_guardias', 'guardias_lunes', 'guardias_martes', 
                  'guardias_miercoles', 'guardias_jueves', 'guardias_viernes', 
                  'guardias_sabado', 'guardias_domingo']
