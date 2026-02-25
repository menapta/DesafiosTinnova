from fastapi import APIRouter, Depends, HTTPException, status

from ..HeaderSecurity import getAuthData, adminAuthData    

router = APIRouter()


@router.get("/dashboard-geral")
def freeRoute(data: dict = Depends(getAuthData)):
    return {"msg": f"Olá {data['user']}, você tem acesso básico."}

@router.get("/dashboard-admin")
def exclusiveRoute(data: dict = Depends(adminAuthData)):
    return {"msg": "Acesso concedido. Usuário Admin."}