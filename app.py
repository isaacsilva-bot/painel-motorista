import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Consulta Local", page_icon="🚚", layout="centered")

# 2. Comando para esconder o menu, o rodapé e o seu nome (CSS Customizado)
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Remove o espaço em branco extra no topo */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# 3. Cabeçalho (Imagem como Banner)
# Certifique-se de que o arquivo no GitHub se chama exatamente: logo.png
st.image("logo.png", use_container_width=True)

# 4. Título do site
st.title("Consulta de Pacotes com Atraso de Recebimento no SOC")

# 5. Lógica de carregamento e busca
try:
    # Lendo o arquivo CSV que você sobe manualmente
    df = pd.read_csv("dados.csv")
    
    id_input = st.text_input("Digite seu ID:", placeholder="Ex: 1547109")

    if st.button("Consultar ID"):
        if id_input:
            # Garante que a coluna driver_id seja tratada como texto para evitar erros
            df['driver_id'] = df['driver_id'].astype(str)
            busca = df[df['driver_id'] == str(id_input)].copy()

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                
                # Mensagem de Boas-vindas
                st.success(f"Olá, {nome}!")
                
                # Instrução importante em linha separada
                st.info("Caso a data de coleta seja próxima a data da sua pesquisa, aguarde 4 dias antes de pesquisar novamente. Os pacotes podem ser reconhecidos durante o passar dos dias e sairá desta lista.")
                
                # Ordenação por Data (Mais antigas primeiro)
                busca = busca.sort_values(by='Data', ascending=True)

                # Métrica de pacotes encontrados
                st.metric("Total de Pacotes", len(busca))
                
                st.write("### Pacotes não reconhecidos no SOC/HUB:")

                # Exibição da tabela limpa (sem números de linha à esquerda)
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
    st.error("Erro técnico: O arquivo 'dados.csv' não foi encontrado ou as colunas não batem.")
    st.info("Verifique se as colunas no seu CSV são exatamente: driver_id, Motorista, loja, Código do Pacote, Data")
