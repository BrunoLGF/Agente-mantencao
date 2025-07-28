import streamlit as st
from components.interface import render_interface

def show_conversation_page():
    st.title("Agente de Manutenção")
    render_interface()
