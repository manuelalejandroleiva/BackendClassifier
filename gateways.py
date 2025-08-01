from fastapi import Depends, FastAPI, Request, Header,Body,APIRouter

import httpx


from usuarios.connection.database import get_db

from usuarios.DTO.dto import LoginRequest  # Asegúrate de que DTO/model.py esté en el mismo directorio o ajusta la ruta
# from usuarios.connection.database import SessionLocal, engine, Base,get_db
from sqlalchemy.ext.asyncio import AsyncSession
from usuarios.dependencies.dependencies import get_current_user
from typing import Optional
import os
from fastapi import HTTPException



from usuarios.schema import *


# 🔐 Router protegido
protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


app = FastAPI()
USER_SERVICE_URL = "http://localhost:8001"
USER_SERVICE_PATH="http://localhost:8001"




@app.post("/login")
async def login( 
    login_data: LoginRequest = Body(...),
   
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SERVICE_URL}/login",
            json=login_data.dict()
        )
    return response.json()




def get_token(authorization: Optional[str] = Header(None, include_in_schema=False)):
    return authorization

@protected_router.get("/users/{user_id}")
async def get_user(
    user_id: int,
   authorization: Optional[str] = Depends(get_token)
):  
    headers = {"Authorization": authorization} if authorization else {}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_PATH}/users/{user_id}", headers=headers)
    return response.json()


@protected_router.post("/users/create")
async def create_user(
    data: UserCreate = Body(...),
   
    authorization: Optional[str] = Depends(get_token)
):
    headers = {"Authorization": authorization} if authorization else {}
    async with httpx.AsyncClient() as client:

       response = await client.post(f"{USER_SERVICE_PATH}/users/", json=data.dict(), headers=headers)

    return response.json()




@protected_router.delete('/users/{user_id}', response_model=UserSchema)
async def delete_user(
    user_id: int,
    authorization: Optional[str] = Depends(get_token)
):
    headers = {"Authorization": authorization} if authorization else {}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SERVICE_PATH}/users/{user_id}", headers=headers)

        # Si el servicio retorna un error
        if response.status_code >= 400:
            error_data = response.json()
            raise HTTPException(status_code=response.status_code, detail=error_data.get("detail", "Error al eliminar usuario"))

        return response.json()
    

@protected_router.put('/users/{user_id}')
async def updateUsers(
    user: UserSchema,
      user_id: int,
        authorization: Optional[str] = Depends(get_token)):
    headers = {"Authorization": authorization} if authorization else {}
    async with httpx.AsyncClient() as client:
        response= await client.put(f"{USER_SERVICE_PATH}/users/{user_id}", json=user.dict() ,headers=headers)
        # Si el servicio retorna un error
        if response.status_code >= 400:
            error_data = response.json()
            raise HTTPException(status_code=response.status_code, detail=error_data.get("detail", "Error al actualizar el  usuario"))

        return response.json()

    




app.include_router(protected_router,prefix="/api")

    
    




