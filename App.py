import streamlit as st
from components.interface import show_interface

# Configuração da página (tem que ser a primeira coisa do script)
st.set_page_config(page_title="Agente de Manutenção", layout="wide")

def main():
    st.title("🛠️ Agente Virtual de Manutenção")
    show_interface()

if __name__ == "__main__":
    main()
