# =======================================================
# Carga dos dados brutos do CSV na tabela raw_vendas.
# =======================================================

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import criar_engine

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ / "data" / "raw" / "supermarket_analysis.csv"

# Nomes das colunas da tabela raw_vendas

COLUNAS_RAW = [
    "invoice_id", "branch", "city", "customer_type", "gender",
    "product_line", "unit_price", "quantity", "tax_5_percent", "sales",
    "sale_date", "sale_time", "payment", "cogs",
    "gross_margin_percentage", "gross_income", "rating",
]


def ler_csv_bruto(caminho):
    # Lê o CSV com tudo como texto, sem alterar o conteúdo original
    df = pd.read_csv(caminho, encoding="utf-8-sig", dtype=str)
    df.columns = COLUNAS_RAW
    return df


def carregar_raw(df, engine):
    # Limpa a tabela raw_vendas e insere os dados do DataFrame
    with engine.begin() as conexao:
        # Evita duplicar os dados se o script for rodado mais de uma vez
        conexao.execute(text("TRUNCATE TABLE raw_vendas"))
    df.to_sql("raw_vendas", engine, if_exists="append", index=False)


if __name__ == "__main__":
    dados = ler_csv_bruto(CAMINHO_CSV)
    motor = criar_engine()
    carregar_raw(dados, motor)
    print(f"{len(dados)} linhas carregadas em raw_vendas.")