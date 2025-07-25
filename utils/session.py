import streamlit as st

# Lista de usuários fictícios (simulando os números)
USERS = {
    "11 00000-0001": "Diretor",
    "11 00000-0002": "Gerente de Produção",
    "11 00000-0003": "Líder de Manutenção",
    "11 00000-0004": "Líder de Produção 1",
    "11 00000-0005": "Líder de Produção 2",
    "11 00000-0010": "Mecânico 1",
    "11 00000-0011": "Mecânico 2",
    "11 00000-0020": "Eletricista 1",
    "11 00000-0021": "Eletricista 2",
}

def get_users():
    return USERS

def get_user_name(phone_number):
    return USERS.get(phone_number, "Desconhecido")

def get_current_user():
    return st.session_state.get("current_user")

def switch_user(new_user):
    st.session_state["current_user"] = new_user

def unread_counts():
    return st.session_state.get("unread", {})

def initialize_session_state():
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = "11 00000-0004"  # Começa com Líder de Produção 1
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "unread" not in st.session_state:
        st.session_state["unread"] = {user: 0 for user in USERS}
