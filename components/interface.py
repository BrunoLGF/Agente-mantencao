import streamlit as st
from utils.database import (
    get_all_users,
    get_role as get_user_role,
    get_message_history,
    add_message_to_log,
)

st.set_page_config(page_title="Agente de Manutenção", layout="wide")
st.title("🛠️ Agente de Manutenção")

# Sessão para manter usuário selecionado
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

# Lateral esquerda com usuários
with st.sidebar:
    st.header("👥 Usuários")
    users = get_all_users()
    for user in users:
        button_label = f"{user['nome']} ({user['perfil']})"
        if st.button(button_label, key=user["numero"]):
            st.session_state.selected_user = user["numero"]
            st.session_state.msg_input = ""  # limpa input ao trocar usuário

# Exibe conversa
if st.session_state.selected_user:
    user_number = st.session_state.selected_user
    user_role = get_user_role(user_number)
    st.subheader(f"💬 Conversa com {user_role} - {user_number}")
    
    messages = get_message_history(user_number)
    for msg in messages:
        align = "user" if msg["autor"] != "agent" else "agent"
        st.markdown(f"**{msg['autor']}:** {msg['mensagem']}", unsafe_allow_html=True)

    # Input de mensagem
    message_input = st.text_input("Digite sua mensagem:", key="msg_input")

    if st.button("Enviar"):
        if message_input.strip():
            # Registra a mensagem do usuário
            add_message_to_log(from_number=user_number, to_number="agent", message=message_input)

            # Resposta automática simples (placeholder para lógica real)
            resposta = "Entendi! Estou processando sua solicitação..."
            add_message_to_log(from_number="agent", to_number=user_number, message=resposta)

            # Limpa campo de input
            st.session_state.msg_input = ""

            st.experimental_rerun()
else:
    st.info("Selecione um usuário na barra lateral para iniciar.")
