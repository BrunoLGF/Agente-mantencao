import streamlit as st
from core.agent import processar_mensagem, estado

st.set_page_config(page_title="Agente de Manutenção", layout="wide")

st.title("💬 Conversas com a Agente")

usuarios = {
    "11 00000-0001": "📢 Diretor",
    "11 00000-0002": "📋 Gerente Produção",
    "11 00000-0003": "🔧 Líder Manutenção",
    "11 00000-0004": "🏭 Líder Produção 1",
    "11 00000-0005": "🏭 Líder Produção 2",
    "11 00000-0010": "🛠️ Mecânico 1",
    "11 00000-0011": "🛠️ Mecânico 2",
    "11 00000-0020": "⚡ Eletricista 1",
    "11 00000-0021": "⚡ Eletricista 2",
}

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("👤 Usuários")

    usuario_selecionado = None

    for numero, nome in usuarios.items():
        mensagens = estado["history"].get(numero, [])
        nao_lidas = sum(1 for m in mensagens if m["remetente"] == "agente")

        if st.button(f"{nome} ({nao_lidas})"):
            estado["active_user"] = numero

with col2:
    if estado["active_user"]:
        numero = estado["active_user"]
        nome = usuarios[numero]
        st.subheader(f"📱 Conversa com {nome}")

        mensagens = estado["history"].get(numero, [])
        for m in mensagens:
            alinhamento = "left" if m["remetente"] == "usuário" else "right"
            st.markdown(
                f"<div style='text-align:{alinhamento}; margin: 5px;'><b>{m['remetente']}:</b> {m['mensagem']} <small>({m['timestamp']})</small></div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        msg = st.text_input("Escreva sua mensagem:")
        if st.button("Enviar"):
            resposta, notificacoes = processar_mensagem(numero, msg)
            for noti in notificacoes:
                if noti["para"] == "equipe":
                    for destino in ["11 00000-0010", "11 00000-0011", "11 00000-0020", "11 00000-0021", "11 00000-0003"]:
                        estado["history"].setdefault(destino, []).append({
                            "remetente": "agente",
                            "mensagem": noti["mensagem"],
                            "timestamp": "agora"
                        })
            st.experimental_rerun()
    else:
        st.info("Selecione um usuário na coluna da esquerda para iniciar.")
