from typing import Dict
from pydantic import BaseModel

#definicion del objeto usuario
#declaramos una clase

class UserInDB(BaseModel): #heredamos el Basemodel de pydantic
    #declaramos los atributos
    username: str
    password: str
    balance: int


#definimos la base de datos a la cual nos conectaremos
# en este caso en una base de datos ficticia

#creo un diccionario para la clase
#decimos que es un Dict(diccionario)
#con una llave=str
#con un valor=objeto(clase=UserinDB)
database_users = Dict[str, UserInDB]

database_users = {# lleno el diccionario y uso el "**" para mapear cada atributo
#recordemos que los diccionario tienen [llave:valor]
    "camilo24": UserInDB(**{"username": "camilo24", 
                            "password": "root", 
                            "balance": 12000}),
                            
    "andres18": UserInDB(**{"username": "andres18",
                            "password": "hola", 
                            "balance": 34000}), 
}

#declaramos las funciones con respecto a la clase
#funcion de llamado
def get_user(u_name: str): #la funcion depende de un str llamado = username
    if u_name in database_users.keys():#el ".keys()" llama todas las llaves del dicccionario
        return database_users[u_name]#retorna el objeto con ese valor
    else:
        return None

def update_user(user_in_db: UserInDB): #entra un objeto usuario
    #busca en el diccionario un objeto que tenga el mismos atributo nombre
    database_users[user_in_db.username] = user_in_db#iguala los objetos
    return user_in_db#retorna el objeto
