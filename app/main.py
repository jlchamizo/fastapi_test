from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth, weather
from .database import engine, get_db
import requests
from typing import List
from datetime import timedelta
from fastapi.openapi.utils import get_openapi

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Tareas y Clima",
    description="Esta API proporciona endpoints para gestionar tareas y obtener información del clima.",
    version="1.0.0",
    terms_of_service="http://ejemplo.com/terms/",
    contact={
        "name": "Tu Nombre",
        "url": "http://ejemplo.com/contact/",
        "email": "tu@email.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Tareas y Clima",
        version="1.0.0",
        description="Esta API proporciona endpoints para gestionar tareas y obtener información del clima.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    #print ("chamizooooooooooooooooooooooooooooooooooooo")
    #print (user)
    #print (user.username)
    #print (user.password)
    db_user = crud.get_user_by_username(db, username=user.username)
    #print (db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/protected-route/")
async def protected_route(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    
    # Obtener el país a partir de la dirección IP
    response = requests.get(f'https://ipapi.co/{ip_address}/json/')
    #print (response)
    data = response.json()
    country = data.get('country_name', 'Desconocido')
    city = data.get('city', 'Desconocido')
    #print (country, city)

    #city = "Havana"
    
    # Obtener información del clima
    weather_info = weather.get_weather(city)
    
    if weather_info:
        # Almacenar información de la llamada a la API
        api_call = schemas.APICallCreate(
            ip_address=ip_address,
            country=country,
            weather_state=weather_info['weather_state'],
            temperature=weather_info['temperature']
        )
        crud.create_api_call(db, api_call)
        
        return {
            "message": "Esta es una ruta protegida",
            "ip_address": ip_address,
            "country": country,
            "weather": weather_info
        }
    else:
        raise HTTPException(status_code=500, detail="No se pudo obtener la información del clima")

# Crear una nueva tarea
@app.post("/tasks", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    return crud.create_task(db=db, task=task, user_id=current_user.id)

# Obtener todas las tareas
@app.get("/tasks", response_model=List[schemas.Task])
async def get_all_tasks(
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    return crud.get_tasks(db=db, user_id=current_user.id)

# Obtener una tarea por ID
@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def get_task(
    task_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    task = crud.get_task(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

# Actualizar una tarea
@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    updated_task = crud.update_task(db=db, task_id=task_id, task_update=task_update, user_id=current_user.id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated_task
    

# Eliminar una tarea
@app.delete("/tasks/{task_id}", response_model=schemas.TaskDelete)
async def delete_task(
    task_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Obtener la dirección IP del cliente
    ip_address = requests.get('https://api.ipify.org').text
    #print (ip_address)
    saved = save_routes(db, ip_address)
    #print (saved)
    deleted = crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}

def save_routes(db, ip_address):
    print(f'API Call: {ip_address}')
    # Obtener el país a partir de la dirección IP
    response = requests.get(f'https://ipapi.co/{ip_address}/json/')
    #print (response)
    data = response.json()
    country = data.get('country_name', 'Desconocido')
    city = data.get('city', 'Desconocido')
    #print (country, city)

    #city = "Havana"
    
    # Obtener información del clima
    weather_info = weather.get_weather(city)
    
    if weather_info:
        # Almacenar información de la llamada a la API
        api_call = schemas.APICallCreate(
            ip_address=ip_address,
            country=country,
            weather_state=weather_info['weather_state'],
            temperature=weather_info['temperature']
        )
        crud.create_api_call(db, api_call)
        
        return {
            "message": "Esta es una ruta protegida",
            "ip_address": ip_address,
            "country": country,
            "weather": weather_info
        }
    else:
        raise HTTPException(status_code=500, detail="No se pudo obtener la información del clima")