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
# run localhost with python3 -m http.server --cgi 8080

import glob
import os
import re
import sys

'''
converte pdf para html utilizando pdf2htmlEX e
converte html para html interativo

sintaxe:
python _pdf2html.py html interativo 2019 2018
'''

CORES = ['AZUL', 'AMARELO', 'BRANCO', 'ROSA', 'CINZA']
AREAS = ['CIÊNCIAS DA NATUREZA', 'CIÊNCIAS HUMANAS', 'LINGUAGENS, CÓDIGOS', 'MATEMÁTICA']
areasID = ['CN', 'CH', 'LC', 'MT']


def PdfToHtml(f):
  print('pdf2htmlEX', f)
  path_pdf = '/'.join([p for p in f.split('/')[:-1]]) + '/'
  file = path_pdf + f.split('/')[-1][:-3] + 'html'
  print('Path:      ' + path_pdf)
  print('Save:      ' + file)
  os.system(
    "pdf2htmlEX " + f)  # --embed-css 0 --embed-font 0 --embed-image 0 --embed-javascript 0 --embed-outline 0 --split-pages 0 --process-type3 1 --tounicode 1 --optimize-text 1
  # os.system('chown ufabc:ufabc . -R')
  os.system('cp ' + f.split('/')[-1][:-3] + 'html ' + path_pdf)
  os.system('rm ' + f.split('/')[-1][:-3] + 'html ')
  os.system('bash _myrepl0.sh ' + file + " > " + '_lixo0.html')
  os.system('bash _myrepl1.sh ' + '_lixo0.html' + " > " + '_lixo1.html')
  print('cp _lixo1.html ' + file)
  os.system('cp _lixo1.html ' + file)
  # os.system('rm _lixo*.html ' + file)

  # genJSON(dirFiles)


