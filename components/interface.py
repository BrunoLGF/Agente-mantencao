# components/interface.py

import streamlit as st
from utils.database import get_all_users, get_message_history

def render_interface():
    st.title("Agente de Manutenção")

    users = get_all_users()

    # Coluna lateral fixa para seleção de usuários
    with st.sidebar:
        st.header("Usuários")
        selected_number = st.radio(
            "Escolha o usuário para conversar",
            options=[user["numero"] for user in users],
            format_func=lambda numero: next((user["nome"] for user in users if user["numero"] == numero), str(numero))
        )

    # Histórico de mensagens
    st.subheader(f"Conversas com {selected_number}")
    messages = get_message_history(selected_number)
    for msg in messages:
        st.markdown(f"**{msg['autor']}**: {msg['mensagem']}")

    # Entrada de mensagem
    with st.form(key="message_form"):
        message = st.text_input("Enviar mensagem", placeholder="Digite sua mensagem")
        submitted = st.form_submit_button("Enviar")
        if submitted and message:
            st.session_state.message_log.append({"from": selected_number, "message": message})
            st.rerun()
