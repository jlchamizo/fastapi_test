# API del Clima y Tareas con FastAPI

Este proyecto es una API basada en FastAPI que implementa autenticación OAuth2, registra llamadas a la API con información de dirección IP y obtiene datos del clima para la ubicación del llamante. Además, ahora incluye funcionalidades para gestionar tareas.

## Características

- Autenticación OAuth2
- Registro e inicio de sesión de usuarios
- Rutas protegidas
- Registro automático de llamadas a la API con dirección IP, país e información del clima
- Integración con base de datos PostgreSQL
- Soporte Docker para pruebas locales fáciles
- Gestión de tareas (CRUD)

## Prerrequisitos

- Docker y Docker Compose
- Clave de API de OpenWeatherMap

## Configuración

1. Clona el repositorio:
   ```
   git clone https://github.com/jlchamizo/fastapi_test.git
   cd fastapi_test
   ```

2. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```
   DATABASE_URL=postgresql://user:password@db:5432/fastapi_db
   SECRET_KEY=tu_clave_secreta
   WEATHER_API_KEY=tu_clave_api_openweathermap
   ```

   Reemplaza `tu_clave_secreta` con una cadena aleatoria segura y `tu_clave_api_openweathermap` con tu clave de API de OpenWeatherMap real.

3. Construye y ejecuta los contenedores Docker:
   ```
   docker-compose up --build
   ```

4. La API estará disponible en `http://localhost:8000`.

## Documentación de la API

### Endpoints

#### Autenticación y Usuarios

- POST /token - Obtener token de acceso
- POST /users/ - Crear un nuevo usuario
- GET /users/me/ - Obtener información del usuario actual

#### Ruta Protegida de Ejemplo

- GET /protected-route/ - Ejemplo de ruta protegida

#### Gestión de Tareas

- POST /tasks - Crear una nueva tarea
- GET /tasks - Obtener todas las tareas del usuario
- GET /tasks/{task_id} - Obtener una tarea específica
- PUT /tasks/{task_id} - Actualizar una tarea
- DELETE /tasks/{task_id} - Eliminar una tarea

### Autenticación

Esta API utiliza OAuth2 con tokens Bearer para la autenticación. Para acceder a las rutas protegidas, necesitas incluir un encabezado `Authorization` con un token de acceso válido:

```
Authorization: Bearer <token_de_acceso>
```

### Ejemplos de Uso

1. Crear un nuevo usuario:
   ```
   curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username": "usuario_prueba", "password": "contraseña_prueba"}'
   ```

2. Obtener un token de acceso:
   ```
   curl -X POST "http://localhost:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=usuario_prueba&password=contraseña_prueba"
   ```

3. Acceder a una ruta protegida:
   ```
   curl -X GET "http://localhost:8000/protected-route/" -H "Authorization: Bearer <token_de_acceso>"
   ```

4. Crear una nueva tarea:
   ```
   curl -X POST "http://localhost:8000/tasks" -H "Authorization: Bearer <token_de_acceso>" -H "Content-Type: application/json" -d '{"task_name": "Mi primera tarea", "description": "Descripción de la tarea"}'
   ```

5. Obtener todas las tareas:
   ```
   curl -X GET "http://localhost:8000/tasks" -H "Authorization: Bearer <token_de_acceso>"
   ```

6. Obtener una tarea específica:
   ```
   curl -X GET "http://localhost:8000/tasks/1" -H "Authorization: Bearer <token_de_acceso>"
   ```

7. Actualizar una tarea:
   ```
   curl -X PUT "http://localhost:8000/tasks/1" -H "Authorization: Bearer <token_de_acceso>" -H "Content-Type: application/json" -d '{"task_name": "Tarea actualizada", "description": "Nueva descripción", "status": "completada"}'
   ```

8. Eliminar una tarea:
   ```
   curl -X DELETE "http://localhost:8000/tasks/1" -H "Authorization: Bearer <token_de_acceso>"
   ```


