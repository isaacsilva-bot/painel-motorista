import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Consulta Local", page_icon="🚚")

# 2. Cabeçalho (Imagem como Banner)
st.image("logo.png", use_container_width=True)

# 3. Título do site
st.title("Consulta de Pacotes com Atraso de Recebimento no SOC")

# O código agora lê o arquivo que você subiu no GitHub
try:
    df = pd.read_csv("dados.csv")
    
    id_input = st.text_input("Digite seu ID:", placeholder="Ex: 1547109")

    if st.button("Consultar ID"):
        if id_input:
            # Garante que a coluna driver_id seja lida como texto
            df['driver_id'] = df['driver_id'].astype(str)
            busca = df[df['driver_id'] == str(id_input)].copy()

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                
                # Mensagem de Boas-vindas
                st.success(f"Olá, {nome}!")
                
                # Frase de instrução
                st.info("Caso a data de coleta seja próxima a data da sua pesquisa, aguarde 4 dias antes de pesquisar novamente. Os pacotes podem ser reconhecidos durante o passar dos dias e sairá desta lista.")
                
                # --- AJUSTE: ORDENAR POR DATA ---
                # Ascending=True para as mais antigas primeiro, False para as mais recentes
                busca = busca.sort_values(by='Data', ascending=True)

                # Métricas
                st.metric("Total de Pacotes", len(busca))
                
                st.write("### Pacotes não reconhecidos no SOC/HUB:")

                # --- AJUSTE: REMOVER NÚMEROS DE LINHA ---
                # Usamos st.dataframe com hide_index=True para uma tabela mais limpa
                st.dataframe(
                    busca[['loja', 'Código do Pacote', 'Data']], 
                    hide_index=True, 
                    use_container_width=True
                )
            else:
                st.error("Você não possui pacotes em falta até o momento. Aguarde a próxima atualização. Atualizações quarta-feira e sexta-feira")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error("Erro: O arquivo 'dados.csv' não foi encontrado no GitHub ou as colunas estão incorretas.")
