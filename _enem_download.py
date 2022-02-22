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

# Sintaxe: python _enem_download.py 2020

import os
import re
import sys
import zipfile

microdados = ['https://download.inep.gov.br/microdados/microdados_enem_2020.zip',
              'https://download.inep.gov.br/microdados/microdados_enem_2019.zip',  # [695M]
              'https://download.inep.gov.br/microdados/microdados_enem2018.zip',  # [709M]
              'https://download.inep.gov.br/microdados/microdados_enem2017.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2016.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2015.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2014.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2013.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2012.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2011.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2010_2.zip',
              'https://download.inep.gov.br/microdados/microdados_enem2009.zip',
              'https://download.inep.gov.br/microdados/microdados_enem_2008.zip',
              'https://download.inep.gov.br/microdados/microdados_enem_2007_DVD.zip',
              'https://download.inep.gov.br/microdados/microdados_ENEM_2006.zip',
              'https://download.inep.gov.br/microdados/microdados_enem_2005.zip',
              'https://download.inep.gov.br/microdados/micro_enem2004.zip',
              'https://download.inep.gov.br/microdados/micro_enem2003.zip',
              'https://download.inep.gov.br/microdados/micro_enem2002.zip',
              'https://download.inep.gov.br/microdados/micro_enem2001.zip',
              'https://download.inep.gov.br/microdados/micro_enem2000.zip',
              'https://download.inep.gov.br/microdados/micro_enem1999.zip',
              'https://download.inep.gov.br/microdados/micro_enem1998.zip']

names = [re.sub('\D', '', i)[:4] for i in microdados]

if len(sys.argv) > 1 and sys.argv[1] in names:
  file = sys.argv[1] + '.zip'
  os.system("wget " + microdados[names.index(sys.argv[1])] + " -O " + file)
  zip_ref = zipfile.ZipFile(file, 'r')
  zip_ref.extractall(sys.argv[1])
  os.system("rm " + file)
  zip_ref.close()
  os.rename(sys.argv[1]+'/PROVAS E GABARITOS', sys.argv[1]+'/PROVAS_E_GABARITOS')
