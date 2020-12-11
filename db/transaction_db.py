from datetime import datetime
from pydantic import BaseModel
class TransactionInDB(BaseModel): 
    id_transaction: int = 0
    username: str
    date: datetime = datetime.now()#objeto datetime
    value: int
    actual_balance: int

#creamos la base de datos de transacciones
database_transactions = []#la declaramos como lista vacia
generator = {"id": 0}#creamos un diccionario "generador" como contador

#funcion save
def save_transaction(transaction_in_db: TransactionInDB):#entra el objeto transaction
    generator["id"] = generator["id"]+1#sirbe como auto-increment
    transaction_in_db.id_transaction = generator["id"]#asigna el primer atributo segun el dicciionario
    database_transactions.append(transaction_in_db)#agregamos cada transaccion a la lista
    return transaction_in_db
