#!bin/bash
# exemplo de uso
# ./__all.sh 2024 10000

echo "ano: $1"
echo "tamanho da amostra: $2"

echo "Download dos microdados de $1"
python _enem_download.py $1

echo "Entrada: $1/DADOS/ITENS_PROVA_$1.csv"
echo "Saída: $1/DADOS/ITENS_PROVA_$1.json"
python _csv2json.py $1

echo "Inclui o campo images no json"
python _addJson.py $1

echo "Converte arquivos PDFs da pasta $1/PROVAS_E_GABARITOS/"
python _pdf2html.py html $1

echo "Converte arquivos *.html da pasta $1/PROVAS_E_GABARITOS/"
echo "para *INTERATIVO.html da pasta $1/PROVAS_E_GABARITOS/"
python _pdf2html.py interativo $1

echo "Inclui arquivo index.html na pasta $1"
echo "modelo: enemANO.html"
python _createIndex.py $1

echo "Cria amostras"
python _enem2matriz.py $1 $2

echo "ATENÇÃO: Rodar no COLAB: _TRI-CCI-matriz.ipynb"

echo "Cria a pasta $1/FIGS com as imagens IRT"
echo "passa ano(s) e o último é o tamanho da amostra"
echo "quanto maior o tamanho, mais lento fica gerar as figuras"
#python _matriz2graficos.py $1 $2
