# app.py

import streamlit as st
from components.interface import render_interface
from utils.session import initialize_session_state

st.set_page_config(page_title="Agente de Manutenção", layout="wide")

# Inicializa estados da sessão
initialize_session_state()

# Renderiza a interface principal
render_interface()
