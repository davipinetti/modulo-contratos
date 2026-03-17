import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Gestão de Contratos Compet", layout="wide")

st.title("📊 Dashboard Inteligente de Contratos")
st.markdown("---")

# Carregamento do Arquivo
uploaded_file = st.sidebar.file_uploader("📂 Selecione sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Filtros na lateral
    st.sidebar.header("Filtros")
    lista_localidade = st.sidebar.multiselect("Localidade", options=df['Localidade'].unique())
    
    df_f = df.copy()
    if lista_localidade:
        df_f = df_f[df_f['Localidade'].isin(lista_localidade)]

    # 1. ALERTAS DE 30 DIAS
    st.subheader("⚠️ Alertas de Atenção")
    criticos = df_f[df_f['Tempo Restante (dias)'] < 30]
    
    if not criticos.empty:
        for index, row in criticos.iterrows():
            st.error(f"**ALERTA:** O contrato **{row['Nome']}** vence em **{row['Tempo Restante (dias)']} dias**!")
    else:
        st.success("✅ Prazos em dia.")

    # 2. PROJEÇÃO DE SALDO E DASHBOARD
    col1, col2, col3 = st.columns(3)
    col1.metric("Valor Total", f"R$ {df_f['Valor do Contrato'].sum():,.2f}")
    col2.metric("Saldo Atual", f"R$ {df_f['Saldo do Contrato'].sum():,.2f}")
    
    proj_media = df_f['Projeção de Saldo (meses)'].mean()
    col3.metric("Fôlego Médio", f"{proj_media:.1f} meses")

    st.subheader("⏳ Projeção de Duração do Saldo (Meses)")
    fig_proj = px.bar(df_f, x='Nome', y='Projeção de Saldo (meses)', color='Projeção de Saldo (meses)', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_proj, use_container_width=True)

    st.subheader("📋 Detalhes")
    st.dataframe(df_f)

else:
    st.info("💡 Carregue sua planilha para ver os alertas e projeções.")
