import streamlit as st
import pandas as pd

# O seu título personalizado!
st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# NOVIDADE: O "Cérebro" do seu edital. Aqui você cadastra as matérias e os tópicos de cada uma.
edital = {
    "Direito Penal": ["Crimes contra a pessoa", "Crimes contra o patrimônio", "Aplicação da lei penal"],
    "Constitucional": ["Direitos Fundamentais", "Organização do Estado", "Poder Judiciário"],
    "Português": ["Interpretação de Texto", "Sintaxe", "Crase e Pontuação"]
}

# 1. A escolha da disciplina fica de fora, para o site atualizar rápido
disciplina_escolhida = st.selectbox("1. Qual disciplina você estudou?", list(edital.keys()))

# 2. O formulário de registro
with st.form("registro_diario"):
    # NOVIDADE: Os tópicos se adaptam à disciplina que ele escolheu lá em cima!
    topico = st.selectbox("2. Qual tópico exato?", edital[disciplina_escolhida])
    
    minutos = st.number_input("Tempo de estudo (em minutos)", min_value=0)
    questoes_feitas = st.number_input("Total de Questões", min_value=0)
    erros = st.number_input("Quantos erros?", min_value=0)
    
    salvar = st.form_submit_button("Salvar Estudo")

if salvar:
    acertos = questoes_feitas - erros
    
    # Adicionando o Tópico na nossa memória
    st.session_state['historico'].append({
        "Disciplina": disciplina_escolhida,
        "Tópico": topico, # Salvando o tópico aqui
        "Minutos": minutos,
        "Questões": questoes_feitas,
        "Acertos": acertos,
        "Erros": erros
    })
    st.success("Boa! Estudo registrado e salvo com sucesso.")

if len(st.session_state['historico']) > 0:
    st.divider()
    st.subheader("Seu Histórico de Estudos 📊")
    tabela = pd.DataFrame(st.session_state['historico'])
    st.dataframe(tabela, use_container_width=True)
