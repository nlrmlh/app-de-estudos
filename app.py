import streamlit as st

st.title("Estudei - Foco na Farda 🚔")

st.write("Bem-vindo ao seu painel de controle de estudos!")

# Criando o formulário para preencher o que estudou no dia
with st.form("registro_diario"):
    disciplina = st.selectbox("Qual disciplina você estudou?", ["Direito Penal", "Constitucional", "Português"])
    minutos = st.number_input("Tempo de estudo (em minutos)", min_value=0)
    questoes_feitas = st.number_input("Total de Questões", min_value=0)
    erros = st.number_input("Quantos erros?", min_value=0)
    
    salvar = st.form_submit_button("Salvar Estudo")

if salvar:
    st.success("Boa! Estudo registrado com sucesso.")
