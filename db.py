"""
db.py
-----
Funzioni di utilità per la connessione al database e l'esecuzione
delle interrogazioni tramite SQLAlchemy.
Importato da tutte le pagine dell'applicazione.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, event, text

DB_PATH = Path(__file__).parent / "palestra.db"


DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def _enable_foreign_keys(dbapi_conn, _):
    """Abilita il controllo delle foreign key per ogni connessione SQLite."""
    dbapi_conn.execute("PRAGMA foreign_keys = ON;")


def run_query(query, params=None):
    """Esegue una SELECT e restituisce un pandas.DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params or {})


def run_action(query, params=None):
    """Esegue una INSERT/UPDATE/DELETE. Solleva l'eccezione in caso di errore."""
    with engine.begin() as conn:
        conn.execute(text(query), params or {})
