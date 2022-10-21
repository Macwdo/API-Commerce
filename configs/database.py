import databases
import sqlalchemy

SECRET_KEY = "secret"
DATABASE_URL = "sqlite:///alunos.sqlite"
database = databases.Database(DATABASE_URL,force_rollback=False)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.drop_all(engine)
metadata.create_all(engine)