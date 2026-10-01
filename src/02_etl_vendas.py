"""ETL: lê a raw_vendas, trata os dados e grava a camada tratada."""

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import criar_engine

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_SAIDA = RAIZ / "data" / "processed" / "vendas_tratadas.csv"

# Tradução dos nomes da raw (inglês) para a tratada (português)
RENOMEAR = {
    "invoice_id": "id_venda",
    "branch": "filial",
    "city": "cidade",
    "customer_type": "tipo_cliente",
    "gender": "genero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "quantidade",
    "tax_5_percent": "imposto",
    "sales": "valor_total",
    "sale_date": "data_venda",
    "sale_time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "avaliacao",
}

COLUNAS_TEXTO = [
    "id_venda", "filial", "cidade", "tipo_cliente",
    "genero", "linha_produto", "forma_pagamento",
]
COLUNAS_NUMERICAS = [
    "preco_unitario", "imposto", "valor_total", "custo_mercadoria",
    "margem_percentual", "receita_bruta", "avaliacao",
]

# Colunas que existem na tabela vendas_tratadas do banco
COLUNAS_TABELA = list(RENOMEAR.values())

DIAS_SEMANA = [
    "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo",
]


def extrair(engine):
    """Lê a tabela raw_vendas do banco."""
    return pd.read_sql("SELECT * FROM raw_vendas", engine)


def limpar_e_tipar(df):
    """Renomeia colunas, remove espaços e converte os tipos."""
    df = df.rename(columns=RENOMEAR)

    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.strip()

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna]).round(2)
    df["quantidade"] = pd.to_numeric(df["quantidade"]).astype(int)

    # O CSV usa o formato americano: mês/dia/ano e hora com AM/PM
    df["data_venda"] = pd.to_datetime(df["data_venda"], format="%m/%d/%Y")
    df["hora_venda"] = pd.to_datetime(df["hora_venda"], format="%I:%M:%S %p")
    return df


def verificar_qualidade(df):
    """Mostra ausentes e remove linhas duplicadas."""
    print("Valores ausentes por coluna:")
    print(df.isnull().sum())

    antes = len(df)
    df = df.dropna().drop_duplicates(subset="id_venda")
    print(f"\nLinhas removidas (ausentes ou duplicadas): {antes - len(df)}")
    return df


def criar_colunas_derivadas(df):
    """Cria colunas novas úteis para a análise."""
    df["mes"] = df["data_venda"].dt.strftime("%Y-%m")
    df["dia_semana"] = df["data_venda"].dt.dayofweek.map(
        lambda n: DIAS_SEMANA[n]
    )
    df["hora"] = df["hora_venda"].dt.hour
    df["periodo_dia"] = pd.cut(
        df["hora"],
        bins=[0, 12, 18, 24],
        labels=["manhã", "tarde", "noite"],
        right=False,
    )

    # Conferência: preço x quantidade + imposto deve dar o valor total
    calculado = df["preco_unitario"] * df["quantidade"] + df["imposto"]
    df["valor_total_confere"] = (calculado - df["valor_total"]).abs() < 0.05

    # Agora sim, separa data e hora nos tipos finais
    df["data_venda"] = df["data_venda"].dt.date
    df["hora_venda"] = df["hora_venda"].dt.time
    return df


def salvar_csv(df):
    """Grava a camada tratada em data/processed."""
    df.to_csv(CAMINHO_SAIDA, index=False)
    print(f"Arquivo salvo em: {CAMINHO_SAIDA}")


def carregar_tratada(df, engine):
    """Carrega as colunas da tabela vendas_tratadas no banco."""
    with engine.begin() as conexao:
        conexao.execute(text("TRUNCATE TABLE vendas_tratadas"))
    df[COLUNAS_TABELA].to_sql(
        "vendas_tratadas", engine, if_exists="append", index=False
    )
    print(f"{len(df)} linhas carregadas em vendas_tratadas.")


if __name__ == "__main__":
    motor = criar_engine()
    dados = extrair(motor)
    dados = limpar_e_tipar(dados)
    dados = verificar_qualidade(dados)
    dados = criar_colunas_derivadas(dados)

    print("\nTipos finais:")
    print(dados.dtypes)
    print("\nConferência do valor total:")
    print(dados["valor_total_confere"].value_counts())

    salvar_csv(dados)
    carregar_tratada(dados, motor)