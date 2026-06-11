# 🏋️ Gym Manager — Streamlit + SQLite Web App

A multi-page web application built with **Python**, **Streamlit**, and **SQLite** for managing a gym's courses, instructors, and weekly schedule.

Developed as a university project for the *Databases* course at Politecnico di Torino.

---

## 📸 Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Dashboard with charts: lessons by time slot and by weekday |
| 📚 **Courses** | Browse and filter courses by type and difficulty level |
| 🧑‍🏫 **Instructors** | Search instructors by surname and date of birth |
| ➕ **Add Course** | Form to insert a new course with input validation |
| 📅 **Add Lesson** | Form to schedule a new lesson with conflict detection |

---

## 🗄️ Database Schema

Three tables managed with SQLite:

```
CORSO       (CodC, Nome, Tipo, Livello)
ISTRUTTORE  (CodFisc, Nome, Cognome, Email, DataNascita)
PROGRAMMA   (CodFisc, Giorno, OrarioInizio, Durata, CodC, Sala)
```

Foreign key constraints are enforced via `PRAGMA foreign_keys = ON`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/gym-manager.git
cd gym-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create and populate the database with sample data
python setup_db.py

# 4. Run the app
streamlit run Home.py
```

Open your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
gym-manager/
├── Home.py                    # Homepage: intro + dashboard charts
├── db.py                      # SQLAlchemy engine and query utilities
├── setup_db.py                # Creates and seeds the database
├── requirements.txt
└── pages/
    ├── 1_Corsi.py             # Course browser with filters
    ├── 2_Istruttori.py        # Instructor search
    ├── 3_Inserisci_Corso.py   # Add new course (form + validation)
    └── 4_Inserisci_Lezione.py # Schedule new lesson (form + conflict check)
```

---

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — web UI framework
- **SQLAlchemy** — database abstraction layer (ORM)
- **SQLite** — embedded relational database
- **Pandas** — data manipulation and display

---

## 📝 Notes

- The database file `palestra.db` is **not tracked** in this repo (see `.gitignore`). Run `setup_db.py` to generate it locally with sample data.
- The `db.py` module uses **SQLAlchemy** as the database abstraction layer: switching from SQLite to PostgreSQL or MySQL only requires updating the `DATABASE_URL` connection string, while all queries remain unchanged.
- Sample data in the database is AI-generated for demonstration purposes only and does not represent real individuals or organizations.
