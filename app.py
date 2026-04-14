import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Consulta SOC", page_icon="🚚", layout="centered")

# 2. CSS Customizado
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO GOOGLE SHEETS ---
# Novo link atualizado conforme solicitado
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLptCJKIUDiCVR440Z6ZaJxzvRB1WJeCV36OJfnTQ2nBLECWjlZOqslbedcybCY-4cUQSDmNOCEx0U/pub?gid=1766127596&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    # Lendo os dados e forçando a remoção de espaços nos nomes das colunas
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# 3. Cabeçalho (Banner)
try:
    st.image("logo.png", use_container_width=True)
except:
    st.warning("Arquivo logo.png não encontrado no repositório.")

st.title("Consulta de Pacotes com Atraso de Recebimento no SOC")

# 4. Lógica de carregamento e busca
try:
    df = load_data(SHEET_URL)
    
    id_input = st.text_input("Digite seu ID:", placeholder="Ex: 1547109")

    if st.button("Consultar ID"):
        if id_input:
            # Tratamento rigoroso: converte ID para string, remove espaços e garante comparação limpa
            df['driver_id'] = df['driver_id'].astype(str).str.strip()
            id_input_str = str(id_input).strip()
            
            # Filtra os dados
            busca = df[df['driver_id'] == id_input_str].copy()

            if not busca.empty:
                # Busca o nome na coluna 'Motorista' removendo espaços extras
                nome = str(busca.iloc[0]['Motorista']).strip()
                
                st.success(f"Olá, {nome}!")
                st.info("Caso a data de coleta seja próxima a data da sua pesquisa, aguarde 4 dias antes de pesquisar novamente.")
                
                # Tratamento de Data
                busca['Data'] = pd.to_datetime(busca['Data'], errors='coerce')
                busca = busca.sort_values(by='Data', ascending=True)

                st.metric("Total de Pacotes", len(busca))
                st.write("### Pacotes não reconhecidos no SOC/HUB:")

                # Exibição da tabela
                st.dataframe(
                    busca[['loja', 'Código do Pacote', 'Data']], 
                    hide_index=True, 
                    use_container_width=True
                )
            else:
                st.error("Você não possui pacotes em falta até o momento.")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    # Exibe o erro real para ajudar no diagnóstico se algo falhar
    st.error(f"Erro ao processar dados: {e}")
    st.info("Certifique-se que as colunas 'driver_id' e 'Motorista' existem na planilha.")
