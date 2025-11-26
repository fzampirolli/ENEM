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

import glob
import sys


def criarArquivo(ano):
  CHAVE = 'images'

  # 505_CN_fig_irtxxx.png

  f = open("enemANO.html", "r")
  texto = f.read()
  texto = texto.replace('__ANO__', ano)

  ss = '<ol>\n'
  for f in sorted(glob.glob(ano + '/PROVAS_E_GABARITOS/*INTERATIVO.html')):
    print(f)
    ss += '<li><a href="../' + f + '" target="_blank">' + f.split('/')[-1][:-16] + '</a></li>\n'
  ss += '</ol>\n'

  texto = texto.replace('__ARQUIVOS__', ss)

  with open(ano + '/index.html', 'w') as file:
    file.write(texto)


names = [str(i).zfill(4) for i in range(2014, 2020)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    criarArquivo(sys.argv[pasta])
