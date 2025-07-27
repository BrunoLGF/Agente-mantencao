# components/interface.py

import streamlit as st
from utils.database import get_all_users, get_message_history

def render_interface():
    st.title("Agente de Manutenção")

    users = get_all_users()

    # Inicializa o log se ainda não existir
    if "message_log" not in st.session_state:
        st.session_state.message_log = []

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

    # Formulário para envio
    with st.form(key="message_form"):
        message = st.text_input("Enviar mensagem", placeholder="Digite sua mensagem")
        submitted = st.form_submit_button("Enviar")

        if submitted and message:
            # Adiciona a mensagem do usuário
            st.session_state.message_log.append({
                "from": selected_number,
                "message": message
            })

            # Gera resposta automática do agente
            resposta = gerar_resposta_agente(message)

            st.session_state.message_log.append({
                "from": "agente",
                "message": resposta
            })

            st.rerun()

def gerar_resposta_agente(mensagem):
    """
    Simples lógica de resposta automática do agente.
    (Você pode substituir isso por algo mais inteligente no futuro)
    """
    mensagem = mensagem.lower()
    if "parou" in mensagem or "erro" in mensagem:
        return "Recebido! Vamos encaminhar um técnico para verificar o problema."
    elif "ok" in mensagem or "obrigado" in mensagem:
        return "De nada! Qualquer coisa, estou à disposição."
    else:
        return "Entendido. A equipe de manutenção foi notificada."
