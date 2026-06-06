import streamlit as st
import pandas as pd # <-- NOVIDADE: Nossa ferramenta de criar tabelas

st.title("Estudei - Foco na Farda 🚔")
st.write("Bem-vindo ao seu painel de controle de estudos!")

# NOVIDADE: Criando o "prontuário" (memória) para o site não esquecer os registros
if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# O formulário
with st.form("registro_diario"):
    disciplina = st.selectbox("Qual disciplina você estudou?", ["Direito Penal", "Constitucional", "Português"])
    minutos = st.number_input("Tempo de estudo (em minutos)", min_value=0)
    questoes_feitas = st.number_input("Total de Questões", min_value=0)
    erros = st.number_input("Quantos erros?", min_value=0)
    
    salvar = st.form_submit_button("Salvar Estudo")

# O que acontece quando clica no botão:
if salvar:
    # Calculando os acertos matematicamente!
    acertos = questoes_feitas - erros
    
    # Guardando os dados digitados na nossa memória
    st.session_state['historico'].append({
        "Disciplina": disciplina,
        "Minutos": minutos,
        "Questões": questoes_feitas,
        "Acertos": acertos,
        "Erros": erros
    })
    st.success("Boa! Estudo registrado e salvo com sucesso.")

# NOVIDADE: Mostrando a tabela na tela se houver algum registro
if len(st.session_state['historico']) > 0:
    st.divider() # Uma linha para separar visualmente
    st.subheader("Seu Histórico de Estudos 📊")
    
    # Transformando a memória numa tabela bonita do Pandas
    tabela = pd.DataFrame(st.session_state['historico'])
    st.dataframe(tabela, use_container_width=True)
