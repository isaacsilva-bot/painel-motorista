import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta Local", page_icon="🚚")

st.title("🚚 Consulta de Stuck - Motorista RJ")

# O código agora lê o arquivo que você subiu no GitHub
try:
    df = pd.read_csv("dados.csv")
    
    id_input = st.text_input("Digite seu ID:", placeholder="Ex: 15471")

    if st.button("Consultar"):
        if id_input:
            # Garante que a coluna driver_id seja lida como texto
            df['driver_id'] = df['driver_id'].astype(str)
            busca = df[df['driver_id'] == str(id_input)]

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                st.success(f"Olá, {nome}!")
                st.metric("Total de Pacotes", len(busca))
                st.write("### Suas Entregas:")
                st.table(busca[['loja', 'Código do Pacote']])
            else:
                st.error("ID não encontrado no arquivo atual.")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error("Erro: O arquivo 'dados.csv' não foi encontrado no GitHub.")
