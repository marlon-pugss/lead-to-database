import os

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base


db_debug_enabled = int(os.environ.get("DATABASE_DEBUG", "0"))
db_connection = os.getenv(
    "DATABASE_URL",
    "sqlite:///leads.db",  # Usar SQLite para testes
)

Base = declarative_base()
BaseAudit = declarative_base()

if db_connection.startswith("sqlite"):
    # Para SQLite, não usar isolation_level
    engine = db.create_engine(
        db_connection,
        echo=bool(db_debug_enabled),
    )
else:
    # Para PostgreSQL e outros bancos
    try:
        engine = db.create_engine(
            db_connection,
            isolation_level="READ COMMITTED",
            echo=bool(db_debug_enabled),
        )
    except Exception:
        # Fallback para SQLite se PostgreSQL não estiver disponível
        engine = db.create_engine(
            "sqlite:///leads.db",
            echo=bool(db_debug_enabled),
        )

session = sessionmaker(bind=engine, expire_on_commit=False)