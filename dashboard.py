import streamlit as st
import pandas as pd
import plotly.express as px

# Título do dashboard
st.title("📊 Dashboard Sensorial")

# Upload de ficheiro
file = st.file_uploader("Carregue o ficheiro CSV", type=["csv"])

if file is not None:
    try:
        # Tente carregar o arquivo CSV com delimitador ';'
        df = pd.read_csv(file, encoding="ISO-8859-1", delimiter=';', on_bad_lines='skip')
        st.subheader("Pré-visualização dos dados")
        st.dataframe(df.head())

        # Verifique se o DataFrame tem pelo menos 3 colunas
        if len(df.columns) >= 3:
            # Renomeie as colunas para 'Categoria', 'Produto' e 'Média'
            df.columns = ['Categoria', 'Produto', 'Média']

            # Filtros
            if 'Categoria' in df.columns:
                Categoria = st.selectbox("Selecione a Categoria", df['Categoria'].unique())
                df_filtrado = df[df['Categoria'] == Categoria]

                # Gráfico
                st.subheader(f"Médias por produto - Categoria: {Categoria}")
                fig = px.bar(df_filtrado, x='Produto', y='Média', color='Produto', title="Médias por Produto")
                st.plotly_chart(fig)

                # Tabela final
                st.subheader("Dados filtrados")
                st.dataframe(df_filtrado)

                # Ranking dos artigos com as melhores médias
                st.subheader("Ranking dos artigos com as melhores médias")
                ranking = df_filtrado.sort_values(by='Média', ascending=False)
                st.dataframe(ranking)
            else:
                st.error("A coluna 'Categoria' não existe no DataFrame.")
        else:
            st.error(f"O ficheiro CSV não contém colunas suficientes. Esperado: 3, Encontrado: {len(df.columns)}")
            st.write("Primeiras linhas do DataFrame:", df.head())
    except pd.errors.EmptyDataError:
        st.error("O ficheiro CSV está vazio.")
    except pd.errors.ParserError as e:
        st.error(f"Erro ao analisar o ficheiro CSV: {e}")
    except Exception as e:
        st.error(f"Erro ao carregar o ficheiro CSV: {e}")
else:
    st.info("💡 Carregue um ficheiro CSV com as colunas: Categoria, Produto, Média")