
# ====================================================
# Leitura e inspeção inicial do CSV de vendas
# ====================================================

from pathlib import Path

import pandas as pd

# Caminho do CSV
RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ / "data" / "raw" / "supermarket_analysis.csv"


def ler_csv(caminho):
    """Lê o CSV e devolve um DataFrame."""
    # utf-8-sig remove um caractere invisível que o arquivo tem 
    return pd.read_csv(caminho, encoding="utf-8-sig")


def inspecionar(df):
    """Mostra informações básicas para conhecermos os dados."""
    print("=== Formato (linhas, colunas) ===")
    print(df.shape)

    print("\n=== Primeiras 5 linhas ===")
    print(df.head())

    print("\n=== Colunas e tipos ===")
    print(df.dtypes)

    print("\n=== Valores ausentes por coluna ===")
    print(df.isnull().sum())

    print("\n=== Linhas duplicadas ===")
    print(df.duplicated().sum())


if __name__ == "__main__":
    dados = ler_csv(CAMINHO_CSV)
    inspecionar(dados)