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


def printM(m):
  h, w = m.shape
  for i in range(h):
    print(*m[i])

def enem_to_mat(f,x):
  rows = len(x)  # Number of students, questions
  cols = 45
  mat = np.zeros((rows + 2, cols + 2), dtype='uint32')
  print(rows, cols)
  for i in range(rows):
    gab, resp = x[i][0], x[i][1]
    for j in range(cols):
      mat[i + 2][j + 2] = 1 if gab[j] == resp[j] else 0

  for i in range(2, cols + 2):
    mat[0, i] = sum(mat[2:, i])  # sum all correct answers
    mat[1, i] = i - 1  # index of question before sort

  for i in range(rows):
    mat[i + 2][0] = sum(mat[i + 2])  # correct answers
    mat[i + 2][1] = i + 1  # x[i][0]  # index of student

  # printM(mat)
  #mat[:, 2:] = mat[:, mat[0].argsort()[:1:-1]]  # sort by answers correct by question
  mat[2:, :] = mat[mat[2:, 0].argsort()[::-1] + 2, :]  # sort by answers correct by student
  # printM(mat)

  # # save data
  # with open(f+'_data_all.csv', 'w', newline='') as file:
  #   writer = csv.writer(file, delimiter=',')
  #   writer.writerows(mat)

  # old version of Okamoto
  with open(f+'_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(mat[2:, 2:])

  # # new version of Okamoto: row 1 is ID question; col 1 is ID student
  # with open(f+'_data.new.csv', 'w', newline='') as file:
  #   writer = csv.writer(file, delimiter=',')
  #   writer.writerows(mat[1:, 1:])

  return mat

def genStatistics(pasta):
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
    #if i >= 1: break

  df = pd.concat(dfList, sort=False)
  print(df.shape)

  path0 = './' + pasta + "/DADOS/MATRIZ/"
  if not os.path.exists(path0):
    print("Create: ", path0)
    os.system('mkdir ' + path0)

  areasID = ['CN', 'CH', 'LC', 'MT']
  for a in areasID:
    print('\n', a)

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
      print('tam = ',tam)
      T = 10
      if tam > 2000:
        T = 2000
        df2 = df0.sample(T)
        file = path0 + codigo + '_' + str(T).zfill(6)
        print(file)
        mat = enem_to_mat(file, df2.to_numpy())
      else:
        while T < tam and T <= 100000:
          print("T = ", T)
          if (tam > T):
            df2 = df0.sample(T)
            file = path0 + codigo + '_' + str(T).zfill(6)
            print(file)
            mat = enem_to_mat(file, df2.to_numpy())
            if tam > T*10:
              T *= 10
            else:
              T = tam
              file = path0 + codigo + '_' + str(tam).zfill(6)
              print(file)
              mat = enem_to_mat(file, df0.to_numpy())
          else:
            file = path0 + codigo + '_' + str(tam).zfill(6)
            print(file)
            mat = enem_to_mat(file, df0.to_numpy())

names = [str(i).zfill(4) for i in range(2014, 2020)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    print(sys.argv[-1])
    genStatistics(sys.argv[pasta])  # ano
