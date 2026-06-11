"""
pages/4_Inserisci_Lezione.py — Inserimento di una nuova lezione (tabella PROGRAMMA).
"""

import datetime

import streamlit as st
from sqlalchemy.exc import IntegrityError

from db import run_action, run_query

st.set_page_config(page_title="Inserisci Lezione", page_icon="📅", layout="centered")

st.title("📅 Programmazione di una nuova lezione")
st.markdown(
    "Inserisci una nuova lezione settimanale nella tabella `PROGRAMMA`. "
    "Istruttore e corso vengono scelti dai menù a tendina popolati dalla base di dati."
)

GIORNI_VALIDI = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]

# ------------------------------------------------------------------
# Opzioni dei menù a tendina popolate dal database
# ------------------------------------------------------------------
df_istr  = run_query("SELECT CodFisc, Nome, Cognome FROM ISTRUTTORE ORDER BY Cognome, Nome")
df_corsi = run_query("SELECT CodC, Nome FROM CORSO ORDER BY CodC")

opzioni_istr  = {f"{r.Nome} {r.Cognome} ({r.CodFisc})": r.CodFisc for r in df_istr.itertuples()}
opzioni_corsi = {f"{r.CodC} – {r.Nome}": r.CodC for r in df_corsi.itertuples()}

with st.form("form_lezione", clear_on_submit=False):
    etichetta_istr  = st.selectbox("Istruttore (codice fiscale)", list(opzioni_istr.keys()))
    etichetta_corso = st.selectbox("Corso", list(opzioni_corsi.keys()))
    giorno          = st.selectbox("Giorno della settimana", GIORNI_VALIDI)

    col_a, col_b = st.columns(2)
    with col_a:
        orario = st.slider(
            "Orario di inizio",
            min_value=datetime.time(8, 0),
            max_value=datetime.time(22, 0),
            value=datetime.time(9, 0),
            step=datetime.timedelta(minutes=15),
            format="HH:mm",
        )
    with col_b:
        durata = st.slider("Durata (minuti)", min_value=15, max_value=90, value=60, step=5)

    sala    = st.text_input("Sala", placeholder="Es. Sala A")
    inviato = st.form_submit_button("Programma lezione", type="primary")

if inviato:
    codfisc   = opzioni_istr[etichetta_istr]
    codc      = opzioni_corsi[etichetta_corso]
    orario_str = orario.strftime("%H:%M")
    sala       = sala.strip()

    if not sala:
        st.error("❌ Il campo 'Sala' deve essere valorizzato.")
    elif durata > 60:
        st.error("❌ Una lezione non può durare più di 60 minuti.")
    elif giorno not in GIORNI_VALIDI:
        st.error("❌ Il giorno deve essere compreso tra Lunedì e Venerdì.")
    else:
        conflitti = run_query(
            "SELECT COUNT(*) AS n FROM PROGRAMMA WHERE CodC = :codc AND Giorno = :giorno",
            {"codc": codc, "giorno": giorno},
        )["n"].iloc[0]

        if conflitti > 0:
            st.error(
                f"❌ Esiste già una lezione del corso **{codc}** il giorno "
                f"**{giorno}**. Non è possibile programmarne un'altra lo stesso giorno."
            )
        else:
            try:
                run_action(
                    """
                    INSERT INTO PROGRAMMA
                        (CodFisc, Giorno, OrarioInizio, Durata, CodC, Sala)
                    VALUES (:codfisc, :giorno, :orario, :durata, :codc, :sala)
                    """,
                    {"codfisc": codfisc, "giorno": giorno, "orario": orario_str,
                     "durata": int(durata), "codc": codc, "sala": sala},
                )
                st.success(
                    f"✅ Lezione del corso **{codc}** programmata il **{giorno}** "
                    f"alle **{orario_str}** in **{sala}**."
                )
            except IntegrityError:
                st.error(
                    "❌ Conflitto di chiave: l'istruttore ha già una lezione "
                    f"il **{giorno}** alle **{orario_str}**."
                )
            except Exception as e:
                st.error(f"❌ Errore durante l'inserimento: {e}")
