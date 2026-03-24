#!/usr/bin/env bash

pasta="$1"
entrada="$2"
saida="$3"

# validar argumentos
if [ -z "$pasta" ] || [ -z "$entrada" ] || [ -z "$saida" ]; then
    echo "Uso: ./source.sh <pasta> <arquivo_entrada> <nome_saida>"
    exit 1
fi

# garantir barra no final
pasta="${pasta%/}/"

# validar se arquivo existe
if [ ! -f "${entrada}" ]; then
    echo "Erro: arquivo de entrada não encontrado"
    exit 1
fi

echo "Pasta: $pasta"
echo "Entrada: $entrada"
echo "Saída: $saida"

# executar tfreg
tfreg \
-data=./../seq_nm_rna_120.dat \
-par=../ref_regra.par,../rna_pb_121_un_f1.par,"${entrada}" \
-expand=lG_lG \
-m=pb \
-t=370 \
-res=regression \
-pm=2 \
-cutoff=10 \
-int=-1:200/400 \
-o="${pasta}${saida}" \
-dict=k:k,l:l,m:m,o:o \
-printusedpar=1 \
-v &> "${pasta}${saida}.echo"
