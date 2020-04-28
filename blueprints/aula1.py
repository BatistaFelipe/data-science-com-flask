import pandas as pd 
import functools
from flask import (Blueprint, render_template, request, Response)
import os
import matplotlib.pyplot as plt
import io

path = os.getcwd()

aula1 = Blueprint('aula1', __name__)

# local dos arquivos csv
uri_filmes = path + "/csv/movies.csv"
uri_avaliacoes = path + "/csv/ratings.csv"

# usa o pandas para ler os arquivos
filmes = pd.read_csv(uri_filmes)
avaliacoes = pd.read_csv(uri_avaliacoes)

# altera o nome das colunas para pt-br
filmes.columns = ["filmeId", "titulo", "generos"]
avaliacoes.columns = ["usuarioId", "filmeId", "nota", "momento"]

plot_dir = path + "/static/images/"

@aula1.route('/')
def index_aula1():
	return render_template('aula1_index.html')

@aula1.route('/aula1-1')
def head_table():
	filmes_head = filmes.head()
	avaliacoes_head = avaliacoes.head()

	return render_template('aula1-1.html',  
		table_filmes=[filmes_head.to_html(classes='data')],
		titles_filmes=[filmes_head.columns.values],
		name_filmes='Filmes (head)',
		table_avaliacoes=[avaliacoes_head.to_html(classes='data')],
		titles_avaliacoes=[avaliacoes_head.columns.values],
		name_avaliacoes='Avaliações (head)',
		shape_avaliacoes=avaliacoes.shape)

@aula1.route('/aula1-2', methods=['POST', 'GET'])
def pesquisa_e_describe():
	if request.method == 'POST':
		if request.form['filmeId']:
			filmeId = request.form['filmeId']
			avaliacoes_pesquisa = avaliacoes.query("filmeId == " + filmeId)
			avaliacoes_head = avaliacoes_pesquisa.head()
			avaliacoes_describe = avaliacoes_pesquisa.describe()
			media_nota_pesquisa = ("%.2f" % avaliacoes_pesquisa['nota'].mean())

			# plot
			# fig, ax = plt.subplots()
			# ax.bar(avaliacoes_head.columns.values, avaliacoes_head)
			# plt.safefig(plot_dir + 'plot.png')

			return render_template('aula1-2.html',  
				table_avaliacoes=[avaliacoes_head.to_html(classes='data')],
				titles_avaliacoes=[avaliacoes_head.columns.values],
				name_avaliacoes='Avaliações (head)',
				table_describe_avaliacoes=[avaliacoes_describe.to_html(classes='data')],
				titles_describe_avaliacoes=[avaliacoes_describe.columns.values],
				name_describe_avaliacoes="Describe Avaliações",
				filmeId=filmeId,
				media_nota_pesquisa=media_nota_pesquisa)
	else:
		return render_template('aula1-2.html')

@aula1.route('/aula1-3')
def join_tables():
	notas_medias_por_filme = avaliacoes.groupby("filmeId")["nota"].mean()
	filmes_com_media = filmes.join(notas_medias_por_filme, on="filmeId")
	filmes_com_media_sort = filmes_com_media.sort_values("nota", ascending=False).head(15)

	return render_template('aula1-3.html',
		table_medias_sort=[filmes_com_media_sort.to_html(classes='data')],
		title_medias_sort=[filmes_com_media_sort.columns.values],
		name_medias_sort='Os 15 com a média mais alta')
