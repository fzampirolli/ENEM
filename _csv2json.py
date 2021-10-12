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

import json
import sys

import pandas as pd

CORES = ['AZUL', 'AMARELO', 'BRANCO', 'ROSA', 'CINZA']
AREAS = ['CIÊNCIAS DA NATUREZA', 'CIÊNCIAS HUMANAS', 'LINGUAGENS, CÓDIGOS', 'MATEMÁTICA']
areasID = ['CN', 'CH', 'LC', 'MT']


def getGabs(gab):
  df = pd.read_csv(gab, sep=';', index_col=0)

  def getGabCor(df):
    qstr = '{"answer": "__answer__", "ability": __ability__, "id": __id__, "percentage": 0, "irt": [], "images": [], "videos": [], "subareas": [] }'
    gab = {}
    # for i, v in enumerate(np.arange(503, 516, 4)):
    for v in sorted(df['CO_PROVA'].unique()):
      if 1:  # 503 <= int(v) <= 518:
        dfAux = df.loc[df['CO_PROVA'] == v]
        d = {}
        area50 = len(list(dfAux['TX_GABARITO']))
        habilidade = list(dfAux['CO_HABILIDADE'])
        codQuestion = list(dfAux['CO_ITEM'])
        COR = list(dfAux['TX_COR'])[0].upper()
        if COR == 'BRANCA':
          COR = 'BRANCO'
        if COR == 'AMARELA':
          COR = 'AMARELO'
        AREA = list(dfAux['SG_AREA'])[0]
        for qi, answer in enumerate(list(dfAux['TX_GABARITO'])):
          aux = json.loads(
            qstr.replace('__answer__', answer).replace('__ability__', str(habilidade[qi])).replace('__id__',
                                                                                                   str(
                                                                                                     codQuestion[qi])))
          if area50 == 50:
            if qi < 5:
              d[str(qi + 1)] = aux
            else:
              d[str(qi - 4).zfill(2)] = aux
          else:
            d[str(qi + 1).zfill(2)] = aux

        gab[str(v)] = {'COR': COR, "AREA": AREA, "QUESTIONS": d}  # list(dfAux['TX_GABARITO'])
    return gab

  return getGabCor(df)


names = [str(i).zfill(4) for i in range(2014, 2020)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    url = './' + sys.argv[pasta] + '/'
    gab = url + 'DADOS/ITENS_PROVA_' + sys.argv[pasta] + '.csv'

    if 1:  # try:
      print('gab:  ', gab)
      gabsDict = getGabs(gab)

      file = '/'.join([p for p in gab.split('/')[:-1]]) + '/' + gab.split('/')[-1][:-4] + '.json'
      print('Save: ', file)
      json.dump(gabsDict, open(file, 'w'), indent=4, sort_keys=False)
    # except:
    # print("ERRO:", gab)
