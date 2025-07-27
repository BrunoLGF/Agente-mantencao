from utils.mock_db import users as USERS, message_log as MESSAGES

def get_all_users():
    return [
        {
            "nome": nome,
            "numero": numero,
            "perfil": get_role(numero)
        }
        for nome, numero in USERS.items()
    ]

def get_message_history(user_number):
    return [
        {
            "autor": "Usuário" if msg["from"] == user_number else "Agente",
            "mensagem": msg["message"]
        }
        for msg in MESSAGES
        if msg["from"] == user_number or msg["from"] == "agent"
    ]

def get_role(number):
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
    return roles.get(number, "Desconhecido")
