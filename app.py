import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Consulta SOC", page_icon="🚚", layout="centered")

# 2. CSS Customizado para esconder menus desnecessários
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO GOOGLE SHEETS ---
# Seu link direto para o CSV da planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLptCJKIUDiCVR440Z6ZaJxzvRB1WJeCV36OJfnTQ2nBLECWjlZOqslbedcybCY-4cUQSDmNOCEx0U/pub?gid=1766127596&single=true&output=csv"

@st.cache_data(ttl=60) # Atualiza os dados a cada 1 minuto
def load_data(url):
    # Lendo os dados diretamente do Google Sheets
    return pd.read_csv(url)

# 3. Cabeçalho (Banner)
# O arquivo "logo.png" deve estar na mesma pasta que este script no seu repositório
try:
    st.image("logo.png", use_container_width=True)
except:
    st.warning("Arquivo logo.png não encontrado no repositório.")

# 4. Título do site
st.title("Consulta de Pacotes com Atraso de Recebimento no SOC")

# 5. Lógica de carregamento e busca
try:
    # Carregando os dados da nuvem
    df = load_data(SHEET_URL)
    
    id_input = st.text_input("Digite seu ID:", placeholder="Ex: 1547109")

    if st.button("Consultar ID"):
        if id_input:
            # Garante que a coluna driver_id seja tratada como texto
            # Certifique-se que o nome da coluna na planilha é exatamente 'driver_id'
            df['driver_id'] = df['driver_id'].astype(str)
            
            # Limpa espaços extras que podem vir da planilha
            id_input_str = str(id_input).strip()
            busca = df[df['driver_id'].str.strip() == id_input_str].copy()

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                
                # Mensagem de Boas-vindas
                st.success(f"Olá, {nome}!")
                
                # Instrução importante
                st.info("Caso a data de coleta seja próxima a data da sua pesquisa, aguarde 4 dias antes de pesquisar novamente. Os pacotes podem ser reconhecidos durante o passar dos dias e sairá desta lista.")
                
                # Ordenação por Data (Mais antigas primeiro)
                # O pandas tentará converter a coluna 'Data' automaticamente
                busca['Data'] = pd.to_datetime(busca['Data'], errors='ignore')
                busca = busca.sort_values(by='Data', ascending=True)

                # Métrica de pacotes encontrados
                st.metric("Total de Pacotes", len(busca))
                
                st.write("### Pacotes não reconhecidos no SOC/HUB:")

                # Exibição da tabela formatada
                st.dataframe(
                    busca[['loja', 'Código do Pacote', 'Data']], 
                    hide_index=True, 
                    use_container_width=True
                )
            else:
                # Mensagem caso o ID não tenha pendências
                st.error("Você não possui pacotes em falta até o momento. Aguarde a próxima atualização. Atualizações quarta-feira e sexta-feira")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Verifique se as colunas na sua planilha são exatamente: driver_id, Motorista, loja, Código do Pacote, Data")
