# components/interface.py

import streamlit as st
from utils.database import get_all_users, get_message_history
from utils.session import get_current_user, set_selected_user

def render_interface():
    st.title("Agente de Manutenção")
    current_user = get_current_user()
    if not current_user:
        st.warning("Nenhum usuário logado.")
        return

    st.sidebar.header("Usuários")
    users = get_all_users()
    for user in users:
        label = f'{user["nome"]} ({user["perfil"]})'
        if st.button(label, key=user["numero"]):
            set_selected_user(user["numero"])

    selected_user = st.session_state.get("selected_user")
    if selected_user:
        st.subheader(f"Conversas com {selected_user}")
        messages = get_message_history(selected_user)
        for msg in messages:
            st.markdown(f"**{msg['autor']}**: {msg['mensagem']}")

        nova_msg = st.text_input("Enviar mensagem", key="msg_input")
        if st.button("Enviar"):
            if nova_msg:
                st.session_state["nova_mensagem"] = nova_msg
