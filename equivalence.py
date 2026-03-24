
#!/usr/bin/env python3

'''
Como script via terminal, execute python equivalence.py folder
folder deve conter o arquivo submit.sh e o arquivo nm.nm.
O autocomplete funcionara

Como biblioteca via python, inclua:
import equivalence

equivalence.eq_rule("folder")

OBS: Se o arquivo de submissao e de nome nao forem, 
submit.sh e nm.nm, respectivamente,
voce precisa alterar os nomes dentro deste programa e adequa-lo a sua necessidade.

uso em sequencia:
for f in $(ls -d */); do python3 equivalence.py "$f"; echo "$f"; wait; done

o wait eh recomendado se o numero de diretorios for grande ou se utilizar processamento paralelo
com mais processos que nucleos
'''

def eq_rule(path):
    #funcao1 retornar a regra de equivalencia
    
    """
    Esta funcao recebe a pasta onde esta o submit.sh e retorna uma lista de listas com as regras de equivalencia
    regras de equivalencia salvas na lista de regras sao do tipo:
    [
    [dimero0,dimeros_correspondente0],
    [dimero1,dimeros_correspondente1],
    ...
    ]
    Uso: regras = eq_rule(path)
    """
    
    with open(path+"submit.sh") as file:
        lines=file.readlines()
        for word in lines[3].split('-var=')[1].split('<')[0].split():
            lista_dimeros=word.split(",")
    # achar as regras de equivalencia
    regras=[]
    for i in lista_dimeros:
        if "=" in i:
            regras.append(i.split("="))
    return regras
#regras = eq_rule(path)
#funcionou

# regras
# verificar se cada item na lista regras[i][a] existe no aruqivo de parametros
# Se o dimero existir, o segundo dimero, regras[i][b], eh associado ao valor extraido do arquivo de parametros
#

def map_val_err(path):
    #funcao2 retornar os dois mapas
    """
    Recebe o diretorio onde se encontra o arquivo nm-av-std-1000.dat
    Retornar dois mapas 
        1. Mapa de valores dos parametros resultado do varpar: mapa_val
        2. Mapa de valores dos erros de parametros resultado do varpar: mapa_err
        Uso: mapa_val,mapa_err = map_val_err(path)
    """
    
    dimero = []
    param = []
    err = []
    header = str
    

    with open(path+"nm-av-std-1000.dat") as file2:
        header = file2.readline()
        lines = iter(file2.readlines())
        next(lines)
        lines = list(lines)
        for i in lines:
            dimero.append(i.split()[0])
            param.append(i.split()[1])
            err.append(i.split()[2])
            
    mapa_val = dict(zip(dimero,param))
    mapa_err = dict(zip(dimero,err))

    return mapa_val, mapa_err, dimero, header
#mapa_val,mapa_err = map_val_err(path)
#funcionou

#funcao3 salvar o arquivo
#salvando o novo arquivo de parametros
#def param_save(path,mapa_val,mapa_err):
def param_save(path, mapa_val, mapa_err, regras, dimero, header):

    """
    Recebe o caminho da pasta e salva o arquivo de parametros nm-av-std.dat
    O arquivo contem os parametros e os correspondentes parametros das regras de equivalencia
    Extraida do arquivo submit
    Uso: param_save(path) 
    """
    import os
    print(f"Criando o arquivo nm-av-std.dat na pasta {path}\n")
    archive = path+"nm-av-std.dat"
    with open(archive,"w") as f:
        f.write(f"{header}")
        print(f"Gravando os dados ja existentes no arquivo")
        for d in dimero:
            f.write(f"{d}{mapa_val[d]} {mapa_err[d]}\n")
        print(f"Gravando os dados equivalentes")
        for r in regras:
            f.write(f"{r[1]} {mapa_val[r[0]]}{mapa_err[r[0]]}\n")
    #checar se o arquivo esta salvo
    try:
        with open(archive, "w") as f:
            f.write("dados...\n")
        print("Arquivo criado com sucesso")
    except Exception as e:
        print("Erro ao criar arquivo:", e)


import sys

def main():
    '''
    Para rodar, execute no terminal:
    python equivalence.py diretorio

    escreva a pasta seguida da barra: "/"
    '''
    
    if len(sys.argv) < 2:
        print("Uso: python equivalence.py <diretorio>")
        sys.exit(1)

    path = sys.argv[1]

    if "/" not in path:
        path += "/"

    regras = eq_rule(path)
    mapa_val, mapa_err, dimero, header = map_val_err(path)
    param_save(path, mapa_val, mapa_err, regras, dimero, header)
