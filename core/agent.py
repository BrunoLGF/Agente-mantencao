import json
import os
from datetime import datetime
from uuid import uuid4

STATE_FILE = "data/state.json"

def carregar_estado():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "os_counter": 1,
        "open_os": {},
        "history": {},
        "active_user": None,
        "notifications": {}
    }

def salvar_estado(estado):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=4, ensure_ascii=False)

estado = carregar_estado()

def adicionar_mensagem(numero, mensagem, remetente):
    if numero not in estado["history"]:
        estado["history"][numero] = []

    estado["history"][numero].append({
        "remetente": remetente,
        "mensagem": mensagem,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

    salvar_estado(estado)

def processar_mensagem(numero, mensagem):
    adicionar_mensagem(numero, mensagem, "usuário")

    resposta = ""
    notificacoes = []

    if "máquina" in mensagem.lower() or "parada" in mensagem.lower():
        resposta = "Entendi! Deseja abrir uma Ordem de Serviço para essa ocorrência?"
    elif mensagem.strip().lower() in ["sim", "sim.", "quero", "quero sim"]:
        os_id = f"OS-{str(uuid4())[:8].upper()}"
        estado["open_os"][os_id] = {
            "usuario": numero,
            "status": "aberta",
            "hora_abertura": datetime.now().strftime("%H:%M:%S")
        }
        salvar_estado(estado)
        resposta = f"Ordem de Serviço {os_id} registrada com sucesso. Enviando notificação para a equipe de manutenção."
        notificacoes.append({
            "para": "equipe",
            "mensagem": f"🚨 Nova OS criada por {numero}: {os_id}"
        })
    elif "andamento" in mensagem.lower():
        resposta = "Consultando o andamento... (em breve resposta detalhada)"
    elif "relatório" in mensagem.lower():
        resposta = "Gerando relatório de Ordens de Serviço do dia... (em breve funcionalidade ativa)"
    else:
        resposta = "Desculpe, ainda estou aprendendo. Você poderia reformular ou ser mais específico?"

    adicionar_mensagem(numero, resposta, "agente")

    return resposta, notificacoes
