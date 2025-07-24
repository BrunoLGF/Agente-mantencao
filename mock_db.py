# mock_db.py

from datetime import datetime

# Lista de usuários simulados
USERS = [
    {"id": "11000000001", "nome": "Diretor"},
    {"id": "11000000002", "nome": "Gerente Produção"},
    {"id": "11000000003", "nome": "Líder Manutenção"},
    {"id": "11000000004", "nome": "Líder Produção 1"},
    {"id": "11000000005", "nome": "Líder Produção 2"},
    {"id": "11000000010", "nome": "Mecânico 1"},
    {"id": "11000000011", "nome": "Mecânico 2"},
    {"id": "11000000020", "nome": "Eletricista 1"},
    {"id": "11000000021", "nome": "Eletricista 2"},
]

# Mensagens por usuário
MESSAGES = {user["id"]: [] for user in USERS}
UNREAD_COUNT = {user["id"]: 0 for user in USERS}

# Histórico de OSs
ORDERS = []
ORDER_ID_COUNTER = 1


def get_conversation(user_id):
    return MESSAGES.get(user_id, [])


def add_message(user_id, text, sender="agent"):
    MESSAGES[user_id].append({"text": text, "from": sender, "time": datetime.now()})
    if sender == "agent":
        UNREAD_COUNT[user_id] += 1


def get_unread_count(user_id):
    return UNREAD_COUNT.get(user_id, 0)


def mark_as_read(user_id):
    UNREAD_COUNT[user_id] = 0


def register_order(equipamento, solicitante, tipo_falha):
    global ORDER_ID_COUNTER
    order = {
        "id": f"OS-{ORDER_ID_COUNTER:03}",
        "equipamento": equipamento,
        "falha": tipo_falha,
        "status": "Aberta",
        "solicitante": solicitante,
        "data_abertura": datetime.now(),
        "responsável": None,
        "data_finalizacao": None
    }
    ORDERS.append(order)
    ORDER_ID_COUNTER += 1
    return order


def finalizar_ordem(ordem_id, responsável):
    for ordem in ORDERS:
        if ordem["id"] == ordem_id:
            ordem["status"] = "Finalizada"
            ordem["responsável"] = responsável
            ordem["data_finalizacao"] = datetime.now()
            return ordem
    return None


def listar_ordens_por_status(status=None):
    if status:
        return [o for o in ORDERS if o["status"] == status]
    return ORDERS
