import streamlit as st
from core.agent import process_user_message
from utils.session import init_session_state
import utils.mock_db as mock_db  # Importa a base simulada

def show_interface():
    st.set_page_config(page_title="Agente de Manutenção", layout="wide")

    # Inicializa estado da sessão
    init_session_state()

    # Define lista de usuários com base nos nomes
    users_dict = mock_db.get_users()
    selected_user = st.sidebar.selectbox(
        "Escolha o usuário para conversar:",
        list(users_dict.keys())
    )

    user_number = users_dict[selected_user]
    user_role = mock_db.get_user_role(user_number)
    st.session_state.user_number = user_number
    st.session_state.user_role = user_role

    st.sidebar.markdown(f"**Função:** {user_role}")
    st.sidebar.markdown(f"**Número:** {user_number}")

    st.title("Agente Virtual de Manutenção")

    st.markdown(f"**Usuário atual:** {selected_user} ({user_role})")

    # Histórico de mensagens
    messages = mock_db.get_message_history(user_number)
    for msg in messages:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["mensagem"])

    # Campo de entrada de mensagem
    if prompt := st.chat_input("Digite sua mensagem para a agente:"):
        with st.chat_message("Usuário"):
            st.markdown(prompt)
        response = process_user_message(user_number, prompt)
        with st.chat_message("Agente"):
            st.markdown(response)
