import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.sql import text

db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "33306")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "Password123*")
db_name = os.getenv("DB_NAME", "quotes")

# DB URL format: dialect+driver://username:password@host:port/database
admin_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/"
sql_url = f"{admin_url}{db_name}"
engine = create_engine(sql_url, echo=True)

def create_database_if_not_exists():
    """Create the database if it does not exist."""
 
    admin_engine = sa_create_engine(admin_url)
    
    try:
        with admin_engine.connect() as conn:
            # Crear la base de datos si no existe
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            conn.commit()
            print(f"✅ Database '{db_name}' created or already exists")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        raise e
    finally:
        admin_engine.dispose()

def create_db_and_tables():
    """Create the database and tables if they do not exist."""
    create_database_if_not_exists()
    SQLModel.metadata.create_all(engine)