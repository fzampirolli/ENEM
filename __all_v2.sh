#!/bin/bash
# ./__all.sh 2024 10000

# Interrompe a execução se algum comando falhar (segurança para pipelines de dados)
set -e

# Verifica se os argumentos foram fornecidos
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Erro: Argumentos faltando."
    echo "Uso correto: $0 <ANO> <TAMANHO_AMOSTRA>"
    echo "Exemplo: $0 2024 10000"
    exit 1
fi

echo "========================================"
echo "Iniciando processamento ENEM $1"
echo "Tamanho da amostra: $2"
echo "========================================"

echo "[1/7] Download dos microdados de $1..."
python _enem_download.py "$1"

echo "[2/7] CSV para JSON..."
echo "      Entrada: $1/DADOS/ITENS_PROVA_$1.csv"
echo "      Saída:   $1/DADOS/ITENS_PROVA_$1.json"
python _csv2json.py "$1"

echo "[3/7] Incluindo campo images no JSON..."
python _addJson.py "$1"

echo "[4/7] Convertendo PDFs para HTML (Base)..."
python _pdf2html.py html "$1"

echo "[5/7] Gerando HTML Interativo..."
python _pdf2html.py interativo "$1"

echo "[6/7] Criando index.html..."
echo "      Modelo: enemANO.html"
python _createIndex.py "$1"

echo "[7/7] Criando amostras e matrizes..."
python _enem2matriz.py "$1" "$2"

echo "----------------------------------------"
echo "SUCESSO PARCIAL."
echo "IMPORTANTE: O próximo passo (TRI) requer execução manual no COLAB:"
echo "Arquivo: _TRI-CCI-matriz.ipynb"
echo "----------------------------------------"

echo "Passo Opcional: Gerar gráficos IRT"
echo "Obs: Quanto maior a amostra ($2), mais lento."
# Para ativar, remova o # da linha abaixo:
# python _matriz2graficos.py "$1" "$2"
