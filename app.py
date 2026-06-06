import streamlit as st
import pandas as pd

st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

edital = {
    "Direito Penal": ["Crimes contra a pessoa", "Crimes contra o patrimônio", "Aplicação da lei penal"],
    "Constitucional": ["Direitos Fundamentais", "Organização do Estado", "Poder Judiciário"],
    "Português": ["Interpretação de Texto", "Sintaxe", "Crase e Pontuação"]
}

disciplina_escolhida = st.selectbox("1. Qual disciplina você estudou?", list(edital.keys()))

with st.form("registro_diario"):
    topico = st.selectbox("2. Qual tópico exato?", edital[disciplina_escolhida])
    
    # NOVIDADE: Dividindo o espaço em duas colunas para Horas e Minutos ficarem lado a lado
    col1, col2 = st.columns(2)
    with col1:
        horas = st.number_input("Tempo (Horas)", min_value=0, max_value=24)
    with col2:
        minutos = st.number_input("Tempo (Minutos)", min_value=0, max_value=59)
        
    questoes_feitas = st.number_input("Total de Questões", min_value=0)
    erros = st.number_input("Quantos erros?", min_value=0)
    
    salvar = st.form_submit_button("Salvar Estudo")

if salvar:
    acertos = questoes_feitas - erros
    
    st.session_state['historico'].append({
        "Disciplina": disciplina_escolhida,
        "Tópico": topico,
        "Horas": horas,       # Agora salvamos as horas
        "Minutos": minutos,   # e os minutos separadamente
        "Questões": questoes_feitas,
        "Acertos": acertos,
        "Erros": erros
    })
    st.success("Boa! Estudo registrado e salvo com sucesso.")

if len(st.session_state['historico']) > 0:
    st.divider()
    st.subheader("Seu Histórico de Estudos 📊")
    
    # Instrução visual para o usuário
    st.info("💡 Dica: Dê um duplo clique em qualquer número abaixo para editar. Para excluir uma linha inteira, selecione a caixinha à esquerda e clique na lixeira (ou aperte 'Delete' no teclado).")
    
    tabela = pd.DataFrame(st.session_state['historico'])
    
    # NOVIDADE: Usando o data_editor no lugar do dataframe. 
    # O num_rows="dynamic" é o que permite excluir (ou até adicionar) linhas!
    tabela_editada = st.data_editor(tabela, use_container_width=True, num_rows="dynamic")
    
    # A atualização da memória: o site "aprende" as alterações ou exclusões que você fez na tabela
    st.session_state['historico'] = tabela_editada.to_dict('records')
