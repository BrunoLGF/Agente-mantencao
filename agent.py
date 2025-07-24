# agent.py

from mock_db import (
    add_message,
    register_order,
    finalizar_ordem,
    listar_ordens_por_status,
    USERS,
)

def process_message(user_id, message):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return

    # Para debug – comportamento básico por função
    nome = user["nome"].lower()

    # ⚙️ Líder de produção abrindo OS
    if "líder produção" in nome and "parado" in message.lower():
        equip = identificar_equipamento(message)
        if equip:
            add_message(user_id, f"Entendi que o equipamento **{equip}** está parado. Deseja abrir uma OS?", "agent")
        else:
            add_message(user_id, "Qual é o equipamento que está com problema?", "agent")
        return

    if "abrir uma os" in message.lower() or message.lower() == "sim":
        equip = identificar_equipamento(message)
        ordem = register_order(equipamento=equip or "Equipamento não identificado", solicitante=user["nome"], tipo_falha="Falha relatada")
        add_message(user_id, f"✅ Ordem de Serviço {ordem['id']} aberta para o equipamento {ordem['equipamento']}.", "agent")
        notificar_manutencao(ordem)
        return

    # 🧰 Técnico respondendo: quer encerrar OS
    if "encerrar" in message.lower():
        ordens_abertas = listar_ordens_por_status("Aberta")
        if ordens_abertas:
            ultima_os = ordens_abertas[-1]
            finalizar_ordem(ultima_os["id"], responsável=user["nome"])
            add_message(user_id, f"✅ OS {ultima_os['id']} encerrada com sucesso!", "agent")
        else:
            add_message(user_id, "🔍 Nenhuma OS aberta para encerrar.", "agent")
        return

    # 📊 Gerente pedindo relatório
    if "relatório" in message.lower() or "andamento" in message.lower():
        ordens = listar_ordens_por_status()
        if ordens:
            rel = "\n".join([f"{o['id']} - {o['equipamento']} - {o['status']}" for o in ordens])
            add_message(user_id, f"📄 Relatório atual de OS:\n{rel}", "agent")
        else:
            add_message(user_id, "Não há ordens registradas no momento.", "agent")
        return

    # Resposta padrão
    add_message(user_id, "🤖 Mensagem recebida! Ainda estou aprendendo a interpretar esse tipo de solicitação. Pode reformular?", "agent")


def identificar_equipamento(message):
    equipamentos = ["ponte rolante", "prensa excêntrica", "prensa hidráulica"]
    for eq in equipamentos:
        if eq in message.lower():
            return eq.title()
    return None


def notificar_manutencao(ordem):
    # Simulando notificação para equipe de manutenção
    manutencao_ids = ["11000000010", "11000000011", "11000000020", "11000000021"]
    for tech_id in manutencao_ids:
        add_message(tech_id, f"🔧 Nova OS {ordem['id']} aberta para: {ordem['equipamento']}", "agent")

    # Notifica também líder e gerente
    add_message("11000000003", f"📢 Abertura da OS {ordem['id']} - {ordem['equipamento']}", "agent")
    add_message("11000000002", f"📢 Abertura da OS {ordem['id']} - {ordem['equipamento']}", "agent")
