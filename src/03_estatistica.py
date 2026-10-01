"""Estatística descritiva, respostas de negócio e gráficos."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_DADOS = RAIZ / "data" / "processed" / "vendas_tratadas.csv"
PASTA_RESULTADOS = RAIZ / "resultados"

COR = "#4C72B0"
DIAS_ORDEM = [
    "segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo",
]


def formatar(valor):
    """Formata número no padrão brasileiro: 110.568,71."""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados():
    """Lê a camada tratada."""
    return pd.read_csv(CAMINHO_DADOS, parse_dates=["data_venda"])


def estatistica_descritiva(df):
    """Calcula e salva as estatísticas das colunas numéricas."""
    colunas = ["preco_unitario", "quantidade", "valor_total", "avaliacao"]
    resumo = df[colunas].describe().round(2)
    resumo.to_csv(PASTA_RESULTADOS / "estatistica_descritiva.csv")
    print("=== Estatística descritiva ===")
    print(resumo)
    return resumo


def responder_perguntas(df):
    """Responde às 8 perguntas de negócio e salva em um arquivo de texto."""
    filial_valor = (
        df.groupby(["filial", "cidade"])["valor_total"].sum().round(2)
    )
    filial_qtd = df.groupby(["filial", "cidade"]).size()
    linha_valor = df.groupby("linha_produto")["valor_total"].sum().round(2)
    linha_nota = df.groupby("linha_produto")["avaliacao"].mean().round(2)
    pagamento = df["forma_pagamento"].value_counts()
    dia = df.groupby("dia_semana").size().reindex(DIAS_ORDEM)
    maior = df.loc[df["valor_total"].idxmax()]

    top_valor = filial_valor.idxmax()
    top_qtd = filial_qtd.idxmax()

    linhas = [
        "RESPOSTAS DE NEGÓCIO",
        "(valores sem símbolo: o dataset não informa a moeda)",
        "",
        f"1. Filial com maior faturamento: {top_valor[0]} ({top_valor[1]}) "
        f"com {formatar(filial_valor.max())}",
        f"2. Filial com maior quantidade de vendas: {top_qtd[0]} "
        f"({top_qtd[1]}) com {filial_qtd.max()} vendas",
        f"3. Linha de produto com maior faturamento: "
        f"{linha_valor.idxmax()} com {formatar(linha_valor.max())}",
        f"4. Linha de produto com melhor avaliação média: "
        f"{linha_nota.idxmax()} com nota {linha_nota.max():.2f}",
        f"5. Forma de pagamento mais utilizada: {pagamento.idxmax()} "
        f"com {pagamento.max()} vendas",
        f"6. Valor médio das vendas: {formatar(df['valor_total'].mean())}",
        f"7. Maior venda registrada: {formatar(maior['valor_total'])} "
        f"(venda {maior['id_venda']}, filial {maior['filial']}, "
        f"{maior['linha_produto']}, "
        f"{maior['data_venda'].strftime('%d/%m/%Y')})",
        f"8. Dia da semana com mais vendas: {dia.idxmax()} "
        f"({dia.max()} vendas)",
        "",
        "INFORMAÇÕES COMPLEMENTARES",
        "",
        "Faturamento por filial:",
        filial_valor.to_string(),
        "",
        "Quantidade de vendas por filial:",
        filial_qtd.to_string(),
        "",
        "Avaliação média por linha de produto:",
        linha_nota.sort_values(ascending=False).to_string(),
        "",
        f"Avaliação média geral: {df['avaliacao'].mean():.2f}",
        "Avaliação média por filial:",
        df.groupby("filial")["avaliacao"].mean().round(2).to_string(),
        "",
        f"Mês com mais vendas: {df.groupby('mes').size().idxmax()}",
        f"Hora com mais vendas: {df.groupby('hora').size().idxmax()}h",
    ]
    texto = "\n".join(linhas)
    print("\n" + texto)
    caminho = PASTA_RESULTADOS / "respostas_negocio.txt"
    caminho.write_text(texto, encoding="utf-8")


def salvar_grafico(arquivo):
    """Ajusta o layout, salva o gráfico em resultados/ e fecha a figura."""
    plt.tight_layout()
    plt.savefig(PASTA_RESULTADOS / arquivo, dpi=150)
    plt.close()


def grafico_barras(dados, x, y, titulo, arquivo):
    """Cria e salva um gráfico de barras."""
    plt.figure(figsize=(9, 5))
    sns.barplot(data=dados, x=x, y=y, color=COR)
    plt.title(titulo)
    plt.xticks(rotation=25, ha="right")
    salvar_grafico(arquivo)


def gerar_graficos(df):
    """Gera todos os gráficos do projeto."""
    sns.set_theme(style="whitegrid")

    faturamento_filial = (
        df.groupby("filial")["valor_total"].sum().reset_index()
    )
    grafico_barras(
        faturamento_filial, "filial", "valor_total",
        "Faturamento por filial", "01_faturamento_filial.png",
    )

    faturamento_categoria = (
        df.groupby("linha_produto")["valor_total"].sum()
        .sort_values(ascending=False).reset_index()
    )
    grafico_barras(
        faturamento_categoria, "linha_produto", "valor_total",
        "Faturamento por categoria", "02_faturamento_categoria.png",
    )

    pagamentos = (
        df.groupby("forma_pagamento").size().reset_index(name="vendas")
    )
    grafico_barras(
        pagamentos, "forma_pagamento", "vendas",
        "Vendas por forma de pagamento", "03_formas_pagamento.png",
    )

    vendas_mes = df.groupby("mes").size().reset_index(name="vendas")
    grafico_barras(
        vendas_mes, "mes", "vendas",
        "Quantidade de vendas por mês", "04_vendas_mes.png",
    )

    vendas_hora = df.groupby("hora").size().reset_index(name="vendas")
    grafico_barras(
        vendas_hora, "hora", "vendas",
        "Quantidade de vendas por hora do dia", "05_vendas_hora.png",
    )

    avaliacao = df.groupby("filial")["avaliacao"].mean().reset_index()
    grafico_barras(
        avaliacao, "filial", "avaliacao",
        "Avaliação média por filial", "06_avaliacao_filial.png",
    )

    plt.figure(figsize=(9, 5))
    sns.histplot(df["valor_total"], bins=20, color=COR)
    plt.title("Distribuição do valor total das vendas")
    salvar_grafico("07_distribuicao_valor_total.png")


if __name__ == "__main__":
    PASTA_RESULTADOS.mkdir(exist_ok=True)
    dados = carregar_dados()
    estatistica_descritiva(dados)
    responder_perguntas(dados)
    gerar_graficos(dados)
    print(f"\nArquivos salvos em: {PASTA_RESULTADOS}")