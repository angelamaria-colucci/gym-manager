"""
pages/1_Corsi.py — Visualizzazione e filtraggio dei corsi disponibili.
"""

import streamlit as st

from db import run_query

st.set_page_config(page_title="Corsi", page_icon="📚", layout="wide")

st.title("📚 Corsi disponibili")
st.markdown(
    "In questa pagina puoi **consultare** il catalogo dei corsi e **filtrarli** "
    "per tipologia e livello di difficoltà."
)

# ------------------------------------------------------------------
# METRICHE
# ------------------------------------------------------------------
num_corsi = run_query("SELECT COUNT(*) AS n FROM CORSO")["n"].iloc[0]
num_tipi  = run_query("SELECT COUNT(DISTINCT Tipo) AS n FROM CORSO")["n"].iloc[0]

m1, m2 = st.columns(2)
m1.metric("Corsi totali", num_corsi)
m2.metric("Tipi distinti", num_tipi)

st.divider()

# ------------------------------------------------------------------
# WIDGET DI INPUT
# ------------------------------------------------------------------
st.subheader("🔎 Filtri")

tipi_disponibili = run_query(
    "SELECT DISTINCT Tipo FROM CORSO ORDER BY Tipo"
)["Tipo"].tolist()

range_livello = run_query("SELECT MIN(Livello) AS minL, MAX(Livello) AS maxL FROM CORSO")
liv_min = int(range_livello["minL"].iloc[0])
liv_max = int(range_livello["maxL"].iloc[0])

col_f1, col_f2 = st.columns(2)
with col_f1:
    tipi_scelti = st.multiselect(
        "Tipo di corso (puoi sceglierne più di uno)",
        options=tipi_disponibili,
        default=tipi_disponibili,
    )
with col_f2:
    liv_range = st.slider(
        "Range di livello",
        min_value=liv_min,
        max_value=liv_max,
        value=(liv_min, liv_max),
    )

# ------------------------------------------------------------------
# INTERROGAZIONE CON FILTRI
# ------------------------------------------------------------------
if not tipi_scelti:
    st.warning("⚠️ Seleziona almeno un tipo di corso per visualizzare i risultati.")
    st.stop()

# SQLAlchemy usa :param come placeholder
placeholders = ",".join([f":tipo{i}" for i in range(len(tipi_scelti))])
query = f"""
    SELECT CodC AS Codice, Nome, Tipo, Livello
    FROM CORSO
    WHERE Tipo IN ({placeholders})
      AND Livello BETWEEN :liv_min AND :liv_max
    ORDER BY Tipo, Livello
"""
params = {f"tipo{i}": t for i, t in enumerate(tipi_scelti)}
params["liv_min"] = liv_range[0]
params["liv_max"] = liv_range[1]

df_corsi = run_query(query, params)

st.subheader("📋 Risultati")
if df_corsi.empty:
    st.error("❌ Nessun corso corrisponde ai filtri selezionati.")
    st.stop()

st.dataframe(df_corsi, width='stretch', hide_index=True)

# ------------------------------------------------------------------
# EXPANDER: programmi delle lezioni per i corsi selezionati
# ------------------------------------------------------------------
with st.expander("📅 Programmi delle lezioni e istruttori dei corsi filtrati"):
    codici_corsi = df_corsi["Codice"].tolist()
    ph_corsi = ",".join([f":codc{i}" for i in range(len(codici_corsi))])
    params_prog = {f"codc{i}": c for i, c in enumerate(codici_corsi)}

    df_prog = run_query(
        f"""
        SELECT
            C.Nome                             AS Corso,
            P.Giorno,
            P.OrarioInizio                     AS Inizio,
            P.Durata,
            P.Sala,
            I.Nome || ' ' || I.Cognome         AS Istruttore,
            I.Email
        FROM PROGRAMMA P
        JOIN CORSO C      ON P.CodC    = C.CodC
        JOIN ISTRUTTORE I ON P.CodFisc = I.CodFisc
        WHERE P.CodC IN ({ph_corsi})
        ORDER BY C.Nome, P.Giorno
        """,
        params_prog,
    )

    if df_prog.empty:
        st.warning("⚠️ Nessuna lezione programmata per i corsi selezionati.")
    else:
        st.dataframe(df_prog, width='stretch', hide_index=True)
