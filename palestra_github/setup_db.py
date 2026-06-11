"""
setup_db.py
-----------
Crea (o ricrea) il database SQLite `palestra.db` con le tabelle
CORSO, ISTRUTTORE e PROGRAMMA e lo popola con dati di esempio.

Eseguire UNA VOLTA prima di avviare l'app:
    python setup_db.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "palestra.db"


def crea_database():
    # Ricreo il file da zero a ogni esecuzione
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Abilito il controllo delle foreign key
    cur.execute("PRAGMA foreign_keys = ON;")

    # ---------- SCHEMA ----------
    cur.executescript(
        """
        CREATE TABLE CORSO (
            CodC    TEXT PRIMARY KEY,      -- es. "CT001"
            Nome    TEXT NOT NULL,
            Tipo    TEXT NOT NULL,
            Livello INTEGER NOT NULL CHECK (Livello BETWEEN 1 AND 4)
        );

        CREATE TABLE ISTRUTTORE (
            CodFisc     TEXT PRIMARY KEY,
            Nome        TEXT NOT NULL,
            Cognome     TEXT NOT NULL,
            Email       TEXT NOT NULL,
            DataNascita TEXT NOT NULL      -- formato 'YYYY-MM-DD'
        );

        CREATE TABLE PROGRAMMA (
            CodFisc      TEXT NOT NULL,
            Giorno       TEXT NOT NULL,
            OrarioInizio TEXT NOT NULL,    -- formato 'HH:MM'
            Durata       INTEGER NOT NULL, -- minuti
            CodC         TEXT NOT NULL,
            Sala         TEXT NOT NULL,
            PRIMARY KEY (CodFisc, Giorno, OrarioInizio),
            FOREIGN KEY (CodFisc) REFERENCES ISTRUTTORE(CodFisc),
            FOREIGN KEY (CodC)    REFERENCES CORSO(CodC)
        );
        """
    )

    # ---------- DATI: CORSO ----------
    corsi = [
        ("CT001", "Hatha Yoga",          "Yoga",       1),
        ("CT002", "Vinyasa Flow",        "Yoga",       3),
        ("CT003", "Spinning Base",       "Spinning",   2),
        ("CT004", "Spinning Advanced",   "Spinning",   4),
        ("CT005", "Pilates Matwork",     "Pilates",    1),
        ("CT006", "Pilates Reformer",    "Pilates",    3),
        ("CT007", "Zumba Fitness",       "Zumba",      2),
        ("CT008", "CrossFit WOD",        "CrossFit",   4),
        ("CT009", "Functional Training", "Functional", 2),
        ("CT010", "Total Body",          "Functional", 3),
    ]
    cur.executemany("INSERT INTO CORSO VALUES (?,?,?,?)", corsi)

    # ---------- DATI: ISTRUTTORE ----------
    istruttori = [
        ("RSSMRA85M01H501Z", "Mario",    "Rossi",   "mario.rossi@palestra.it",     "1985-08-01"),
        ("BNCLRA90A41F205X", "Laura",    "Bianchi", "laura.bianchi@palestra.it",   "1990-01-01"),
        ("VRDGPP78D12L219K", "Giuseppe", "Verdi",   "giuseppe.verdi@palestra.it",  "1978-04-12"),
        ("FRRNNA92T55G273Q", "Anna",     "Ferrari", "anna.ferrari@palestra.it",    "1992-12-15"),
        ("GLLLCA88E03H501W", "Luca",     "Gallo",   "luca.gallo@palestra.it",      "1988-05-03"),
        ("MRTSFN95H62L736J", "Stefania", "Marino",  "stefania.marino@palestra.it", "1995-06-22"),
    ]
    cur.executemany("INSERT INTO ISTRUTTORE VALUES (?,?,?,?,?)", istruttori)

    # ---------- DATI: PROGRAMMA ----------
    programma = [
        ("RSSMRA85M01H501Z", "Lunedì",    "09:00", 60, "CT001", "Sala A"),
        ("RSSMRA85M01H501Z", "Martedì",   "09:00", 60, "CT001", "Sala A"),
        ("RSSMRA85M01H501Z", "Mercoledì", "18:00", 60, "CT002", "Sala A"),
        ("BNCLRA90A41F205X", "Lunedì",    "10:00", 45, "CT005", "Sala B"),
        ("BNCLRA90A41F205X", "Mercoledì", "10:00", 45, "CT005", "Sala B"),
        ("BNCLRA90A41F205X", "Giovedì",   "17:00", 60, "CT006", "Sala B"),
        ("VRDGPP78D12L219K", "Martedì",   "19:00", 45, "CT003", "Sala Spinning"),
        ("VRDGPP78D12L219K", "Venerdì",   "18:00", 60, "CT004", "Sala Spinning"),
        ("FRRNNA92T55G273Q", "Mercoledì", "20:00", 60, "CT007", "Sala A"),
        ("FRRNNA92T55G273Q", "Venerdì",   "19:00", 45, "CT007", "Sala A"),
        ("GLLLCA88E03H501W", "Lunedì",    "18:00", 60, "CT008", "Sala CrossFit"),
        ("GLLLCA88E03H501W", "Giovedì",   "19:00", 50, "CT009", "Sala A"),
        ("MRTSFN95H62L736J", "Martedì",   "10:00", 60, "CT010", "Sala B"),
        ("MRTSFN95H62L736J", "Venerdì",   "09:00", 45, "CT005", "Sala B"),
    ]
    cur.executemany("INSERT INTO PROGRAMMA VALUES (?,?,?,?,?,?)", programma)

    conn.commit()
    conn.close()
    print(f"Database creato correttamente in: {DB_PATH}")
    print(f"  CORSO:      {len(corsi)} righe")
    print(f"  ISTRUTTORE: {len(istruttori)} righe")
    print(f"  PROGRAMMA:  {len(programma)} righe")


if __name__ == "__main__":
    crea_database()
