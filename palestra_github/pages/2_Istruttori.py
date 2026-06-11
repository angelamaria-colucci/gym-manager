"""
pages/2_Istruttori.py — Visualizzazione degli istruttori disponibili.
"""

import datetime

import streamlit as st

from db import run_query

st.set_page_config(page_title="Istruttori", page_icon="🧑‍🏫", layout="wide")

st.title("🧑‍🏫 Istruttori")
st.markdown(
    "Cerca gli istruttori per **cognome** e/o filtra per **data di nascita** "
    "tramite l'intervallo di date."
)

st.divider()

# ------------------------------------------------------------------
# WIDGET DI INPUT
# ------------------------------------------------------------------
st.subheader("🔎 Filtri di ricerca")

cognome = st.text_input("Cognome dell'istruttore (anche parziale)", value="")

col_d1, col_d2 = st.columns(2)
with col_d1:
    data_da = st.date_input(
        "Nato/a dal",
        value=datetime.date(1970, 1, 1),
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY",
    )
with col_d2:
    data_a = st.date_input(
        "Nato/a al",
        value=datetime.date.today(),
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY",
    )

# ------------------------------------------------------------------
# INTERROGAZIONE
# ------------------------------------------------------------------
df_istruttori = run_query(
    """
    SELECT Nome, Cognome, Email, DataNascita
    FROM ISTRUTTORE
    WHERE Cognome LIKE :cognome
      AND DataNascita BETWEEN :data_da AND :data_a
    ORDER BY Cognome, Nome
    """,
    {"cognome": f"%{cognome}%", "data_da": str(data_da), "data_a": str(data_a)},
)

st.divider()
st.subheader("📋 Risultati")

if df_istruttori.empty:
    st.warning("⚠️ Nessun istruttore trovato con i criteri selezionati.")
else:
    st.caption(f"Trovati {len(df_istruttori)} istruttori.")
    for _, riga in df_istruttori.iterrows():
        with st.container(border=True):
            col_icona, col_info = st.columns([1, 6])
            with col_icona:
                st.markdown("# 🧑‍🏫")
            with col_info:
                st.markdown(f"### {riga['Nome']} {riga['Cognome']}")
                st.markdown(f"📧 **Email:** {riga['Email']}")
                st.markdown(f"🎂 **Data di nascita:** {riga['DataNascita']}")
