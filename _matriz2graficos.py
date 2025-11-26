'''
=====================================================================
Copyright (C) 2021 UFABC, developed by Francisco de Assis Zampirolli
from Federal University of ABC and individual contributors.
All rights reserved.

This file is part of "ENEM Interativo".

Languages: Python 3.8.5, Javascript, HTML and many libraries
described at github.com/fzampirolli/ENEM

You should cite some references included in vision.ufabc.edu.br
in any publication about it.

ENEM Interativo is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License
(gnu.org/licenses/agpl-3.0.txt) as published by the Free Software
Foundation, either version 3 of the License, or (at your option)
any later version.

ENEM Interativo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
=====================================================================
'''

import csv
import glob
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from pyirt import irt
#pip install plotly>=4.0.0
import plotly.graph_objects as go
import pylab
import seaborn as sns
from PIL import Image

DPI_resolution = 200
width_resolution = 2400
height_resolution = 1600

def plot_TRI(a, b, c, D, media, std, f, TAM):
  theta = np.arange(-5, 5, .1)
  # x = np.arange(-theta, theta, .1)
  irt = c + (1 - c) / (1 + np.exp(-D * a * (theta - b)))
  plt.clf()
  plt.title("TRI-CCI com amostra de %s candidatos\n média=%.2f, std=%.2f" % (TAM, media, std))
  plt.ylabel("Prob. Respostas Correta")

  plt.vlines(b, 0, 0.5, linestyle=':')

  _ = plt.plot(theta, irt, 'b-', linewidth=1)

  # x1 = b
  # y1 = irt[(x1 + theta) * 10]
  # xrange = np.arange(x1 - 1, x1 + 1, .1)
  # plt.scatter(x1, y1, color='r', s=50)
  # def line(a, x, x1, y1):
  #  return a * (x - x1) / 3 + y1
  # plt.plot(xrange, line(a, xrange, x1, y1), 'r--', linewidth=3)

  if a < .5:
    plt.text(b + .4, 0.5, 'a=%.1f => não separa bem hab.' % a)
  elif a >= 1.5:
    plt.text(b + .4, 0.5, 'a=%.1f => separa bem hab.' % a)
  else:
    plt.text(b + .4, 0.5, 'a=%.1f' % a)

  plt.text(b + 0.1, 0.05, 'b=%.1f' % b)
  plt.text(min(theta), c + .05, 'c=%.1f' % c)
  if -1 < b <= 1:
    plt.xlabel("Habilidade: b próximo de %d => item médio" % 0)
  elif 1 < b <= 3:
    plt.xlabel("Habilidade: b próximo de %d => item difícil" % 2)
  elif b > 3:
    plt.xlabel("Habilidade: b > %d => item muito difícil" % 3)
  elif -3 < b <= -1:
    plt.xlabel("Habilidade: b próximo de %d => item fácil" % -2)
  elif b <= -3:
    plt.xlabel("Habilidade: b < %d => item muito fácil" % -3)

  x1, x2, y1, y2 = plt.axis()
  plt.axis((x1, x2, 0, 1))

  plt.grid()
  # _ = plt.plot(x, irt, 'b-', linewidth=1)
  plt.savefig(f)


def drawViolinPlot(f, vet, i):
  s = '<br> %d ' % i
  fig1 = go.Violin(meanline_visible=True, box_visible=True,
                   y=vet, name='')
  layout = go.Layout(title_font_size=12,
                     width=800, height=500, showlegend=False,
                     title={'text': s, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                     # yaxis=dict(title=cols[col])
                     )
  fig = go.Figure(layout=layout)
  fig.add_trace(fig1)
  fig.show()

  fig.write_image(f, width=width_resolution, height=height_resolution)
  img = Image.open(f)
  img.save(f)

def draw_signoits(pasta, f, mat):
  theta = np.arange(-5, 5, .1)
  for i in range(mat.shape[0]):
    a = mat[i][0]  # discriminação
    b = mat[i][1]  # dificuldade
    c = mat[i][2]  # chute
    m = mat[i][3]  # media
    st = mat[i][4]  # std
    D = 1.7  # fator de escala

    codigo, tam = f.split('/')[-1].split('_')[0:2]
    fimg = pasta + '/' + str(codigo) + '_' + str(tam) + '_fig_tri_' + str(i + 1).zfill(3) + '.png'
    print(fimg)
    plot_TRI(a, b, c, D, m, st, fimg, tam)

def genStatistics(pasta):
  print(pasta)

  path0 = './' + pasta + "/FIGS"
  if not os.path.exists(path0):
    print("Create: ", path0)
    os.system('mkdir ' + path0)

  colunas = '"","Dscrmn","Dffclt","Gussng"'
  colunas = colunas.split(',')
  for f in sorted(glob.glob(pasta + '/DADOS/MATRIZ/*_TRI.csv')):
    print(f)
    print(f[:-8])
    df_mat = pd.read_csv(f[:-8], sep=',', header=None)
    df_tri = pd.read_csv(f, sep=',')

    mat = df_mat.to_numpy()

    codigo, tam = f.split('/')[-1].split('_')[0:2]
    for i in range(0,mat.shape[1]):
      fimg = path0 + '/' + str(codigo) + '_' + str(tam) + '_fig_box_' + str(i + 1).zfill(3) + '.png'
      print(fimg)
      drawViolinPlot(fimg, mat[:,i], i)

    v_mean = np.mean(mat, axis=0)
    v_std = np.std(mat, axis=0)

    mat = df_tri.to_numpy()[:, 1:]
    mat = np.insert(mat, 3, v_mean, axis=1)
    mat = np.insert(mat, 4, v_std, axis=1)

    draw_signoits(path0, f, mat)


names = [str(i).zfill(4) for i in range(2014, 2020)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    genStatistics(sys.argv[pasta])  # ano
