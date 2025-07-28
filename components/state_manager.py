from utils import mock_db
import streamlit as st
from datetime import datetime

def process_message(user_number, message):
    role = mock_db.get_user_role(user_number)
    nome = mock_db.get_users()[user_number]["name"]

    if "message_log" not in st.session_state:
        st.session_state.message_log = []

    if "ordens_servico" not in st.session_state:
        st.session_state.ordens_servico = {}

    if "contador_os" not in st.session_state:
        st.session_state.contador_os = 1

    resposta = ""
    agora = datetime.now().strftime("%H:%M:%S")

    if role == "Líder de Produção":
        if "parada" in message.lower():
            numero_os = f"OS-{st.session_state.contador_os:03d}"
            st.session_state.contador_os += 1
            st.session_state.ultima_os = numero_os
            st.session_state.ordens_servico[numero_os] = {
                "status": "aberta",
                "solicitante": nome,
                "equipamento": message,
                "hora_abertura": agora,
                "responsável": None,
                "problema": "",
                "peças": [],
                "serviço": "",
                "hora_fechamento": ""
            }
            resposta = f"{nome}, deseja abrir uma ordem de serviço para: '{message}'?"
        elif "sim" in message.lower() and st.session_state.ultima_os:
            os = st.session_state.ordens_servico[st.session_state.ultima_os]
            os["status"] = "pendente"
            resposta = f"Ordem de serviço {st.session_state.ultima_os} aberta para {os['equipamento']}. Aguardando técnico."
        else:
            resposta = f"{nome}, por favor detalhe se deseja abrir uma ordem de serviço ou informe o problema."

    elif role == "Mecânico":
        if "aceito" in message.lower() and st.session_state.ultima_os:
            os = st.session_state.ordens_servico[st.session_state.ultima_os]
            os["responsável"] = nome
            resposta = f"{nome}, confirmado! Você assumiu a {st.session_state.ultima_os}."
        elif "concluído" in message.lower():
            resposta = f"{nome}, o serviço foi concluído com sucesso? O equipamento voltou a funcionar normalmente?"
        elif "sim" in message.lower():
            resposta = f"{nome}, houve troca de peças?"
        elif "não" in message.lower():
            resposta = f"{nome}, deseja encerrar a {st.session_state.ultima_os}?"
        elif "encerrar" in message.lower():
            os = st.session_state.ordens_servico[st.session_state.ultima_os]
            os["hora_fechamento"] = agora
            os["status"] = "fechada"
            resposta = f"Ordem {st.session_state.ultima_os} encerrada. Obrigado, {nome}."
        else:
            resposta = f"{nome}, poderia informar o status da OS ou peça trocada?"

    else:
        resposta = f"Olá {nome}, sua função ainda não está com interações definidas."

    st.session_state.message_log.append({
        "from": user_number,
        "message": message,
        "response": resposta
    })

    return resposta
