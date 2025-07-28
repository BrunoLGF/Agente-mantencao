# utils/equipment_data.py

equipments = {
    1: {
        "nome": "Ponte Rolante 1",
        "setor": "Movimentação",
        "falhas_comuns": [
            {
                "descricao": "Sem freio no moitão",
                "tipo": "elétrica ou mecânica",
                "tempo_estimado": "1 hora"
            },
            {
                "descricao": "Comando não trava no fim de curso",
                "tipo": "elétrica",
                "tempo_estimado": "30 minutos"
            },
            {
                "descricao": "Cabo de aço com marcas e trama rompida",
                "tipo": "mecânica",
                "tempo_estimado": "3 horas"
            }
        ]
    },
    2: {
        "nome": "Prensa Excêntrica 250T 2",
        "setor": "Estamparia",
        "falhas_comuns": [
            {
                "descricao": "Não libera a função em automático da linha",
                "tipo": "elétrica",
                "tempo_estimado": "45 minutos"
            },
            {
                "descricao": "Falha ao acionar a fricção",
                "tipo": "elétrica ou mecânica",
                "tempo_estimado": "30 minutos"
            },
            {
                "descricao": "Vazamento de ar",
                "tipo": "mecânica",
                "tempo_estimado": "15 minutos a 2 horas"
            }
        ]
    },
    3: {
        "nome": "Prensa Hidraulica 3",
        "setor": "Estamparia",
        "falhas_comuns": [
            {
                "descricao": "Martelo não se movimenta",
                "tipo": "elétrica ou mecânica",
                "tempo_estimado": "20 minutos a 1 hora"
            },
            {
                "descricao": "Martelo fora de posição",
                "tipo": "elétrica",
                "tempo_estimado": "20 minutos"
            },
            {
                "descricao": "Prensa sem pressão de trabalho",
                "tipo": "mecânica",
                "tempo_estimado": "30 minutos a 2 horas"
            }
        ]
    }
}

def get_equipment_by_id(equip_id):
    return equipments.get(equip_id, None)

def list_all_equipments():
    return equipments
