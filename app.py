import streamlit as st
import pandas as pd
import json
import os

st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

# --- FUNÇÕES PARA SALVAR E LER OS DADOS REAIS ---
if os.path.exists("meus_editais.json"):
    with open("meus_editais.json", "r") as f:
        st.session_state['editais'] = json.load(f)
else:
    if 'editais' not in st.session_state:
        st.session_state['editais'] = {
            "Concurso Polícia": {
                "Direito Penal": ["Crimes contra a pessoa", "Crimes contra o patrimônio"]
            }
        }

if os.path.exists("meu_historico.csv"):
    df_salvo = pd.read_csv("meu_historico.csv")
    st.session_state['historico'] = df_salvo.to_dict('records')
else:
    if 'historico' not in st.session_state:
        st.session_state['historico'] = []

def gravar_arquivos():
    with open("meus_editais.json", "w") as f:
        json.dump(st.session_state['editais'], f)
    pd.DataFrame(st.session_state['historico']).to_csv("meu_historico.csv", index=False)

# --- GAVETA DE GERENCIAMENTO ---
with st.expander("⚙️ Gerenciar Editais, Matérias e Tópicos"):
    st.subheader("1. Novo Edital / Projeto")
    novo_edital = st.text_input("Nome do novo edital:")
    if st.button("Criar Edital"):
        if novo_edital and novo_edital not in st.session_state['editais']:
            st.session_state['editais'][novo_edital] = {} 
            gravar_arquivos()
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
                gravar_arquivos()
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
                    gravar_arquivos()
                    st.success("Tópico adicionado!")
                    st.rerun()
        else:
            st.info("Crie uma matéria primeiro.")

st.divider()

# --- ÁREA DE REGISTRO DE ESTUDOS ---
st.subheader("📝 Registrar Estudo Diário")

# Esta variável agora é a "chave" que controla o que aparece no resto do site!
edital_escolhido = st.selectbox("1. Qual Edital/Projeto você estudou hoje?", list(st.session_state['editais'].keys()))
materias_do_edital = list(st.session_state['editais'][edital_escolhido].keys())

if len(materias_do_edital) == 0:
    st.warning("⚠️ Você precisa cadastrar pelo menos uma matéria neste edital.")
else:
    disciplina_escolhida = st.selectbox("2. Qual disciplina?", materias_do_edital)
    topicos_disponiveis = st.session_state['editais'][edital_escolhido][disciplina_escolhida]
    
    if len(topicos_disponiveis) == 0:
        st.warning("⚠️ Você precisa cadastrar pelo menos um tópico nesta matéria.")
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
            
            gravar_arquivos()
            st.success("Boa! Estudo registrado e salvo com sucesso.")
            st.rerun()

# --- NOVIDADE: DASHBOARD FILTRADO ---
if len(st.session_state['historico']) > 0:
    st.divider()
    
    # Pega o histórico todo
    df_completo = pd.DataFrame(st.session_state['historico'])
    
    # MÁGICA DO FILTRO: Cria uma tabela só com o edital que está selecionado na caixa 1
    df_filtrado = df_completo[df_completo['Edital'] == edital_escolhido]
    
    # Só mostra o dashboard se tiver dados PARA ESTE EDITAL
    if not df_filtrado.empty:
        st.header(f"📈 Dashboard: {edital_escolhido}")
        
        # O dashboard agora usa a tabela filtrada (df_filtrado) em vez da completa
        df_questoes = df_filtrado[df_filtrado['Questões'] > 0]
        
        if not df_questoes.empty:
            resumo_disciplina = df_questoes.groupby('Disciplina')[['Questões', 'Acertos']].sum().reset_index()
            
            for index, row in resumo_disciplina.iterrows():
                disciplina = row['Disciplina']
                taxa_geral = (row['Acertos'] / row['Questões']) * 100
                
                st.subheader(f"📚 {disciplina} (Geral: {taxa_geral:.1f}%)")
                st.progress(min(int(taxa_geral) / 100, 1.0))
                
                with st.expander(f"Ver desempenho por assuntos de {disciplina}"):
                    df_desta_disciplina = df_questoes[df_questoes['Disciplina'] == disciplina]
                    resumo_topico = df_desta_disciplina.groupby('Tópico')[['Questões', 'Acertos']].sum().reset_index()
                    
                    for t_index, t_row in resumo_topico.iterrows():
                        topico = t_row['Tópico']
                        taxa_topico = (t_row['Acertos'] / t_row['Questões']) * 100
                        
                        st.markdown(f"**{topico}**: {t_row['Acertos']}/{t_row['Questões']} acertos ({taxa_topico:.1f}%)")
                        st.progress(min(int(taxa_topico) / 100, 1.0))
                        
                        if taxa_topico < 70:
                            st.warning(f"🚨 Foco de Revisão: {topico}")
                st.write("---")

        st.subheader(f"Histórico de {edital_escolhido} 📊")
        
        tabela_visual = df_filtrado[["Edital", "Disciplina", "Tópico", "Horas", "Minutos", "Questões", "Acertos", "Erros"]]
        tabela_editada = st.data_editor(tabela_visual, use_container_width=True, num_rows="dynamic", key="editor_historico")
        
        # Trava de segurança para edição do histórico filtrado
        if tabela_editada.to_dict('records') != tabela_visual.to_dict('records'):
            # Guarda os dados dos OUTROS editais
            historico_outros = [item for item in st.session_state['historico'] if item['Edital'] != edital_escolhido]
            # Junta com a tabela deste edital que você acabou de editar/excluir
            st.session_state['historico'] = historico_outros + tabela_editada.to_dict('records')
            gravar_arquivos()
            st.rerun()
            
    else:
        st.info(f"Nenhum estudo registrado para '{edital_escolhido}' ainda. Comece preenchendo o formulário acima!")
