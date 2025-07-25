import streamlit as st
from core.agent import estado

st.set_page_config(page_title="Modo Debug", layout="wide")

st.title("🛠️ Modo Debug da Agente")

st.header("📦 Variáveis Internas")
st.json(estado)

st.markdown("---")

st.header("🗃️ Histórico de Mensagens por Usuário")

for numero, mensagens in estado["history"].items():
    st.subheader(f"Usuário: {numero}")
    for msg in mensagens:
        remetente = msg.get("remetente", "desconhecido")
        conteudo = msg.get("mensagem", "")
        timestamp = msg.get("timestamp", "sem horário")
        st.markdown(f"- **{remetente}** ({timestamp}): {conteudo}")
