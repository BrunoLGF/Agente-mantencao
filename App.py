# app.py

import streamlit as st
from agent import process_message
from mock_db import USERS, get_unread_count, get_conversation, mark_as_read

st.set_page_config(page_title="Agente de Manutenção", layout="wide")

# Sessão de estado para controle da seleção de usuário
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None

st.title("💬 Agente Virtual de Manutenção - Simulação")

# Interface dos usuários no topo
st.subheader("👥 Usuários")
cols = st.columns(len(USERS))
for i, user in enumerate(USERS):
    count = get_unread_count(user["id"])
    btn_label = f"{user['nome']}"
    if count > 0:
        btn_label += f" 🔴 {count}"
    if cols[i].button(btn_label):
        st.session_state.selected_user = user["id"]

st.markdown("---")

# Área da conversa
selected_id = st.session_state.selected_user
if selected_id:
    user = next(u for u in USERS if u["id"] == selected_id)
    st.subheader(f"📱 Simulando como: {user['nome']}")

    conversation = get_conversation(selected_id)
    for msg in conversation:
        sender = "🧠 Agente" if msg["from"] == "agent" else f"👤 {user['nome']}"
        st.markdown(f"**{sender}:** {msg['text']}")

    mark_as_read(selected_id)

    # Caixa de entrada
    input_msg = st.text_input("Digite sua mensagem", key=f"input_{selected_id}")
    if st.button("Enviar", key=f"send_{selected_id}"):
        if input_msg.strip() != "":
            process_message(user_id=selected_id, message=input_msg)
            st.experimental_rerun()
else:
    st.info("👆 Selecione um usuário acima para começar a simulação.")
