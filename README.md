# Análise de Vendas de Supermercado

Pipeline introdutório de dados com **PostgreSQL, SQL, Python e Pandas**, inspirado na Arquitetura Medallion (camadas Raw, Tratada e Resultados).

## Sumário

1. [Sobre o projeto](#1-sobre-o-projeto)
2. [Tecnologias](#2-tecnologias)
3. [Arquitetura](#3-arquitetura)
4. [Estrutura de pastas](#4-estrutura-de-pastas)
5. [Como executar](#5-como-executar)
   - [5.1 Pré-requisitos](#51-pré-requisitos)
   - [5.2 Clonar e criar o ambiente virtual](#52-clonar-e-criar-o-ambiente-virtual)
   - [5.3 Configurar as credenciais](#53-configurar-as-credenciais)
   - [5.4 Criar o banco e as tabelas](#54-criar-o-banco-e-as-tabelas)
   - [5.5 Colocar o CSV original](#55-colocar-o-csv-original)
   - [5.6 Rodar o pipeline](#56-rodar-o-pipeline)
6. [Fases do projeto](#6-fases-do-projeto)
7. [Dicionário de dados](#7-dicionário-de-dados)
8. [Principais resultados](#8-principais-resultados)
9. [Boas práticas](#9-boas-práticas)
10. [Autora](#10-autora)

---

## 1. Sobre o projeto

Uma rede de supermercados quer entender o desempenho de suas filiais a partir dos registros de vendas. Este projeto organiza os dados brutos em um banco PostgreSQL, faz consultas SQL, trata os dados com Pandas e responde perguntas de negócio com estatística descritiva e gráficos.

**Fonte dos dados:** dataset público *Supermarket Sales* (Kaggle), com 1.000 vendas de 3 filiais, entre 01/01/2019 e 30/03/2019.

[↑ Voltar ao sumário](#sumário)

## 2. Tecnologias

- PostgreSQL e DBeaver
- Python 3
- Pandas, SQLAlchemy, psycopg2 e python-dotenv
- Matplotlib e Seaborn
- Git e GitHub

[↑ Voltar ao sumário](#sumário)

## 3. Arquitetura

```
CSV original → raw_vendas → (Pandas: limpeza e tipagem) → vendas_tratadas → resultados
```

| Camada      | O que é                                         | Onde fica                                       |
| ----------- | ------------------------------------------------ | ----------------------------------------------- |
| Raw (bruta) | Cópia fiel do CSV, tudo como texto              | Tabela`raw_vendas` e `data/raw/`            |
| Tratada     | Dados limpos, tipados e com colunas derivadas    | Tabela`vendas_tratadas` e `data/processed/` |
| Resultados  | Estatísticas, respostas de negócio e gráficos | `resultados/`                                 |

[↑ Voltar ao sumário](#sumário)

## 4. Estrutura de pastas

```
supermarket-analysis/
├── data/
│   ├── raw/                     # CSV original e exportações do banco
│   └── processed/               # vendas_tratadas.csv
├── resultados/                  # estatísticas e gráficos
├── sql/
│   ├── 01_criar_banco.sql
│   ├── 02_criar_tabelas.sql
│   └── 03_consultas.sql
├── src/
│   ├── 01_leitura_dados.py      # leitura e inspeção do CSV
│   ├── conexao.py               # conexão com o PostgreSQL
│   ├── carga_raw.py             # carga do CSV na raw_vendas
│   ├── 02_etl_vendas.py         # limpeza, tipagem e colunas derivadas
│   └── 03_estatistica.py        # estatísticas e gráficos
├── .gitignore
├── README.md
└── requirements.txt
```

[↑ Voltar ao sumário](#sumário)

## 5. Como executar

### 5.1 Pré-requisitos

PostgreSQL, DBeaver (ou outro cliente SQL) e Python 3 instalados.

### 5.2 Clonar e criar o ambiente virtual

```bash
git clone <URL-DO-SEU-REPOSITORIO>
cd supermarket-analysis
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 5.3 Configurar as credenciais

Crie um arquivo `credenciais.env` na pasta principal (ele **não** vai para o GitHub):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=supermarket_analysis
DB_USER=postgres
DB_PASSWORD=******
```

### 5.4 Criar o banco e as tabelas

No DBeaver, conectado ao banco `postgres`, execute `sql/01_criar_banco.sql`. Depois, conectado ao banco `supermarket_analysis`, execute `sql/02_criar_tabelas.sql`.

### 5.5 Colocar o CSV original

Salve o arquivo do Kaggle em `data/raw/supermarket_analysis.csv`.

### 5.6 Rodar o pipeline

Execute na ordem:

```bash
python src/01_leitura_dados.py    # inspeção inicial
python src/carga_raw.py           # carga na raw_vendas
python src/02_etl_vendas.py       # tratamento e carga na vendas_tratadas
python src/03_estatistica.py      # estatísticas e gráficos
```

As consultas de `sql/03_consultas.sql` podem ser executadas no DBeaver a qualquer momento depois da carga raw.

[↑ Voltar ao sumário](#sumário)

## 6. Fases do projeto

| Fase                                    | O que foi feito                                                                                                                    |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **0. Banco e tabelas**            | Criação do banco e das tabelas Raw e Tratada, com chave primária e restrições`NOT NULL` e `CHECK`                         |
| **1. Carga Raw**                  | O CSV é carregado em`raw_vendas` com todas as colunas como texto, sem alterar o conteúdo original                              |
| **2. Consultas e exportação**   | Nove consultas SQL (`SELECT`, `WHERE`, `GROUP BY`, `SUM`, `AVG`, `COUNT`) e exportação de resultados para CSV        |
| **3. Transformação com Pandas** | Renomeação das colunas, conversão de tipos, verificação de ausentes, remoção de duplicadas e criação de colunas derivadas |
| **4. Análise**                   | Estatística descritiva e gráficos que respondem às perguntas de negócio                                                        |

[↑ Voltar ao sumário](#sumário)

## 7. Dicionário de dados

Camada tratada (`vendas_tratadas`):

| Coluna            | Tipo          | Descrição                                       |
| ----------------- | ------------- | ------------------------------------------------- |
| id_venda          | VARCHAR(50)   | Chave primária da venda                          |
| filial            | VARCHAR(10)   | Filial                                            |
| cidade            | VARCHAR(100)  | Cidade da filial                                  |
| tipo_cliente      | VARCHAR(50)   | Membro ou normal                                  |
| genero            | VARCHAR(20)   | Gênero do cliente                                |
| linha_produto     | VARCHAR(150)  | Categoria do produto                              |
| preco_unitario    | NUMERIC(10,2) | Preço por unidade                                |
| quantidade        | INTEGER       | Itens comprados                                   |
| imposto           | NUMERIC(10,2) | Imposto de 5%                                     |
| valor_total       | NUMERIC(12,2) | Valor total da venda                              |
| data_venda        | DATE          | Data da venda                                     |
| hora_venda        | TIME          | Horário da venda                                 |
| forma_pagamento   | VARCHAR(50)   | Dinheiro, cartão de crédito ou carteira digital |
| custo_mercadoria  | NUMERIC(12,2) | Custo da mercadoria vendida                       |
| margem_percentual | NUMERIC(10,2) | Margem bruta em %                                 |
| receita_bruta     | NUMERIC(12,2) | Receita bruta da venda                            |
| avaliacao         | NUMERIC(4,2)  | Nota do cliente (0 a 10)                          |

Colunas derivadas (apenas no CSV tratado): `mes`, `dia_semana`, `hora`, `periodo_dia` e `valor_total_confere`.

[↑ Voltar ao sumário](#sumário)

## 8. Principais resultados

Respostas às perguntas de negócio do projeto:

| # | Pergunta                                                    | Resposta                                                                   |
| - | ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| 1 | Qual filial apresentou o maior faturamento?                 | Giza (Naypyitaw), com 110.568,71                                           |
| 2 | Qual filial realizou a maior quantidade de vendas?          | Alex (Yangon), com 340 vendas (Cairo 332 e Giza 328)                       |
| 3 | Qual linha de produto apresentou o maior faturamento?       | Food and beverages, com 56.144,86                                          |
| 4 | Qual linha de produto recebeu a melhor avaliação média?  | Food and beverages, com nota 7,11                                          |
| 5 | Qual foi a forma de pagamento mais utilizada?               | Ewallet, com 345 vendas (Cash tem 344)                                     |
| 6 | Qual foi o valor médio das vendas?                         | 322,97                                                                     |
| 7 | Qual foi a maior venda registrada?                          | 1.042,65 (venda 860-79-0874, filial Giza, Fashion accessories, 15/02/2019) |
| 8 | Em qual dia da semana ocorreu a maior quantidade de vendas? | Sábado, com 164 vendas                                                    |

Informações complementares:

- Avaliação média geral de 6,97 (Giza 7,07, Alex 7,03 e Cairo 6,82)
- Linha com mais itens vendidos: Electronic accessories, com 971 itens
- Mês com mais vendas: janeiro de 2019 (352 vendas)
- Horário com mais vendas: 19h (113 vendas)

As três filiais têm faturamento parecido: Giza lidera, e Alex e Cairo ficam praticamente empatadas. O dataset não informa a moeda, mas os valores são apresentados em reais simulando a moeda do Brasil. Os valores da camada tratada podem diferir em centavos dos calculados no SQL sobre a raw, porque o ETL arredonda cada venda para 2 casas antes de somar.

Os arquivos completos estão em `resultados/`:

- `respostas_negocio.txt`
- `estatistica_descritiva.csv`
- 7 gráficos em PNG (faturamento, categorias, pagamentos, vendas por mês e por hora, avaliação e distribuição do valor total)

[↑ Voltar ao sumário](#sumário)

## 9. Boas práticas

- Credenciais em `credenciais.env`, protegido pelo `.gitignore`
- Código organizado em funções e módulos (conexão separada da carga)
- Estilo PEP 8
- Camada Raw preservada, sem alterações, para permitir reprocessamento

[↑ Voltar ao sumário](#sumário)

## 10. Autora

Seu Nome
[GitHub]https://github.com/Karine6Casas · [LinkedIn] linkedin.com/in/ana-karine-m-farias-91559426a

[↑ Voltar ao sumário](#sumário)
