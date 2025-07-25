# components/interface.py

import streamlit as st
from logic.agent import process_message
from utils.session import get_current_user, get_users, switch_user, unread_counts

def render_interface():
    st.title("🛠️ Agente de Manutenção")
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Usuários")
        for user in get_users():
            count = unread_counts(user)
            label = f"{user['nome']} ({count})" if count > 0 else user["nome"]
            if st.button(label, key=user["numero"]):
                switch_user(user["numero"])

    with col2:
        current_user = get_current_user()
        st.subheader(f"Conversa - {current_user['nome']}")
        history = st.session_state["mensagens"][current_user["numero"]]

        for msg in history:
            align = "🧑‍🔧" if msg["remetente"] == current_user["numero"] else "🤖"
            st.markdown(f"**{align}** {msg['mensagem']}")

        nova_msg = st.text_input("Digite sua mensagem:", key="input_msg")
        if st.button("Enviar"):
            if nova_msg.strip():
                history.append({
                    "remetente": current_user["numero"],
                    "mensagem": nova_msg.strip()
                })
                resposta = process_message(current_user["numero"], nova_msg.strip())
                history.append({
                    "remetente": "agente",
                    "mensagem": resposta
                })
                st.experimental_rerun()
