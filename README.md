# Agente de Manutenção

Este é um protótipo de agente inteligente para gestão de ordens de serviço na manutenção industrial. A interface simula interações via WhatsApp com diferentes perfis de usuários (líderes, técnicos, gerentes e diretor).

## Funcionalidades

- Abertura de Ordens de Serviço (OS)
- Notificações automáticas por perfil
- Acompanhamento do status da OS
- Encerramento da OS com validação e registro
- Log de conversas e modo debug
- Simulação de múltiplos usuários com controle de mensagens não lidas

## Perfis Simulados

| Perfil               | Número Fictício  |
|----------------------|------------------|
| Diretor              | 11 00000-0001    |
| Gerente de Produção  | 11 00000-0002    |
| Líder de Manutenção  | 11 00000-0003    |
| Líder de Produção 1  | 11 00000-0004    |
| Líder de Produção 2  | 11 00000-0005    |
| Mecânico 1           | 11 00000-0010    |
| Mecânico 2           | 11 00000-0011    |
| Eletricista 1        | 11 00000-0020    |
| Eletricista 2        | 11 00000-0021    |

## Estrutura de Pastas

```
Agente-manutencao/
├── app.py
├── requirements.txt
├── README.md
├── .env
├── components/
│   ├── interface.py
│   ├── state_manager.py
├── core/
│   └── agent.py
├── data/
│   └── equipamentos.json
├── utils/
│   ├── database.py
│   ├── session.py
├── logs/
│   └── conversas.log
```

## Observações

- A inteligência do agente será expandida com base no log de conversas.
- No futuro, o agente será treinado com um histórico real e integrado a bancos de dados externos.
