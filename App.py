import streamlit as st
from datetime import datetime
import uuid

# Simulação de banco de dados em memória
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {
        "11 00000-0001": "Diretor",
        "11 00000-0002": "Gerente de Produção",
        "11 00000-0003": "Líder de Manutenção",
        "11 00000-0004": "Líder de Produção 1",
        "11 00000-0005": "Líder de Produção 2",
        "11 00000-0010": "Mecânico 1",
        "11 00000-0011": "Mecânico 2",
        "11 00000-0020": "Eletricista 1",
        "11 00000-0021": "Eletricista 2"
    }

# Função para enviar mensagem
def enviar_mensagem(remetente, destinatario, texto):
    st.session_state.mensagens.append({
        "id": str(uuid.uuid4()),
        "remetente": remetente,
        "destinatario": destinatario,
        "texto": texto,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "lido": False
    })

# Interface
st.title("💬 Simulador de Agente de Manutenção via WhatsApp")

modo_debug = st.checkbox("🔧 Modo Debug (mostrar bastidores)")

perfil = st.selectbox("👤 Selecione seu número (perfil)", list(st.session_state.usuarios.keys()), format_func=lambda x: f"{x} - {st.session_state.usuarios[x]}")

st.markdown("---")

aba = st.radio("📨 Ação", ["Enviar mensagem", "Visualizar mensagens recebidas"])

if aba == "Enviar mensagem":
    destino = st.selectbox("👥 Enviar para:", [k for k in st.session_state.usuarios.keys() if k != perfil], format_func=lambda x: f"{x} - {st.session_state.usuarios[x]}")
    mensagem = st.text_area("✍️ Mensagem")
    if st.button("📤 Enviar"):
        if mensagem.strip():
            enviar_mensagem(perfil, destino, mensagem.strip())
            st.success("Mensagem enviada!")
        else:
            st.warning("Digite uma mensagem antes de enviar.")
else:
    mensagens_recebidas = [m for m in st.session_state.mensagens if m['destinatario'] == perfil]
    if mensagens_recebidas:
        for m in sorted(mensagens_recebidas, key=lambda x: x['timestamp'], reverse=True):
            st.info(f"De: {st.session_state.usuarios[m['remetente']]} ({m['remetente']})\n\n📩 {m['texto']}\n🕒 {m['timestamp']}")
    else:
        st.write("📭 Nenhuma mensagem recebida ainda.")

if modo_debug:
    st.markdown("---")
    st.subheader("🧠 Bastidores (modo debug)")
    st.json(st.session_state.mensagens)