def includeButtonsQuestions(f):
  print('includeButtonsQuestions', f)
  html = open(f, 'r')
  text = html.read()

  ## inclui tipo de prova em id de body
  print(">>>>>", f)
  tipoProva = f.split('/')[-1][:-5]
  if '_DIA_1_' in f:
    tipoProva += '_LC_CH_'
  elif '_DIA_2_' in f:
    tipoProva += '_CN_MT_'

  if 'ENEM_2019_P1_CAD_01_DIA_1_AZUL' in f: tipoProva += '511_507'
  if 'ENEM_2019_P1_CAD_02_DIA_1_AMARELO' in f: tipoProva += '512_508'
  if 'ENEM_2019_P1_CAD_03_DIA_1_BRANCO' in f: tipoProva += '514_509'
  if 'ENEM_2019_P1_CAD_04_DIA_1_ROSA' in f: tipoProva += '513_510'
  if 'ENEM_2019_P1_CAD_05_DIA_2_AMARELO' in f: tipoProva += '504_516'
  if 'ENEM_2019_P1_CAD_06_DIA_2_CINZA' in f: tipoProva += '505_518'
  if 'ENEM_2019_P1_CAD_07_DIA_2_AZUL' in f: tipoProva += '503_515'
  if 'ENEM_2019_P1_CAD_08_DIA_2_ROSA' in f: tipoProva += '506_517'
  if 'ENEM_2019_P2_CAD_01_DIA_1_AZUL' in f: tipoProva += '551_547'
  if 'ENEM_2019_P2_CAD_02_DIA_1_AMARELO' in f: tipoProva += '552_548'
  if 'ENEM_2019_P2_CAD_03_DIA_1_BRANCO' in f: tipoProva += '553_549'
  if 'ENEM_2019_P2_CAD_04_DIA_1_ROSA' in f: tipoProva += '554_550'
  if 'ENEM_2019_P2_CAD_05_DIA_2_AMARELO' in f: tipoProva += '543_555'
  if 'ENEM_2019_P2_CAD_06_DIA_2_CINZA' in f: tipoProva += '544_556'
  if 'ENEM_2019_P2_CAD_07_DIA_2_AZUL' in f: tipoProva += '545_557'
  if 'ENEM_2019_P2_CAD_08_DIA_2_ROSA' in f: tipoProva += '546_558'

  text = text.replace('<body>', '<body id="' + tipoProva + '">')

  ## title
  ss = '<title>ENEM Interativo by UFABC</title>\n'
  ss += '<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>\n'
  ss += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>\n'
  ss += '<link rel="stylesheet" href="../../_cronometro.css">\n'
  ss += '<script src="../../_quiz.js"></script>\n'
  text = text.replace('<title></title>', ss)

  ## cronometro e título h2
  ss = '<div id="page-container">\n'
  ss += '<script>loadJSON("' + tipoProva + '")</script>\n'
  ss += '<div class="cronometro"><table  style="width: 78%;"><thead><tr>\n'
  ss += '<th style="font-size: 14px; background-color: lightgreen; width: 200px;">\n'
  ss += '<div id="contador">\n'
  ss += '   <div class="reloj" id="Horas">00</div>\n'
  ss += '   <div class="reloj" id="Minutos">:00</div>\n'
  ss += '   <div class="reloj" id="Segundos">:00</div>\n'
  ss += '   <div class="reloj" id="Centesimas">:00</div></div>\n'
  ss += '<div id="botoes">\n'
  ss += '  <input type="button" class="boton" id="inicio" value=" &#9658;" onclick="inicio();">\n'
  ss += '   <input type="button" class="boton" id="parar" value=" &#8718;" onclick="parar();" disabled>\n'
  ss += '   <input type="button" class="boton" id="continuar" value=" &#8634;" onclick="inicio();" disabled>\n'
  ss += '   <input type="button" class="boton" id="reinicio" value=" &#8635;" onclick="reinicio();" disabled>\n'
  ss += '</div></th>\n'
  ss += '<th style="font-size: 17px; background-color: lightgreen; width: 72%;">\n'
  ss += '<h2>\n'
  ss += '<a href="../../">ENEM Interativo</a>\n'
  ss += '<p style="font-size: 15px;">\n'
  ss += 'Copyright 2021 - <a href="http://ufabc.edu.br" target="_blank">UFABC</a></p></h2>\n'
  ss += 'Se necessário, aumente a fonte usando o zoom do navegador.<br>\n'
  ss += 'Recarregue esta página se nenhuma área verde aparecer em cada questão.\n'
  ss += '</th></tr></thead></table></div>\n'
  text = text.replace('<div id="page-container">', ss)

  ## botão estatíticas, no final da prova
  ss = '\n\n\n</div></div><table style="font-size: 17px; background-color: lightgreen; width: 100%;">'
  ss += '<thead><tr><th><h2>'
  ss += '<a href="../../">ENEM Interativo</a><p style="font-size: 15px;">'
  ss += 'Copyright 2021 - <a href="http://ufabc.edu.br" target="_blank">UFABC</a></p>'
  ss += '<input type="submit" value="Estatísticas" onclick="checkStatistcs(1)" style="font-size : 25px; width: 160px; height: 42px; background-color: lightblue;"/>'
  ss += '</h2></th></tr></thead></table>\n\n\n'

  # text = text.replace('</div></div>', ss)

  def rreplace(s, old, new):  # última ocorrencia
    return (s[::-1].replace(old[::-1], new[::-1], 1))[::-1]

  text = rreplace(text, '</div></div>', ss)

  if tipoProva.find('_LC_') >= 0:
    print("LC")
    text = text.replace('Questão 01', '<div id="question1"></div>', 1)
    text = text.replace('Questão 02', '<div id="question2"></div>', 1)
    text = text.replace('Questão 03', '<div id="question3"></div>', 1)
    text = text.replace('Questão 04', '<div id="question4"></div>', 1)
    text = text.replace('Questão 05', '<div id="question5"></div>', 1)

  for i in range(163, 191):
    sbug = '<span class="fc2 sc0">Questão </span><span class="fc2 sc0">' + str(i) + ' </span>'
    text = text.replace(sbug, '<div id="question' + str(i) + '"></div>')

  botoesRespostas = '<div id="question__XX__"></div>'
  for i in range(180):
    if tipoProva.find('_LC_') >= 0 and i < 99:
      qSTR = str(i + 1).zfill(2)
      ss = 'Questão ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))
      ss = 'QUESTÃO ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))
    elif i >= 99:
      qSTR = str(i + 1).zfill(3)
      ss = 'Questão ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))
      ss = 'QUESTÃO ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))
    elif tipoProva.find('_LC_') < 0 and i >= 90:
      qSTR = str(i + 1).zfill(2)
      ss = 'Questão ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))
      ss = 'QUESTÃO ' + qSTR
      text = text.replace(ss, botoesRespostas.replace('__XX__', qSTR))

  html.close()
  f2 = f[:-5] + '_INTERATIVO.html'
  print('Save: ', f2)
  html2 = open(f2, 'w')
  html2.write(text)
  html2.close()


names = [str(i).zfill(4) for i in range(2014, 2021)]
for pasta in range(len(sys.argv)):
  if sys.argv[pasta] in names:
    url = './' + sys.argv[pasta] + '/'

    dirFolders = glob.glob(url)
    dirFolders.sort(key=lambda f: int(re.sub('\D', '', f)))

    saveJSON = True
    for ano in dirFolders:

      for p in glob.glob(ano + '*'):  # rename folders
        if ' ' in p:
          pn = p.replace(' ', '_')
          os.system('mv ' + p.replace(' ', '\ ') + ' ' + pn)

      for p in glob.glob(ano + '*'):
        if 'PROVAS' in p:
          print(p)
          dirFiles = glob.glob(p + '/*.pdf')
          for f in dirFiles:
            if not ('DIGITAL' in f or 'Gab_' in f or '_GAB_' in f or 'AMPLIADA' in f or '_LIBRAS' in f or '_LEDOR' in f):
              for c in CORES:
                if c in f:
                  if 'html' in sys.argv:
                    try:
                      PdfToHtml(f)
                      pass
                    except:
                      print("ERRO in PdfToHtml:", f)

                  if 'interativo' in sys.argv:
                    try:
                      includeButtonsQuestions(f[:-3] + 'html')
                    except:
                      print("ERRO in includeButtonsQuestions:", f)
                  # exit(0)
            else:
              if not os.path.exists(p + "/OUTROS"):
                print("Create: ", p + "/OUTROS")
                os.system('mkdir ' + p + "/OUTROS")
              os.system('mv ' + f + ' ' + p + "/OUTROS")
