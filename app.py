import streamlit as st
import pandas as pd
import json
import os

st.title("Acompanhamento de Estudos 📚")
st.write("Bem-vindo ao seu painel de controle de estudos!")

# --- NOVIDADE: FUNÇÕES PARA SALVAR E LER OS DADOS REAIS ---
# 1. Carregar Editais Salvos
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

# 2. Carregar Histórico Salvo
if os.path.exists("meu_historico.csv"):
    df_salvo = pd.read_csv("meu_historico.csv")
    st.session_state['historico'] = df_salvo.to_dict('records')
else:
    if 'historico' not in st.session_state:
        st.session_state['historico'] = []

# 3. Função Mágica para gravar no arquivo toda vez que houver mudança
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
            gravar_arquivos() # Salva no arquivo!
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
                gravar_arquivos() # Salva no arquivo!
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
                    gravar_arquivos() # Salva no arquivo!
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
            
            gravar_arquivos() # Salva no arquivo!
            
            st.success("Boa! Estudo registrado e salvo com sucesso.")
            st.rerun()

# --- DASHBOARD DE DESEMPENHO E HISTÓRICO ---
if len(st.session_state['historico']) > 0:
    st.divider()
    df = pd.DataFrame(st.session_state['historico'])
    
    st.header("📈 Dashboard de Desempenho")
    df_questoes = df[df['Questões'] > 0]
    
    if not df_questoes.empty:
        resumo = df_questoes.groupby('Disciplina')[['Questões', 'Acertos']].sum().reset_index()
        resumo['Aproveitamento'] = (resumo['Acertos'] / resumo['Questões']) * 100
        
        for index, row in resumo.iterrows():
            disciplina = row['Disciplina']
            taxa = row['Aproveitamento']
            
            col_nome, col_barra = st.columns([1, 2])
            with col_nome:
                st.write(f"**{disciplina}**")
                st.write(f"{row['Acertos']} / {row['Questões']} acertos")
            with col_barra:
                st.progress(min(int(taxa) / 100, 1.0)) # Trava para a barra não passar de 100%
                
            if taxa < 70:
                st.warning(f"🚨 **Alerta:** Seu aproveitamento está em {taxa:.1f}%. Recomendamos revisar {disciplina}!")
            elif taxa >= 90:
                st.success(f"🏆 **Excelente!** Dominando com {taxa:.1f}%.")
            else:
                st.info(f"👍 **Bom!** Taxa de {taxa:.1f}%.")
            st.write("---")

    st.subheader("Seu Histórico de Estudos 📊")
    st.caption("💡 Para excluir, apague os dados da linha na tabela.")
    
    tabela = df[["Edital", "Disciplina", "Tópico", "Horas", "Minutos", "Questões", "Acertos", "Erros"]]
    tabela_editada = st.data_editor(tabela, use_container_width=True, num_rows="dynamic")
    
    # Se a tabela for editada manualmente pelo usuário, salva as mudanças!
    if tabela_editada.to_dict('records') != st.session_state['historico']:
        st.session_state['historico'] = tabela_editada.to_dict('records')
        gravar_arquivos()
        st.rerun()
