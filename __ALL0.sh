#!/bin/bash

# Executa de 1998 até 2024
for ano in {1998..2024}; do
    source __all.sh "$ano" 10000
done
