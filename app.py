import streamlit as st
import pandas as pd

st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# NOVIDADE: A "Pasta Mestre". Agora temos Editais diferentes!
if 'editais' not in st.session_state:
    st.session_state['editais'] = {
        "Concurso Polícia": {
            "Direito Penal": ["Crimes contra a pessoa", "Crimes contra o patrimônio"],
            "Constitucional": ["Direitos Fundamentais"]
        },
        "Pós-Graduação (TC e RM)": {
            "Tomografia Computadorizada": ["Princípios Físicos", "Padrões de Imagem Torácica"],
            "Ressonância Magnética": ["Sequências T1 e T2", "Neuroimagem"]
        }
    }

# A gaveta de gerenciamento agora controla as 3 etapas
with st.expander("⚙️ Gerenciar Editais, Matérias e Tópicos"):
    
    # 1. Criar novo Edital
    st.subheader("1. Novo Edital / Projeto")
    novo_edital = st.text_input("Nome do novo edital (Ex: Banco do Brasil):")
    if st.button("Criar Edital"):
        if novo_edital and novo_edital not in st.session_state['editais']:
            st.session_state['editais'][novo_edital] = {} # Cria a pasta do edital vazia
            st.success(f"Edital '{novo_edital}' criado!")
            st.rerun()
            
    st.divider()
    
    col_mat, col_top = st.columns(2)
    
    # 2. Criar nova Matéria dentro de um Edital
    with col_mat:
        st.subheader("2. Nova Matéria")
        edital_para_materia = st.selectbox("Em qual edital quer adicionar a matéria?", list(st.session_state['editais'].keys()), key="sel_mat")
        nova_materia = st.text_input("Nome da nova matéria:")
        if st.button("Adicionar Matéria"):
            if nova_materia and nova_materia not in st.session_state['editais'][edital_para_materia]:
                st.session_state['editais'][edital_para_materia][nova_materia] = []
                st.success(f"Matéria adicionada no edital {edital_para_materia}!")
                st.rerun()
                
    # 3. Criar novo Tópico dentro de uma Matéria
    with col_top:
        st.subheader("3. Novo Tópico")
        edital_para_topico = st.selectbox("De qual edital?", list(st.session_state['editais'].keys()), key="sel_top")
        
        # Puxa só as matérias do edital escolhido acima
        materias_disponiveis = list(st.session_state['editais'][edital_para_topico].keys())
        
        if len(materias_disponiveis) > 0:
            materia_alvo = st.selectbox("Em qual matéria?", materias_disponiveis)
            novo_topico = st.text_input("Nome do novo tópico:")
            if st.button("Adicionar Tópico"):
                if novo_topico and novo_topico not in st.session_state['editais'][edital_para_topico][materia_alvo]:
                    st.session_state['editais'][edital_para_topico][materia_alvo].append(novo_topico)
                    st.success("Tópico adicionado!")
                    st.rerun()
        else:
            st.info("Crie uma matéria para este edital primeiro.")

st.divider()

# O formulário de registro agora tem 3 passos!
st.subheader("📝 Registrar Estudo Diário")

edital_escolhido = st.selectbox("1. Qual Edital/Projeto você estudou hoje?", list(st.session_state['editais'].keys()))

with st.form("registro_diario"):
    materias_do_edital = list(st.session_state['editais'][edital_escolhido].keys())
    
    # Prevenção de erro caso o edital seja novo e não tenha matérias
    if len(materias_do_edital) == 0:
        disciplina_escolhida
