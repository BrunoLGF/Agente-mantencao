from datetime import datetime
import time
from core.mock_db import mock_db

def timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def initialize_session_state(session_state):
    if "ordens_servico" not in session_state:
        session_state["ordens_servico"] = {}
    if "contador_os" not in session_state:
        session_state["contador_os"] = 1

    ordens_servico = session_state["ordens_servico"]
    contador_os = session_state["contador_os"]
    return ordens_servico, contador_os

def nova_os(equipamento, problema, solicitante):
    os_id = f"OS{session_state['contador_os']:03d}"
    session_state["contador_os"] += 1
    session_state["ordens_servico"][os_id] = {
        "equipamento": equipamento,
        "problema": problema,
        "solicitante": solicitante,
        "status": "aberta",
        "abertura": timestamp(),
        "responsavel": None,
        "finalizacao": None,
        "pecas_repostas": [],
        "descricao_servico": "",
        "validada": False
    }
    return os_id

def notificar(lider_manutencao=True, gerente_producao=True):
    notificacoes = []
    for os_id, os in session_state["ordens_servico"].items():
        if os["status"] == "aberta" and os["responsavel"] is None:
            notificacoes.append(f"""🔔 **Notificação de Abertura de OS**

OS: {os_id}
Horário: {os['abertura']}
Solicitante: {mock_db.get_users().get(os['solicitante'], {}).get('name', 'Desconhecido')}
Equipamento: {os['equipamento']}
Problema: {os['problema']}
Técnico Responsável: {mock_db.get_users().get(os['responsavel'], {}).get('name', 'Desconhecido')}""")
    return notificacoes

def process_message(log, sender, message, session_state):
    ordens_servico, _ = initialize_session_state(session_state)
    response = ""
    role = mock_db.get_users().get(sender, {}).get("role", "")

    if role == "Líder de Produção":
        if "parada" in message.lower():
            response = "⚠️ Deseja abrir uma OS e solicitar um mecânico?"
        elif "vazamento" in message.lower():
            response = "Deseja abrir uma OS e solicitar um mecânico?"
        elif "sim" in message.lower():
            os_id = nova_os("Prensa Hidráulica", "Vazamento de óleo", sender)
            session_state["ultima_os"] = os_id
            response = f"✅ Ordem de serviço {os_id} aberta para Prensa Hidráulica com vazamento de óleo."
        elif "está funcionando normalmente" in message.lower() or "sim" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id and os_id in ordens_servico:
                ordens_servico[os_id]["validada"] = True
                ordens_servico[os_id]["status"] = "finalizada"
                ordens_servico[os_id]["finalizacao"] = timestamp()
                response = f"✅ OS {os_id} confirmada como finalizada. Obrigado!"
        else:
            response = "Entendi. Pode me dar mais detalhes sobre o problema?"

    elif role == "Mecânico":
        if "aceito" in message.lower() or "sim" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["responsavel"] = sender
                response = f"✅ Obrigado, {mock_db.get_users().get(sender, {}).get('name', 'Técnico')}! Bom trabalho!"
        elif "concluído" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["status"] = "finalizada"
                ordens_servico[os_id]["finalizacao"] = timestamp()
                response = f"✅ OS {os_id} encerrada. Obrigado!"

    return response

def process_user_message(sender, message, session_state):
    if "log" not in session_state:
        session_state["log"] = []

    message_log = session_state["log"]
    response = process_message(message_log, sender, message, session_state)
    message_log.append({
        "sender": sender,
        "message": message,
        "response": response
    })
    return response
