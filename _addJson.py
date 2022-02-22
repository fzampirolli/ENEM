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


def alteraChave(ano, CHAVE):
  CHAVE = 'images'

  # 505_CN_fig_irtxxx.png

  with open(ano + '/DADOS/ITENS_PROVA_' + ano + '.json', 'r') as f:
    data = json.load(f)
    for i, t in enumerate(data.keys()):
      print(t, data[t]['AREA'], data[t]['COR'])
      for q in data[t]['QUESTIONS']:
        f = t + '_' + '010000' + '_fig_tri_' + str(int(q)).zfill(3) + '.png'
        data[t]['QUESTIONS'][q][CHAVE].append(f)
        f = t + '_' + '010000' + '_fig_box_' + str(int(q)).zfill(3) + '.png'
        data[t]['QUESTIONS'][q][CHAVE].append(f)

    with open(ano + '/DADOS/ITENS_PROVA_' + ano + '.json', 'w') as outfile:
      json.dump(data, outfile, indent=2)


names = [str(i).zfill(4) for i in range(2014, 2021)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    alteraChave(sys.argv[pasta], 'images')
