import streamlit as st
import pandas as pd

st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

if 'editais' not in st.session_state:
    st.session_state['editais'] = {
        "Concurso Polícia": {
            "Direito Penal": ["Crimes contra a pessoa", "Crimes contra o patrimônio"],
            "Constitucional": ["Direitos Fundamentais"]
        },
        "Pós-Graduação": {
            "Módulo Básico": ["Física Aplicada", "Anatomia"]
        }
    }

# --- GAVETA DE GERENCIAMENTO ---
with st.expander("⚙️ Gerenciar Editais, Matérias e Tópicos"):
    st.subheader("1. Novo Edital / Projeto")
    novo_edital = st.text_input("Nome do novo edital:")
    if st.button("Criar Edital"):
        if novo_edital and novo_edital not in st.session_state['editais']:
            st.session_state['editais'][novo_edital] = {} 
            st.success(f"Edital '{novo_edital}' criado!")
            st.rerun()
            
    st.divider()
    
    col_mat, col_top = st.columns(2)
    with col_mat:
        st.subheader("2. Nova Matéria")
        edital_para_materia = st.selectbox("Em qual edital?", list(st.session_state['editais'].keys()), key="sel_mat")
        nova_materia = st.text_input("Nome da nova matéria:")
        if st.button("Adicionar Matéria"):
            if nova_materia and nova_materia not in st.session_state['editais'][edital_para_materia]:
                st.session_state['editais'][edital_para_materia][nova_materia] = []
                st.success("Matéria adicionada!")
                st.rerun()
                
    with col_top:
        st.subheader("3. Novo Tópico")
        edital_para_topico = st.selectbox("De qual edital?", list(st.session_state['editais'].keys()), key="sel_top")
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
            st.info("Crie uma matéria primeiro.")

st.divider()

# --- ÁREA DE REGISTRO DE ESTUDOS ---
st.subheader("📝 Registrar Estudo Diário")

edital_escolhido = st.selectbox("1. Qual Edital/Projeto você estudou hoje?", list(st.session_state['editais'].keys()))
materias_do_edital = list(st.session_state['editais'][edital_escolhido].keys())

if len(materias_do_edital) == 0:
    st.warning("⚠️ Você precisa cadastrar pelo menos uma matéria neste edital lá em cima para começar a registrar.")
else:
    disciplina_escolhida = st.selectbox("2. Qual disciplina?", materias_do_edital)
    topicos_disponiveis = st.session_state['editais'][edital_escolhido][disciplina_escolhida]
    
    if len(topicos_disponiveis) == 0:
        st.warning("⚠️ Você precisa cadastrar pelo menos um tópico nesta matéria lá em cima.")
    else:
        topico = st.selectbox("3. Qual tópico exato?", topicos_disponiveis)
        
        col1, col2 = st.columns(2)
        with col1:
            horas = st.number_input("Tempo (Horas)", min_value=0, max_value=24)
        with col2:
            minutos = st.number_input("Tempo (Minutos)", min_value=0, max_value=59)
            
        questoes_feitas = st.number_input("Total de Questões", min_value=0)
        erros = st.number_input("Quantos erros?", min_value=0)
        
        if st.button("Salvar Estudo", type="primary"):
            acertos = questoes_feitas - erros
            
            st.session_state['historico'].append({
                "Edital": edital_escolhido,
                "Disciplina": disciplina_escolhida,
                "Tópico": topico,
                "Horas": horas,
                "Minutos": minutos,
                "Questões": questoes_feitas,
                "Acertos": acertos,
                "Erros": erros
            })
            st.success("Boa! Estudo registrado e salvo com sucesso.")
            st.rerun()

# --- NOVIDADE: DASHBOARD DE DESEMPENHO E HISTÓRICO ---
if len(st.session_state['historico']) > 0:
    st.divider()
    
    # Transforma o histórico em uma tabela do Pandas para fazermos os cálculos
    df = pd.DataFrame(st.session_state['historico'])
    
    st.header("📈 Dashboard de Desempenho")
    
    # Filtra apenas os registros que tiveram questões (para evitar erro de divisão por zero caso você só leia a teoria)
    df_questoes = df[df['Questões'] > 0]
    
    if not df_questoes.empty:
        # Agrupa por disciplina e soma o total de questões e acertos
        resumo = df_questoes.groupby('Disciplina')[['Questões', 'Acertos']].sum().reset_index()
        resumo['Aproveitamento'] = (resumo['Acertos'] / resumo['Questões']) * 100
        
        # Mostra o desempenho de cada matéria com barras e alertas
        for index, row in resumo.iterrows():
            disciplina = row['Disciplina']
            taxa = row['Aproveitamento']
            
            col_nome, col_barra = st.columns([1, 2])
            with col_nome:
                st.write(f"**{disciplina}**")
                st.write(f"{row['Acertos']} / {row['Questões']} acertos")
            with col_barra:
                # O st.progress exige um número entre 0.0 e 1.0, por isso dividimos por 100
                st.progress(int(taxa) / 100)
                
            # Os alertas inteligentes baseados na porcentagem
            if taxa < 70:
                st.warning(f"🚨 **Alerta de Revisão:** Seu aproveitamento está em {taxa:.1f}%. Recomendamos focar mais em {disciplina}!")
            elif taxa >= 90:
                st.success(f"🏆 **Excelente!** Você está dominando {disciplina} com {taxa:.1f}% de acerto.")
            else:
                st.info(f"👍 **Bom desempenho!** Taxa de {taxa:.1f}% em {disciplina}. Continue assim.")
                
            st.write("---") # Linha para separar as matérias visualmente
    else:
        st.info("Faça registros com questões para ver suas estatísticas de acerto aqui.")

    st.subheader("Seu Histórico de Estudos 📊")
    st.caption("💡 Dica: Dê um duplo clique para editar. Para excluir, selecione a caixinha à esquerda e clique na lixeira.")
    
    tabela = df[["Edital", "Disciplina", "Tópico", "Horas", "Minutos", "Questões", "Acertos", "Erros"]]
    tabela_editada = st.data_editor(tabela, use_container_width=True, num_rows="dynamic")
    st.session_state['historico'] = tabela_editada.to_dict('records')
