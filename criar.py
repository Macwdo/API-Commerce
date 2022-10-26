import sqlalchemy
from configs.database import metadata , DATABASE_URL
from models.usuarios import Usuario
from models.produtos import Produto
from models.pedidos import Pedido

def config(databaseurl=DATABASE_URL):
    engine = sqlalchemy.create_engine(databaseurl)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    
if __name__ == "__main__":
    config()