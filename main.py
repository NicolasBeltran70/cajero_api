#importamos todas las clases y funciones de las otras carpetas
from db.user_db import UserInDB
from db.user_db import update_user, get_user

from db.transaction_db import TransactionInDB 
from db.transaction_db import save_transaction

from models.user_models import UserIn, UserOut 
from models.transaction_models import TransactionIn, TransactionOut

#importamos las librerias que vamos a usar
import datetime 
from fastapi import FastAPI 
from fastapi import HTTPException # retorna los errores con los codigos de status

api = FastAPI()#creamos la aplicacion -> RESTAPI

##################      funcionalidad        ################}

#funcionalidad de autenticacion

@api.post("/user/auth/")#decorador: la funcion se ejecutara cuando se use la siguiente URL
#funcion asyncrona, que se ejecuta en desorden(en el momento que se ejecute)
async def auth_user(user_in: UserIn):#funcion que usa un objeto usuario entrada(uss,pass)
    user_in_db = get_user(user_in.username)#creo una variable y la igualo con la busqueda del nombre del objeto ingresado
    if user_in_db == None: 
        raise HTTPException(status_code=404, detail="El usuario no existe")#raise lanza el error
    if user_in_db.password != user_in.password: 
        return {"Autenticado": False}
    return{"Autenticado": True}

#funcionalidad balance


@api.get("/user/balance/{username}")#ojo con el llamado del usuario en la url
async def get_balance(username: str): 
    user_in_db = get_user(username)#retorna el objeto llamado y lo guarda en una variable
    if user_in_db == None: 
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    #UserOut solo utiliza 2 atributos(user y balance)
    #el doble "**" mapea y toma los valores que necesita del diccionario
    #se usa el .dict() para que lo tome como diccionario y pueda mapear
    user_out = UserOut(**user_in_db.dict())
    return user_out

#funcionalidad transaccion


@api.put("/user/transaction/")
async def make_transaction(transaction_in: TransactionIn): #entra modelo transaccion
    
    user_in_db = get_user(transaction_in.username)#valida usuario
    
    if user_in_db == None: 
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    if user_in_db.balance < transaction_in.value:#valida el saldo con lo que se retirara
        raise HTTPException(status_code=400, detail="Sin fondos suficientes")
# ya todo validado

    user_in_db.balance = user_in_db.balance - transaction_in.value #resta la transaccion del saldo
    update_user(user_in_db)#actualiza la base de datos 

    #creamos el un objeto trnasaccionIN con el mapeo de la transaccion
    transaction_in_db = TransactionInDB(**transaction_in.dict(), 
                            actual_balance=user_in_db.balance)#guarda el balance del usuario en ese momento como un atributo suyo

    transaction_in_db = save_transaction(transaction_in_db)#guarda esa transaccionIN

    transaction_out = TransactionOut(**transaction_in_db.dict())#crea la TransaccionOUT con su mapeo
    return transaction_out#retorna el modelo de transaccion OUT
