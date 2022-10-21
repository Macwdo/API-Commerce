import sqlalchemy
from configs.database import metadata , DATABASE_URL
from models.usuarios import Usuario

def config(databaseurl=DATABASE_URL):
    engine = sqlalchemy.create_engine(databaseurl)
    metadata.drop_all(engine)
    metadata.create_all(engine)

    
if __name__ == "__main__":
    config()