import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

# carregar as bases de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

# Merge
df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

# Criando coluna de Custo
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
# Criando a coluna de lucro
df["Lucro"] = df["Valor Venda"] - df["Custo"]
# Criando uma coluna de mês-ano
df["mes-ano"] = df["Data Venda"].dt.to_period("M")
df['mes-ano'] = df['mes-ano'].astype(str)


produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()
lucro_mes_categoria = df.groupby(["mes-ano","Categoria"])["Lucro"].sum().reset_index()

def main():

    st.title("Análise de Vendas")
    st.image("vendas.jpg")

    total_custo = (df["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5]+ "." + total_custo[5:8]
    
    total_lucro = (df["Lucro"].sum()).astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] + "." + total_lucro[2:5]+ "." + total_lucro[5:8]


    total_clientes = df["ID Cliente"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Custo Total",total_custo)

    with col2:
        st.metric("Lucro Total",total_lucro)

    with col3:
        st.metric("Total de Clientes Únicos",total_clientes)

    col1, col2 = st.columns(2)

    fig1 = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca" , orientation="h",
                 title="Total produtos vendidos por Marca", text="Quantidade",
                 width=450,height=400)
    col1.plotly_chart(fig1)

    fig2 = px.pie(lucro_categoria, values="Lucro", names="Categoria" , 
                 title="Lucro por Categoria",width=450,height=400)
    col2.plotly_chart(fig2)


    fig3 = px.line(lucro_mes_categoria, x="mes-ano", y="Lucro",
                   title="Lucro", color="Categoria")
    st.plotly_chart(fig3)


if __name__ == "__main__":
    main()

