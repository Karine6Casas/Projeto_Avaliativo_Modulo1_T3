

-- 1. Conferir as primeiras linhas
SELECT * FROM raw_vendas LIMIT 10;

-- 2. Quantidade total de vendas
SELECT COUNT(*) AS total_vendas FROM raw_vendas;

-- 3. Faturamento por filial (da maior para a menor)
SELECT branch AS filial,
       city AS cidade,
       ROUND(SUM(CAST(sales AS NUMERIC)), 2) AS faturamento
FROM raw_vendas
GROUP BY branch, city
ORDER BY faturamento DESC;

-- 4. Quantidade vendida por categoria de produto
SELECT product_line AS categoria,
       SUM(CAST(quantity AS INTEGER)) AS total_itens
FROM raw_vendas
GROUP BY product_line
ORDER BY total_itens DESC;

-- 5. Formas de pagamento mais usadas
SELECT payment AS forma_pagamento,
       COUNT(*) AS total_vendas
FROM raw_vendas
GROUP BY payment
ORDER BY total_vendas DESC;

-- 6. Valor médio das vendas
SELECT ROUND(AVG(CAST(sales AS NUMERIC)), 2) AS ticket_medio
FROM raw_vendas;

-- 7. Avaliação média por filial
SELECT branch AS filial,
       ROUND(AVG(CAST(rating AS NUMERIC)), 2) AS avaliacao_media
FROM raw_vendas
GROUP BY branch
ORDER BY avaliacao_media DESC;

-- 8. Vendas por mês
SELECT TO_CHAR(TO_DATE(sale_date, 'MM/DD/YYYY'), 'YYYY-MM') AS mes,
       COUNT(*) AS total_vendas
FROM raw_vendas
GROUP BY mes
ORDER BY mes;

-- 9. Vendas acima de 500 (exemplo de WHERE)
SELECT invoice_id, branch, product_line, CAST(sales AS NUMERIC) AS valor
FROM raw_vendas
WHERE CAST(sales AS NUMERIC) > 500
ORDER BY valor DESC;