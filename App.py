import streamlit as st
from agent import process_message
from mock_db import get_users, get_messages_for_user, save_message

# Título da aplicação
st.set_page_config(page_title="Agente Virtual de Manutenção", layout="wide")
st.title("💬 Agente Virtual de Manutenção - Simulação")

# Lista de usuários (simulados)
users = get_users()

# Sidebar para depuração
with st.sidebar:
    st.header("🛠️ Modo Debug")
    if "debug" in st.session_state:
        show_debug = st.checkbox("Mostrar Debug", value=st.session_state["debug"])
    else:
        show_debug = st.checkbox("Mostrar Debug")
        st.session_state["debug"] = show_debug
    st.session_state["debug"] = show_debug

# Mostrar os botões dos usuários na horizontal
st.subheader("👥 Usuários")
cols = st.columns(len(users))
selected_user = None
for i, (label, number) in enumerate(users.items()):
    with cols[i]:
        if st.button(label):
            selected_user = number
            st.session_state["selected_user"] = number

# Definir usuário selecionado
if "selected_user" in st.session_state:
    selected_user = st.session_state["selected_user"]

if selected_user:
    label = [k for k, v in users.items() if v == selected_user][0]
    st.markdown(f"### 🧑‍💻 Simulando como: **{label}**")
    
    # Histórico de mensagens
    history = get_messages_for_user(selected_user)
    for item in history:
        sender = item["from"]
        msg = item["message"]
        if sender == "agent":
            st.chat_message("assistant").write(f"🧠 Agente: {msg}")
        else:
            label_sender = [k for k, v in users.items() if v == sender]
            name = label_sender[0] if label_sender else "Usuário"
            st.chat_message("user").write(f"👤 {name}: {msg}")
    
    # Campo de envio
    prompt = st.text_input("Digite sua mensagem", key="msg_input")
    if st.button("Enviar"):
        if prompt.strip() != "":
            # Salvar mensagem do usuário
            save_message(selected_user, prompt, "user")
            # Processar mensagem
            resposta, debug = process_message(selected_user, prompt)
            # Salvar resposta do agente
            save_message(selected_user, resposta, "agent")
            st.session_state["last_debug"] = debug
            st.rerun()
        else:
            st.warning("Digite uma mensagem antes de enviar.")

    # Debug
    if show_debug and "last_debug" in st.session_state:
        st.subheader("📊 DEBUG")
        st.json(st.session_state["last_debug"])
