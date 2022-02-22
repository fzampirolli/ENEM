#!bin/bash

echo "passar 2019 e tamanho da amostra como parametros desse bash"

echo "Download dos microdados de 2019"
python enem_download.py 2019

echo "Entrada: 2019/DADOS/ITENS_PROVA_2019.csv"
echo "Saída: 2019/DADOS/ITENS_PROVA_2019.json"
python _csv2json.py 2019

echo "Inclui o campo images no json"
python _addJson.py 2019

echo "Converte arquivos PDFs da pasta 2019/PROVAS_E_GABARITOS/"
python _pdf2html.py html 2019

echo "Converte arquivos *.html da pasta 2019/PROVAS_E_GABARITOS/"
echo "para *INTERATIVO.html da pasta 2019/PROVAS_E_GABARITOS/"
python _pdf2html.py interativo 2019

echo "Inclui arquivo index.html na pasta 2019"
echo "modelo: enemANO.html"
python _createIndex.py 2019

echo "Cria a pasta 2019/FIGS com as imagens IRT"
echo "passa ano(s) e o último é o tamanho da amostra"
echo "quanto maior o tamanho, mais lento fica gerar as figuras"
python _enemToIRT.py 2019 1000

