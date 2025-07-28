from utils.database import get_user_role, get_user_by_number
from datetime import datetime

def process_message(message_log, sender, message, session_state):
    role = get_user_role(sender)
    response = ""
    timestamp = datetime.now().strftime("%H:%M")

    # Inicializa o estado global da OS se não existir
    if "ordens_servico" not in session_state:
        session_state["ordens_servico"] = {}
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
                notificacoes.append(f"🔔 Notificação de Abertura de OS\n"
                                    f"OS: {os_id}\n"
                                    f"Horário: {os['abertura']}\n"
                                    f"Solicitante: {get_user_by_number(os['solicitante'])['name']}\n"
                                    f"Equipamento: {os['equipamento']}\n"
                                    f"Problema: {os['problema']}\n"
                                    f"Técnico Responsável: {get_user_by_number(os['responsavel'])['name']}")
        return notificacoes

    if role == "lider_producao":
        if "parada" in message.lower():
            response = "Qual o problema identificado?"
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

    elif role == "mecanico":
        if "aceito" in message.lower() or "sim" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["responsavel"] = sender
                response = f"✅ Obrigado, {get_user_by_number(sender)['name']}! Bom trabalho!"
        elif "concluído" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                response = "O equipamento está funcionando normalmente?"
        elif "funcionando" in message.lower():
            response = "Foi realizada a troca de alguma peça?"
        elif "sim" in message.lower():
            response = "Liste as peças que foram substituídas."
        elif "mangueira" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["pecas_trocadas"].append("Mangueira hidráulica YY")
                response = "Qual o serviço realizado?"
        elif "troca da mangueira" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["descricao_servico"] = "Troca da mangueira hidráulica"
                response = "Posso confirmar o fechamento da OS ou deseja revisar?"
        elif "finalizar" in message.lower():
            os_id = session_state.get("ultima_os")
            if os_id:
                ordens_servico[os_id]["status"] = "finalizada"
                ordens_servico[os_id]["finalizacao"] = timestamp
                response = f"✅ OS {os_id} encerrada com sucesso."

    elif role in ["lider_manutencao", "gerente_producao"]:
        response = "\n\n".join(notificar())

    else:
        response = "Olá! Como posso ajudar no suporte à manutenção?"

    return response
