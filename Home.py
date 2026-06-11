"""
Home.py — Pagina principale dell'applicazione.
Avviare con:  streamlit run Home.py
"""

import pandas as pd
import streamlit as st

from db import run_query

st.set_page_config(
    page_title="Gestione Palestra",
    page_icon="🏋️",
    layout="wide",
)

# ------------------------------------------------------------------
# INTRODUZIONE
# ------------------------------------------------------------------
st.title("🏋️ Gestione Corsi e Lezioni della Palestra")

st.markdown(
    """
    Benvenuto/a nell'applicazione per la gestione di una **palestra**.

    Questa applicazione multi-pagina permette di **consultare** e **inserire** le
    informazioni contenute nel database, organizzato nelle tabelle
    `CORSO`, `ISTRUTTORE` e `PROGRAMMA`.
    """
)

st.markdown("👈 Usa il **menù laterale** per navigare tra le pagine.")
st.divider()

# ------------------------------------------------------------------
# GRAFICI SULLE LEZIONI PROGRAMMATE
# ------------------------------------------------------------------
st.header("📊 Panoramica delle lezioni programmate")

col1, col2 = st.columns(2)

# --- Area Chart: numero di lezioni per slot orario ---
with col1:
    st.subheader("Lezioni per slot orario")
    df_slot = run_query(
        """
        SELECT OrarioInizio AS Slot, COUNT(*) AS NumeroLezioni
        FROM PROGRAMMA
        GROUP BY OrarioInizio
        ORDER BY OrarioInizio
        """
    )
    if df_slot.empty:
        st.info("Nessuna lezione in programma.")
    else:
        df_slot = df_slot.set_index("Slot")
        st.area_chart(df_slot, y="NumeroLezioni")
        st.caption("Numero di lezioni programmate per ogni orario di inizio.")

# --- Bar Chart: numero di lezioni per giorno della settimana ---
with col2:
    st.subheader("Lezioni per giorno della settimana")
    df_giorni = run_query(
        """
        SELECT Giorno, COUNT(*) AS NumeroLezioni
        FROM PROGRAMMA
        GROUP BY Giorno
        """
    )
    if df_giorni.empty:
        st.info("Nessuna lezione in programma.")
    else:
        ordine = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        df_giorni["Giorno"] = pd.Categorical(
            df_giorni["Giorno"], categories=ordine, ordered=True
        )
        df_giorni = df_giorni.sort_values("Giorno").set_index("Giorno")
        st.bar_chart(df_giorni, y="NumeroLezioni")
        st.caption("Numero di lezioni programmate per ogni giorno della settimana.")
