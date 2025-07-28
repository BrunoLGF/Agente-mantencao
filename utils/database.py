def get_user_role(number):
    roles = {
        "11000000001": "diretor",
        "11000000002": "gerente_producao",
        "11000000003": "lider_manutencao",
        "11000000004": "lider_producao",
        "11000000005": "lider_producao",
        "11000000010": "mecanico",
        "11000000011": "mecanico",
        "11000000020": "eletricista",
        "11000000021": "eletricista",
    }
    return roles.get(str(number), "desconhecido")

def get_user_by_number(number):
    users = {
        "11000000001": {"name": "Diretor", "number": "11000000001"},
        "11000000002": {"name": "Gerente de Produção", "number": "11000000002"},
        "11000000003": {"name": "Líder de Manutenção", "number": "11000000003"},
        "11000000004": {"name": "Líder Produção 1", "number": "11000000004"},
        "11000000005": {"name": "Líder Produção 2", "number": "11000000005"},
        "11000000010": {"name": "Mecânico 1", "number": "11000000010"},
        "11000000011": {"name": "Mecânico 2", "number": "11000000011"},
        "11000000020": {"name": "Eletricista 1", "number": "11000000020"},
        "11000000021": {"name": "Eletricista 2", "number": "11000000021"},
    }
    return users.get(str(number), {"name": "Desconhecido", "number": str(number)})

def get_all_users():
    return [
        {"name": "Diretor", "number": "11000000001"},
        {"name": "Gerente de Produção", "number": "11000000002"},
        {"name": "Líder de Manutenção", "number": "11000000003"},
        {"name": "Líder Produção 1", "number": "11000000004"},
        {"name": "Líder Produção 2", "number": "11000000005"},
        {"name": "Mecânico 1", "number": "11000000010"},
        {"name": "Mecânico 2", "number": "11000000011"},
        {"name": "Eletricista 1", "number": "11000000020"},
        {"name": "Eletricista 2", "number": "11000000021"},
    ]
