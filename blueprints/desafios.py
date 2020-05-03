import pandas as pd 
from flask import (Blueprint, render_template, request, Response)
import matplotlib.pyplot as plt
from config.utils import (DirectoryConfiguration, series_to_table_html)

# para o plt rodar no macOS
plt.switch_backend('Agg')

# seta o blueprint
desafios = Blueprint('desafios', __name__)

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

@desafios.route('/')
def index():
	return render_template('desafios_index.html')

@desafios.route('/aula1/desafio1')
def aula1_desafio1():
	title = "AULA 1 - DESAFIO 1"
	notas_medias_por_filme = avaliacoes.groupby("filmeId")["nota"].mean()
	filmes_com_media = filmes.join(notas_medias_por_filme, on="filmeId")
	avaliacoes_count = filmes_com_media['nota'].value_counts(dropna=False)
	name = "Contagem das avaliações"
	header = ["nota", "qtd"]
	data = series_to_table_html(name=name, header=header, series=avaliacoes_count)

	return render_template("desafios.html", title=title, data=data)


	
