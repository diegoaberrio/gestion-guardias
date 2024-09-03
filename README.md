### Gestión de Guardias Médicas

**Gestión de Guardias Médicas** es una aplicación web diseñada para facilitar la gestión de guardias médicas en la Comunidad de Madrid. La aplicación permite la asignación automática de guardias de manera equitativa, la gestión de la disponibilidad de los médicos, la comunicación de asignaciones, y la visualización de estadísticas detalladas, todo a través de una interfaz gráfica moderna y responsiva.

## Funcionalidades Principales

1. **Sistema de Autenticación:**
   - Registro de usuarios (médicos) con correo electrónico y contraseña.
   - Inicio de sesión seguro y gestión de roles (médicos y administradores).

2. **Gestión de Guardias:**
   - Los médicos pueden marcar su disponibilidad en un calendario mensual.
   - Asignación automática de guardias basada en la disponibilidad, asegurando un equilibrio equitativo.
   - Interfaz de calendario mensual para visualizar y gestionar las guardias.

3. **Notificaciones:**
   - Notificaciones por correo electrónico y push para asignaciones de guardias y cambios.
   - Confirmaciones automáticas para cambios de guardias.

4. **Estadísticas:**
   - Visualización de estadísticas de las guardias realizadas, desglosadas por días de la semana.
   - Exportación de estadísticas a formatos PDF y Excel.

## Requerimientos del Sistema

- **Backend:** Python 3.x, Django, Django Rest Framework (DRF)
- **Base de Datos:** MySQL para el entorno de producción
- **Frontend:** Bootstrap o Tailwind CSS
- **Infraestructura:** Docker para contenedores, CI/CD para despliegue automatizado

## Estructura de la Base de Datos

**Usuarios:**
- `id_usuario`: Identificador único del usuario (INT, PK, AUTO_INCREMENT)
- `nombre`: Nombre del usuario (VARCHAR)
- `email`: Correo electrónico del usuario (VARCHAR, UNIQUE)
- `password`: Contraseña del usuario (VARCHAR)
- `rol`: Rol del usuario (ENUM: 'medico', 'admin')
- `fecha_creacion`: Fecha de creación de la cuenta (DATETIME)

**Disponibilidad:**
- `id_disponibilidad`: Identificador único de la disponibilidad (INT, PK, AUTO_INCREMENT)
- `id_usuario`: Referencia al usuario (INT, FK)
- `fecha`: Fecha de disponibilidad (DATE)

**Guardia:**
- `id_guardia`: Identificador único de la guardia (INT, PK, AUTO_INCREMENT)
- `id_usuario`: Referencia al usuario (INT, FK)
- `fecha`: Fecha de la guardia (DATE)
- `hora_inicio`: Hora de inicio de la guardia (TIME)
- `hora_fin`: Hora de finalización de la guardia (TIME)

**Cambio de Guardia:**
- `id_cambio`: Identificador único del cambio de guardia (INT, PK, AUTO_INCREMENT)
- `id_guardia_original`: Referencia a la guardia original (INT, FK)
- `id_guardia_solicitada`: Referencia a la guardia solicitada (INT, FK)
- `id_usuario_solicitante`: Referencia al usuario que solicita el cambio (INT, FK)
- `id_usuario_receptor`: Referencia al usuario receptor del cambio (INT, FK)
- `estado`: Estado del cambio (ENUM: 'pendiente', 'aprobado', 'rechazado')

**Notificación:**
- `id_notificacion`: Identificador único de la notificación (INT, PK, AUTO_INCREMENT)
- `id_usuario`: Referencia al usuario (INT, FK)
- `tipo`: Tipo de notificación (ENUM: 'email', 'push')
- `mensaje`: Mensaje de la notificación (TEXT)
- `fecha_envio`: Fecha de envío de la notificación (DATETIME)
- `estado`: Estado de la notificación (ENUM: 'enviado', 'pendiente')

**Estadísticas de Guardia:**
- `id_estadistica`: Identificador único de la estadística (INT, PK, AUTO_INCREMENT)
- `id_usuario`: Referencia al usuario (INT, FK)
- `total_guardias`: Total de guardias realizadas (INT)
- `guardias_lunes`: Guardias realizadas los lunes (INT)
- `guardias_martes`: Guardias realizadas los martes (INT)
- `guardias_miercoles`: Guardias realizadas los miércoles (INT)
- `guardias_jueves`: Guardias realizadas los jueves (INT)
- `guardias_viernes`: Guardias realizadas los viernes (INT)
- `guardias_sabado`: Guardias realizadas los sábados (INT)
- `guardias_domingo`: Guardias realizadas los domingos (INT)


## Instalación y Configuración

Para desplegar la aplicación de Gestión de Guardias Médicas localmente, sigue estos pasos:

1. **Clonar el Repositorio:**

   git clone https://github.com/diegoaberrio/gestion-guardias.git
  

2. **Navegar al Directorio del Proyecto:**
 
   cd gestion-guardias
 

3. **Configurar un Entorno Virtual (Opcional pero Recomendado):**
   - Crea un entorno virtual:
    
     python -m venv venv
   
   - Activa el entorno virtual:
     - En Windows:
       
       venv\Scripts\activate
      
     - En macOS/Linux:
      
       source venv/bin/activate
      

4. **Instalar las Dependencias:**
  
   pip install -r requirements.txt
  

5. **Configurar la Base de Datos:**
   - Configura la base de datos en el archivo `settings.py` de Django.
   - Ejecuta las migraciones para crear las tablas necesarias:
   
     python manage.py migrate
   

6. **Cargar Datos Iniciales (si es necesario):**
   - Si tienes un archivo para cargar datos iniciales (fixture), puedes hacerlo con:
    
     python manage.py loaddata nombre_del_archivo.json
    

7. **Iniciar el Servidor:**
   
   python manage.py runserver
 

8. **Acceder a la Aplicación:**
   - Abre tu navegador y accede a `http://localhost:8000` para comenzar a usar la aplicación de Gestión de Guardias Médicas.

## Demo en YouTube

Para ver una demostración de la aplicación en acción, visita [este video en YouTube](https://www.youtube.com/watch?v=Z8TDsfNoKlI).

## Mi Sitio Web Personal

Puedes explorar más sobre mi trabajo y otros proyectos en mi [página web personal](https://diegoincode-dc1cd734cb90.herokuapp.com/).

## Contacto

- **Correo electrónico:** diegoaberrio@hotmail.com
- **LinkedIn:** [Diego Alonso Berrío Gómez](https://www.linkedin.com/in/diego-alonso-berrío-gómez)
- **GitHub:** [Diego Aberrio](https://github.com/diegoaberrio)

