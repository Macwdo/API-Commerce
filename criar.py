import sqlalchemy
from configs.database import metadata , DATABASE_URL
import modelos.Produtos
import modelos.Usuarios


def config(databaseurl=DATABASE_URL):
    engine = sqlalchemy.create_engine(databaseurl)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    
if __name__ == "__main__":
    config()