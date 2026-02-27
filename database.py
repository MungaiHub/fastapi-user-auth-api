from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


MYSQL_USER ="root"
MYSQL_PASSWORD ="amos"
MYSQL_HOST ="localhost"
MYSQL_PORT ="3306"
MYSQL_DATABASE="fastapi_db"  


DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"  

## CONNECTION

engine = create_engine(DATABASE_URL)

##session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        #base class for our models
Base = declarative_base()
                       