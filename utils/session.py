import streamlit as st

def initialize_session_state():
    if "message_log" not in st.session_state:
        st.session_state.message_log = []
    
    if "ultima_os" not in st.session_state:
        st.session_state.ultima_os = None

    if "ordens_servico" not in st.session_state:
        st.session_state.ordens_servico = {}

    if "contador_os" not in st.session_state:
        st.session_state.contador_os = 1
