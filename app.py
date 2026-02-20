import streamlit as st
import pandas as pd

# Configuração visual
st.set_page_config(page_title="Consulta Motorista", page_icon="🚚")

st.title("🚚 Painel do Motorista")

# Link da sua planilha (Já configurado para leitura direta)
URL = "https://docs.google.com/spreadsheets/d/1n5_9PPwvgS3PAaUXPiOZymz8TTkLhEBTsDmxdxc6vYU/export?format=csv"

try:
    # Carrega os dados
    df = pd.read_csv(URL)
    
    id_input = st.text_input("Digite seu ID de Motorista:", placeholder="Ex: 15471")

    if st.button("Consultar"):
        if id_input:
            # Garante que o ID seja texto
            df['driver_id'] = df['driver_id'].astype(str)
            busca = df[df['driver_id'] == str(id_input)]

            if not busca.empty:
                nome = busca.iloc[0]['Motorista']
                st.success(f"Olá, {nome}!")
                
                # Exibe as métricas
                total_pacotes = len(busca)
                st.metric("Total de Pacotes", total_pacotes)
                
                st.write("### Suas Entregas:")
                st.table(busca[['loja', 'Código do Pacote']])
            else:
                st.error("ID não encontrado. Verifique se o número está correto.")
        else:
            st.warning("Por favor, digite um ID.")

except Exception as e:
    st.error("Erro ao conectar com a planilha.")
    st.info("Dica: Verifique se a planilha está 'Aberta para qualquer pessoa com o link'.")
