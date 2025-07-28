import streamlit as st
from utils.database import get_user_role, get_all_users, get_user_by_number
from core.agent import process_message
from utils.session import initialize_session_state

def show_interface():
    initialize_session_state()

    st.sidebar.title("Usuários")
    selected_user = st.sidebar.selectbox("Escolha o usuário para conversar", get_all_users(), format_func=lambda u: u["name"])
    selected_number = selected_user["number"]
    st.session_state.current_user_number = selected_number

    unread_count = st.session_state.unread_counts.get(selected_number, 0)
    if unread_count > 0:
        st.sidebar.markdown(f"🔴 Mensagens não lidas: {unread_count}")

    st.title("Agente de Manutenção")
    st.subheader(f"Conversas com {selected_number}")

    if "message_log" not in st.session_state:
        st.session_state.message_log = []

    for msg in st.session_state.message_log:
        if msg["from"] == selected_number:
            st.markdown(f"👷‍♂️ **{get_user_by_number(msg['from'])['name']}**: {msg['message']}")
        else:
            st.markdown(f"🤖 **Agente**: {msg['message']}")

    message = st.text_input("Enviar mensagem")
    if st.button("Enviar") and message.strip():
        st.session_state.message_log.append({"from": selected_number, "message": message})
        response = process_message(message, selected_number)
        st.session_state.message_log.append({"from": "agent", "message": response})

        # Reduz contador de não lidas
        if selected_number in st.session_state.unread_counts:
            st.session_state.unread_counts[selected_number] = 0
