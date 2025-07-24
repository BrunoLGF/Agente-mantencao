import datetime

# Simula usuários e papéis
users = {
    "Diretor": "11000000001",
    "Gerente de Produção": "11000000002",
    "Líder de Manutenção": "11000000003",
    "Líder Produção 1": "11000000004",
    "Líder Produção 2": "11000000005",
    "Mecânico 1": "11000000010",
    "Mecânico 2": "11000000011",
    "Eletricista 1": "11000000020",
    "Eletricista 2": "11000000021",
}

roles = {
    "11000000001": "Diretor",
    "11000000002": "Gerente de Produção",
    "11000000003": "Líder de Manutenção",
    "11000000004": "Líder de Produção",
    "11000000005": "Líder de Produção",
    "11000000010": "Mecânico",
    "11000000011": "Mecânico",
    "11000000020": "Eletricista",
    "11000000021": "Eletricista",
}

# Simula histórico de mensagens e ordens de serviço
message_log = []
order_counter = 1
open_orders = []

def get_users():
    return users

def get_user_role(number):
    return roles.get(number, "Desconhecido")

def save_message(user_number, message, sender):
    message_log.append({
        "from": user_number if sender == "user" else "agent",
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    })

def get_messages_for_user(user_number):
    return [
        msg for msg in message_log
        if msg["from"] == user_number or msg["from"] == "agent"
    ]

def create_order(user_number, description):
    global order_counter
    new_order = {
        "id": order_counter,
        "aberta_por": user_number,
        "equipamento": description,
        "status": "aberta",
        "responsável": None,
        "timestamp": datetime.datetime.now().isoformat()
    }
    open_orders.append(new_order)
    order_counter += 1
    return new_order["id"]

def assign_technician(tech_number):
    for order in open_orders:
        if order["responsável"] is None:
            order["responsável"] = tech_number
            order["status"] = "em atendimento"
            break

def close_order(tech_number):
    for order in open_orders:
        if order["responsável"] == tech_number and order["status"] == "em atendimento":
            order["status"] = "finalizado"
            break

def get_open_orders(user_number=None):
    if user_number:
        return [
            o for o in open_orders
            if o["aberta_por"] == user_number and o["status"] != "finalizado"
        ]
    return [o for o in open_orders if o["status"] != "finalizado"]
