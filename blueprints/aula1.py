import pandas as pd 
from flask import (Blueprint, render_template, request, Response)
import matplotlib.pyplot as plt
from config.utils import DirectoryConfiguration

# para o plt rodar no macOS
plt.switch_backend('Agg')

# seta o blueprint
aula1 = Blueprint('aula1', __name__)

# diretórios
config = DirectoryConfiguration()
CSV_DIR = config.CSV_DIR
PLOT_DIR = config.PLOT_PICTURES_DIR

# arquivos csv
uri_filmes = CSV_DIR + "/movies.csv"
uri_avaliacoes = CSV_DIR + "/ratings.csv"

# usa o pandas para ler os arquivos
filmes = pd.read_csv(uri_filmes)
avaliacoes = pd.read_csv(uri_avaliacoes)

# altera o nome das colunas para pt-br
filmes.columns = ["filmeId", "titulo", "generos"]
avaliacoes.columns = ["usuarioId", "filmeId", "nota", "momento"]

@aula1.route('/')
def index_aula1():
	return render_template('aula1_index.html')

@aula1.route('/aula1-1')
def head_table():
	title = 'AULA 1-1'
	filmes_head = filmes.head()
	avaliacoes_head = avaliacoes.head()

	tb_filmes = "<h3> Filmes (head) </h3>" + filmes_head.to_html(index=False) + "<br />"
	tb_avaliacoes = "<h3> Avaliações (head) </h3>" + avaliacoes_head.to_html(index=False) + "<br />"
	label_text = ('<p>"Formato" dos dados da tabela Avaliações (linhas X colunas): %s </p>' % str(avaliacoes.shape))
	data = tb_filmes + tb_avaliacoes + label_text
	
	return render_template('aula1.html', title=title, data=data)

@aula1.route('/aula1-2', methods=['POST', 'GET'])
def pesquisa_e_describe():
	title = "AULA 1-2"
	form =''' 
	<form action="/aula1/aula1-2" method="POST">
		<label for="filmeId">Digite o ID do Filme:</label><br>
		<input type="text" id="filmeId" name="filmeId" placeholder="(número inteiro)"><br>
		<input type="submit" value="Submit">
	</form> 
	<br>'''

	if request.method == 'POST':
		if request.form['filmeId']:
			filmeId = request.form['filmeId']
			avaliacoes_pesquisa = avaliacoes.query("filmeId == " + filmeId)
			avaliacoes_head = avaliacoes_pesquisa.head()
			avaliacoes_describe = avaliacoes_pesquisa.describe()
			media_nota_pesquisa = ("%.2f" % avaliacoes_pesquisa['nota'].mean())

			avaliacoes_pesquisa['nota'].plot(kind='hist', title='Notas do filme')
			name_plot = '/plot1_aula1_2.png'
			plt.savefig(PLOT_DIR + name_plot)
			url_plot = '/static/images' + name_plot


			label_filmeID = ("<h2>FilmeID: %s </h2>" % filmeId)
			label_media = ("<h2>Média (nota): %s </h2>" % media_nota_pesquisa)
			tb_avaliacoes = "<h3> Avaliações (head) </h3>" + avaliacoes_head.to_html(index=False) + "<br />"
			tb_avaliacoes_describe = "<h3> Descrição </h3>" + avaliacoes_describe.to_html() + "<br />"

			label_img = ('<img src="%s" alt="" height="300px" width="400px">' % url_plot)

			data = form + label_filmeID + label_media + tb_avaliacoes + tb_avaliacoes_describe + label_img

			return render_template('aula1.html', title=title, data=data)

	else:
		return render_template('aula1.html', title=title, data=form)

@aula1.route('/aula1-3')
def join_tables():
	title = "AULA 1-3"
	notas_medias_por_filme = avaliacoes.groupby("filmeId")["nota"].mean()
	filmes_com_media = filmes.join(notas_medias_por_filme, on="filmeId")
	filmes_com_media_sort = filmes_com_media.sort_values("nota", ascending=False).head(15)

	data = "<h3> 15 filmes com maior média </h3>" + filmes_com_media_sort.to_html(index=False) + "<br />"

	return render_template('aula1.html', title=title, data=data)
