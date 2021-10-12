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
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyirt import irt


def enem_to_irt_csv(x):
  rows = len(x)  # Number of students, questions
  cols = 45
  mat = np.zeros((rows + 2, cols + 2), dtype='uint16')
  print(rows, cols)
  for i in range(rows):
    gab, resp = x[i][0], x[i][1]
    for j in range(cols):
      mat[i + 2][j + 2] = 1 if gab[j] == resp[j] else 0

  for i in range(2, cols):
    mat[0, i] = sum(mat[2:, i])  # sum all correct answers
    mat[1, i] = i  # index of question before sort

  for i in range(rows):
    mat[i + 2][0] = sum(mat[i + 2])  # correct answers
    mat[i + 2][1] = i + 1  # x[i][0]  # index of student

  # mat[:, 2:] = mat[:, mat[0].argsort()[:1:-1]]  # sort by answers correct by question
  # mat[2:, :] = mat[mat[2:, 0].argsort()[::-1] + 2, :]  # sort by answers correct by student

  # save data
  with open('_data_all.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(mat)

  # old version of Okamoto
  with open('_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(mat[2:, 2:])

  # new version of Okamoto: row 1 is ID question; col 1 is ID student
  with open('_data.new.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(mat[1:, 1:])

  return mat[2:, 2:]


def ep_irt(x):
  H, W = len(x), len(x[0])
  print(H, W)
  src_fp = []
  for r in range(H): # users
    for i in range(W): # questions
      src_fp.append((r, i, x[r, i]))

  # alternatively, pass in list of tuples in the format of [(user_id, item_id, ans_boolean)]
  # ans_boolean is 0/1.

  guessParamDict = {'1': {'c': 0.0}, '2': {'c': 0.2}}
  item_param, user_param = irt(src_fp,
                               theta_bnds=[-5, 5],
                               alpha_bnds=[0.2, 2],
                               beta_bnds=[-3, 3],
                               model_spec='2PL',
                               in_guess_param=guessParamDict
                               )
  return item_param, user_param


def plot_IRT(a, b, c, D, media, std, f, TAM):
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


def draw_signoits(pasta, codigo, area, item_param, mat, TAM):
  # plot
  v_mean = np.mean(mat[2:, 2:], axis=0)
  v_std = np.std(mat[2:, 2:], axis=0)
  theta = np.arange(-5, 5, .1)
  for i in range(len(item_param)):
    a = item_param[i]['alpha']  # discriminação
    b = item_param[i]['beta']  # dificuldade
    c = item_param[i]['c']  # chute
    D = 1.7  # fator de escala
    f = pasta + '/' + str(codigo) + '_' + area + '_fig_irt' + str(i + 1).zfill(3) + '.png'
    print(f)
    plot_IRT(a, b, c, D, v_mean[i], v_std[i], f, TAM)


def genStatistics(pasta, TAM):
  print(pasta)
  local = pasta + '/DADOS/MICRODADOS_ENEM_' + pasta + '.csv'
  colunas = 'CO_PROVA_CN;CO_PROVA_CH;CO_PROVA_LC;CO_PROVA_MT;'
  colunas += 'TX_RESPOSTAS_CN;TX_RESPOSTAS_CH;TX_RESPOSTAS_LC;TX_RESPOSTAS_MT;'
  colunas += 'TP_LINGUA;TX_GABARITO_CN;TX_GABARITO_CH;TX_GABARITO_LC;TX_GABARITO_MT'
  colunas = colunas.split(';')
  TextFileReader = pd.read_csv(local, sep=';', encoding="ISO-8859-1", engine='python', usecols=colunas, low_memory=True,
                               chunksize=100000)
  dfList = []
  for i, df in enumerate(TextFileReader):
    dfList.append(df)
    print(i, df.shape)
    # if i >= 1: break

  df = pd.concat(dfList, sort=False)
  print(df.shape)

  areasID = ['CN', 'CH', 'LC', 'MT']
  for a in areasID:
    print('\n\n\n', a)
    for v in sorted(df['CO_PROVA_' + a].unique()):
      codigo = str(v)[:-2]
      print(codigo)
      if str(v) != 'nan':
        print('CO_PROVA_' + a + ' == ' + codigo)
        df0 = df.query('CO_PROVA_' + a + ' == ' + codigo)  # + ' & TP_LINGUA == 0')
        df0 = df0[['TX_GABARITO_' + a, 'TX_RESPOSTAS_' + a]]
        print(df.query('CO_PROVA_' + a + ' == ' + codigo + ' & TP_LINGUA == 0').shape[0])  # ingles
        print(df.query('CO_PROVA_' + a + ' == ' + codigo + ' & TP_LINGUA == 1').shape[0])  # espanhol
      else:
        continue
      df0 = df0.dropna()  # remove alunos faltantes
      tam = df0.shape[0]
      if (tam > int(TAM)):
        df0 = df0.sample(int(TAM))
      else:
        TAM = tam

      mat = enem_to_irt_csv(df0.to_numpy())
      printM(mat)
      item_param19, user_param19 = ep_irt(mat[2:, 2:])
      path0 = './' + pasta + "/FIGS"
      if not os.path.exists(path0):
        print("Create: ", path0)
        os.system('mkdir ' + path0)
      draw_signoits(path0, codigo, a, item_param19, mat, TAM)


names = [str(i).zfill(4) for i in range(2014, 2020)]
for pasta in range(len(sys.argv) - 1):
  if sys.argv[pasta] in names:
    print(sys.argv[-1])
    genStatistics(sys.argv[pasta], sys.argv[-1])  # ano e tamanho da amostra
