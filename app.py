import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta Local", page_icon="🚚")

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
                st.success(f"Olá, {nome}!")
                st.metric("Total de Pacotes", len(busca))
                st.write("### Suas Entregas:")
                st.table(busca[['loja', 'Código do Pacote', 'Data']])
            else:
                st.error("Você não possui pacotes em falta até o momento. Aguarde a próxima atualização. Atualizações quarta-feira e sexta-feira")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error("Erro: O arquivo 'dados.csv' não foi encontrado no GitHub.")
