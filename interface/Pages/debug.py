import streamlit as st
from utils.session import get_debug_log

def show_debug_page():
    st.title("Modo Debug")
    log = get_debug_log()
    
    if not log:
        st.info("Nenhuma atividade registrada ainda.")
        return
    
    for entry in log:
        st.markdown(f"**{entry['timestamp']}** - **{entry['actor']}**: {entry['content']}")
