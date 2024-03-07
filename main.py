from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def padrao():
    return render_template('index2.html')

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    #O metodo post é implementado aqui, onde adiciona
    #no servidor flask os valores digitados em nome
    #e senha
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha):
        return render_template('menu.html')
    else:
        return render_template('index2.html')

@app.route('/grafvioleciapib', methods=['POST','GET'])
def gerarGrafViolenciaPib():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados()
    dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
    return render_template('grafviolenciapib.html', mapa=fig.to_html())

@app.route('/grafcrimesemcidades', methods=['POST','GET'])
def grafCrimesEmCidades():

    dados = da.lerdados()

    cvp_porcentagem = dados.groupby('municipio')['cvp'].sum() / dados['cvp'].sum() * 100

    fig = px.pie(values=cvp_porcentagem, names=cvp_porcentagem.index, title='Porcentagem de Crimes de Violência Contra o Patrimônio (CVP) em Cada Município')
    return render_template('grafcrimesemcidades.html', mapa=fig.to_html())


@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados()
    fig = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig.to_html())

@app.route('/melhoresedu')
def exibirmunicipiosedu():
    data = da.lerdados()

    data['somaedu'] = data['idebanosiniciais'] + data['idebanosfinais']
    data.sort_values(by=['somaedu'], ascending=False, inplace=True)
    fig= da.exibirgraficobarraseduc(data.head(15))

    return render_template('melhoresedu.html', mapa=fig.to_html())

@app.route('/grafpibidh')
def gerarGrafPibIdh():
    dados = da.lerdados()

    fig = px.area(dados, x='municipio', y=['pib', 'idh'], title='PIB e Índice de Desenvolvimento Humano (IDH)', labels={'value': 'Valor'})
    return render_template('grafpibidh.html', mapa=fig.to_html())


@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)