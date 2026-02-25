import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Consulta Local", page_icon="🚚")

# 2. Cabeçalho (Imagem como Banner)
# O arquivo logo.png deve estar na mesma pasta no GitHub
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
            busca = df[df['driver_id'] == str(id_input)]

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                
                # Mensagem de Boas-vindas
                st.success(f"Olá, {nome}!")
                
                # Frase de instrução em uma linha separada (caixa azul informativa)
                st.info("Caso a data da coleta esteja próxima à data da sua pesquisa, aguarde 4 dias antes de realizar uma nova consulta. Os pacotes podem ser reconhecidos ao longo dos dias e, consequentemente, deixarão de constar nesta lista.")
                
                # Métricas e Tabela
                st.metric("Total de Pacotes", len(busca))
                st.write("### Pacotes não reconhecidos no SOC/HUB:")
                st.table(busca[['loja', 'Código do Pacote', 'Data']])
            else:
                # Mensagem caso não encontre o ID
                st.error("Você não possui pacotes em falta até o momento. Aguarde a próxima atualização. Atualizações quarta-feira e sexta-feira")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error("Erro: O arquivo 'dados.csv' não foi encontrado no GitHub.")
