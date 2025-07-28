from utils import mock_db
from datetime import datetime

def process_message(message_log, sender, message, session_state):
    role = mock_db.get_user_role(sender)
    response = ""
    timestamp = datetime.now().strftime("%H:%M")

    # Inicializa o estado global da OS se não existir
    if "ordens_servico" not in session_state:
        session_state["ordens_servico"] = {}
    if "contador_os" not in session_state:
        session_state["contador_os"] = 1

    ordens_servico = session_state["ordens_servico"]
    contador_os = session_state["contador_os"]

    def nova_os(equipamento, problema, solicitante):
        os_id = f"OS{contador_os:03d}"
        session_state["contador_os"] += 1
        ordens_servico[os_id] = {
            "equipamento": equipamento,
            "problema": problema,
            "solicitante": solicitante,
            "status": "aberta",
            "abertura": timestamp,
            "responsavel": None,
            "finalizacao": None,
            "pecas_trocadas": [],
            "descricao_servico": "",
            "validada": False
        }
        return os_id

    def notificar(lider_manutencao=True, gerente_producao=True):
        notificacoes = []
        for os_id, os in ordens_servico.items():
            if os["status"] == "aberta" and os["responsavel"]:
                notificacoes.append(f"""🔔 Notificação de Abertura de OS\n
OS: {os_id}\n
Horário: {os['abertura']}\n
Solicitante: {mock_db.get_users().get(os['solicitante'], {}).get('name', 'Desconhecido')}\n
Equipamento: {os['equipamento']}\n
Problema: {os['problema']}\n
Técnico Responsável: {mock_db.get_users().get(os['responsavel'], {}).get('name', 'Desconhecido')}""")
        return notificacoes

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
                ordens_servico[os_id]["finalizacao"] = timestamp
                response = f"✅ OS {os_id} confirmada como finalizada. Obrigado!"
        else:
            response = "Entendi. Pode me dar mais detalhes sobre o problema?"

    elif role == "Mecânico":
        if "aceito" in message.lower() or "sim" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["responsavel"] = sender
                response = f"✅ Obrigado, {mock_db.get_users().get(sender, {}).get('name', 'Técnico')}! Bom trabalho"
        elif "concluído" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["status"] = "finalizada"
                ordens_servico[os_id]["finalizacao"] = timestamp
                response = f"✅ OS {os_id} encerrada. Obrigado!"

    return response
