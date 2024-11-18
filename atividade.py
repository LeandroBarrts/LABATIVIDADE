import numpy as np
from datetime import datetime
import os

# Função principal
def main():
    arquivo_csv = '/mnt/data/vendas.csv'  # Substitua pelo caminho do seu arquivo CSV

if __name__ == "_main_":
    main()

# Função para carregar e preparar os dados
def carregar_dados(arquivo_csv):

        # Carrega os dados com nomes das colunas
        dados = np.genfromtxt(
            arquivo_csv, delimiter=',', dtype=None, encoding='utf-8', skip_header=1, names=True
        )

        # Converte as colunas para tipos apropriados
        datas = np.array([datetime.strptime(row['data'], "%Y-%m-%d") for row in dados])
        regioes = np.array([row['regiao'] for row in dados])
        produtos = np.array([row['produto'] for row in dados])
        quantidade = np.array([float(row['quantidade']) for row in dados])
        preco_unitario = np.array([float(row['preco_unitario']) for row in dados])
        valor_total = quantidade * preco_unitario  # Calculado como array

        # Retorna uma matriz consolidada
        matriz_dados = np.column_stack((datas, regioes, produtos, quantidade, preco_unitario, valor_total))
        return matriz_dados

# Funções de análise
def analise_estatistica(dados):

        valor_total = dados[:, 5].astype(float)
        produtos = dados[:, 2]
        quantidades = dados[:, 3].astype(float)

        # Cálculos de estatísticas
        resultados = {
            "media": np.mean(valor_total),
            "mediana": np.median(valor_total),
            "desvio_padrao": np.std(valor_total)
        }

        # Valor total por produto
        valor_por_produto = {
            produto: valor_total[produtos == produto].sum()
            for produto in np.unique(produtos)
        }

        # Quantidade total por produto
        quantidade_por_produto = {
            produto: quantidades[produtos == produto].sum()
            for produto in np.unique(produtos)
        }

        resultados["produto_mais_vendido"] = max(quantidade_por_produto, key=quantidade_por_produto.get)
        resultados["produto_maior_valor"] = max(valor_por_produto, key=valor_por_produto.get)
        resultados["quantidade_mais_vendida"] = quantidade_por_produto[resultados["produto_mais_vendido"]]
        resultados["valor_maior_venda"] = valor_por_produto[resultados["produto_maior_valor"]]

        regioes = dados[:, 1]
        resultados["total_vendas_por_regiao"] = {
            regiao: valor_total[regioes == regiao].sum() for regiao in np.unique(regioes)
        }

        return resultados

def analise_temporal(dados):

        datas = dados[:, 0]
        valor_total = dados[:, 5].astype(float)

        # Agrupa vendas por dia
        dias_unicos = np.unique(datas)
        vendas_por_dia = np.array([valor_total[datas == dia].sum() for dia in dias_unicos])
        dias_semana = [dia.strftime("%A") for dia in dias_unicos]

        resultados = {
            "venda_media_por_dia": np.mean(vendas_por_dia),
            "dia_mais_vendas": max(set(dias_semana), key=dias_semana.count),
            "variacao_diaria": np.diff(vendas_por_dia)
        }

        return resultados


