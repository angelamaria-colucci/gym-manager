"""
pages/3_Inserisci_Corso.py — Inserimento di un nuovo corso (tabella CORSO).
"""

import streamlit as st
from sqlalchemy.exc import IntegrityError

from db import run_action, run_query

st.set_page_config(page_title="Inserisci Corso", page_icon="➕", layout="centered")

st.title("➕ Inserimento nuovo corso")
st.markdown(
    "Compila il modulo per aggiungere un nuovo corso alla tabella `CORSO`. "
    "Tutti i campi sono **obbligatori**."
)

tipi_esistenti = run_query("SELECT DISTINCT Tipo FROM CORSO ORDER BY Tipo")["Tipo"].tolist()

with st.form("form_corso", clear_on_submit=False):
    codc   = st.text_input("Codice corso (CodC) — deve iniziare con 'CT'", placeholder="CT011")
    nome   = st.text_input("Nome del corso", placeholder="Es. Power Yoga")

    col_a, col_b = st.columns(2)
    with col_a:
        tipo_scelto = st.selectbox("Tipo", options=tipi_esistenti + ["➕ Nuovo tipo..."])
    with col_b:
        livello = st.number_input("Livello (1–4)", min_value=1, max_value=4, step=1, value=1)

    nuovo_tipo = ""
    if tipo_scelto == "➕ Nuovo tipo...":
        nuovo_tipo = st.text_input("Specifica il nuovo tipo")

    inviato = st.form_submit_button("Inserisci corso", type="primary")

if inviato:
    tipo = nuovo_tipo.strip() if tipo_scelto == "➕ Nuovo tipo..." else tipo_scelto
    codc = codc.strip()
    nome = nome.strip()

    if not codc or not nome or not tipo:
        st.error("❌ Tutti i campi devono essere valorizzati.")
    elif not codc.upper().startswith("CT"):
        st.error("❌ Il codice corso (CodC) deve iniziare con 'CT'.")
    elif not (1 <= int(livello) <= 4):
        st.error("❌ Il livello deve essere un numero intero compreso tra 1 e 4.")
    else:
        try:
            run_action(
                "INSERT INTO CORSO (CodC, Nome, Tipo, Livello) VALUES (:codc, :nome, :tipo, :livello)",
                {"codc": codc.upper(), "nome": nome, "tipo": tipo, "livello": int(livello)},
            )
            st.success(f"✅ Corso **{codc.upper()} – {nome}** inserito correttamente!")
        except IntegrityError:
            st.error(f"❌ Esiste già un corso con codice **{codc.upper()}** (chiave duplicata).")
        except Exception as e:
            st.error(f"❌ Errore durante l'inserimento: {e}")
