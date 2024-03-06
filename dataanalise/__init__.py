import pandas as pd
import plotly.express as px

def analisar():
    dados = pd.read_html('https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_taxa_de_homic%C3%ADdios')
    mais250 = dados[0]
    menores = dados[1]
    print(dados[0])

def lerdados():
    dados = pd.read_csv('dadosindicadoresPB3.csv')
    #excluir colunas
    dados.drop(columns=['code'], inplace=True)
    return dados

def exibirmapacorrelacoes(data):
    data.drop(columns=['municipio'], inplace=True)
    fig = px.imshow(data.corr())
    return fig


def exibirgraficobarraseduc(dados):
    fig = px.bar(dados, x='municipio', y='somaedu')
    return fig

'''
['Municípios', 'Gentílico',
       'Salário médio mensal dos trabalhadores formais', 'PIB per capita',
       'IDEB – Anos finais do ensino fundamental (Rede pública)',
       'População no último censo']
'''