from mock_db import get_user_role, get_open_orders, create_order, assign_technician, close_order

def process_message(user_number, message):
    role = get_user_role(user_number)
    response = ""
    debug = {
        "user_number": user_number,
        "role": role,
        "mensagem_recebida": message,
        "ação_tomada": ""
    }

    if role == "Líder de Produção":
        if "parada" in message or "problema" in message or "defeito" in message:
            response = (
                "Mensagem recebida! Deseja que eu abra uma Ordem de Serviço para essa ocorrência?"
            )
            debug["ação_tomada"] = "Sugerir abertura de OS"
        elif "sim" in message.lower() and get_open_orders(user_number) is None:
            order_id = create_order(user_number, message)
            response = (
                f"Ordem de Serviço #{order_id} aberta! Irei acionar um técnico agora mesmo."
            )
            debug["ação_tomada"] = f"Abrir OS #{order_id}"
        else:
            response = "Ainda estou aprendendo a interpretar esse tipo de solicitação. Pode reformular?"
            debug["ação_tomada"] = "Solicitação não reconhecida"

    elif role in ["Mecânico", "Eletricista"]:
        if "aceito" in message.lower() or "estou indo" in message.lower():
            assign_technician(user_number)
            response = "Atendimento confirmado! A equipe de gestão foi notificada."
            debug["ação_tomada"] = "Técnico aceitou a OS"
        elif "finalizado" in message.lower():
            close_order(user_number)
            response = "Serviço marcado como finalizado. Aguardando validação da produção."
            debug["ação_tomada"] = "Técnico finalizou OS"
        else:
            response = "Entendi. Você está a caminho ou finalizou o serviço?"
            debug["ação_tomada"] = "Técnico respondeu algo não padronizado"

    elif role in ["Líder de Manutenção", "Gerente de Produção", "Diretor"]:
        if "status" in message.lower():
            open_orders = get_open_orders()
            if open_orders:
                response = f"Existem {len(open_orders)} ordens em aberto:\n" + "\n".join(
                    [f"- #{o['id']} para {o['equipamento']}" for o in open_orders]
                )
                debug["ação_tomada"] = "Listar OS abertas"
            else:
                response = "Não há ordens de serviço abertas no momento."
                debug["ação_tomada"] = "Sem OS abertas"
        elif "histórico" in message.lower():
            # Aqui você pode implementar histórico total
            response = "Histórico completo ainda está em desenvolvimento."
            debug["ação_tomada"] = "Solicitação de histórico"
        else:
            response = "Comando recebido. Pode reformular ou solicitar o status das ordens."
            debug["ação_tomada"] = "Comando geral da gestão"

    else:
        response = "Desculpe, ainda não reconheço seu perfil para essa ação."
        debug["ação_tomada"] = "Perfil não reconhecido"

    return response, debug
