import streamlit as st
from utils import mock_db
from core.agent import process_message
from utils.session import initialize_session_state

def show_interface():
    initialize_session_state()

    st.sidebar.title("Usuários")
    selected_user = st.sidebar.selectbox(
        "Escolha o usuário para conversar:",
        list(mock_db.get_users().keys()),
        format_func=lambda x: mock_db.get_users()[x]["name"]
    )
    st.session_state.current_user_number = selected_user

    unread_count = st.session_state.unread_counts.get(selected_user, 0)
    if unread_count > 0:
        st.sidebar.markdown(f"🔴 Mensagens não lidas: **{unread_count}**")

    st.title("🛠️ Agente de Manutenção")
    st.subheader(f"💬 Conversas com {mock_db.get_users()[selected_user]['name']}")

    if "message_log" not in st.session_state:
        st.session_state.message_log = []

    for msg in st.session_state.message_log:
        if msg["from"] == selected_user:
            st.markdown(f"👷 **{mock_db.get_users()[msg['from']]['name']}**: {msg['message']}")
        elif msg["from"] == "agent":
            st.markdown(f"🤖 **Agente**: {msg['message']}")

    message = st.text_input("Digite sua mensagem:")
    if st.button("Enviar") and message.strip():
        st.session_state.message_log.append({
            "from": selected_user,
            "message": message
        })

        response = process_message(
            st.session_state.message_log,
            selected_user,
            message,
            st.session_state
        )

        st.session_state.message_log.append({
            "from": "agent",
            "message": response
        })

        # Zera contador de não lidas
        if selected_user in st.session_state.unread_counts:
            st.session_state.unread_counts[selected_user] = 0
