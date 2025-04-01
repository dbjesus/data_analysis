from collections import defaultdict
import pandas as pd
from os.path import isfile
import sys
def ordenar_parametros(values, param_names):
    '''recebe uma linha que do aquivo.dat, no caso especifico, 2ome.dat, cria um dicionario, onde a chave eh o chi2
    o restante dos parametros sao os que sao apresentados no arquivo.var
    retorna o dicionario de parametros com os nomes dos parametros em cada uma das colunas.'''
    parametros_medios= defaultdict(float)
    for chi, l_valores in values.items():
        for i,j in zip(param_names,l_valores):
            parametros_medios[i]+=float(j)
    print("Proceeding...\n")
    if parametros_medios:
        return parametros_medios
def treat_dict(dict_):
    print(f"O tamanho do dicionario eh: {len(dict_)}")
    for key, values in dict_.items():
        dict_[key]=[float(value)/len(dict_) for value in values]
    return dict_ #pd.DataFrame.from_dict(dic)
def df_sorted(arquivo):
    '''recebe uma aquivo.txt com a lista de parametros 
    com o primeiro parametro sendo o chi2 e cria dicionario com o chi2 sendo a chave
    retorna o dicionario'''
    defd= defaultdict(float) 
    with open(arquivo,'r') as file:
        #print("Os chi2's que serao utilizados sao:\n")
        print("The used Chi2 values are:\n")
        for line in file:
            defd[line.split()[0]]=line.split()[1:]
            print(line.split()[0],"\n")
        brecar=input("Is this what you want? y/n\n")
        if brecar.upper()=="N":
            print("Exiting")#    break
            sys.exit(0)
        #else:print("Proceeding...")
    file.close()
    return defd
def names(file_var001_address):
    arquivo_nomes=str(file_var001_address)
    #extrair os nomes dos parametros em sequencia e colocar em uma lista
    names=[]
    with open(arquivo_nomes, "r") as file:
        for line in file.readlines()[1:]:
            #print(line.split()[0])
            names.append(line.split()[0])
    file.close()
    return names
def save_file_par(df):
    #print("Constuindo o arquivo de saida .par\n")
    print("Working on output file.par\n")
    #output_file_name=input("Digite o nome do arquivo de saida.\n") 
    output_file_name=input("Write the output file name\n")
    with open(f"{output_file_name}.par", "w") as file:
        #cabecalho
        file.write("average-std\n")
        #print("O arquivo salvo tem o seguinte formato:\n")
        #print("The file format is:\n")
        #print("average-std\n")
        for i,j in df.items():
        #    print(i," ",j)
            file.write(f"{i} {j}\n")
    file.close()
    #Checking if file is saved
    #print(f"Salvando arquivo {output_file_name}.par\n")
    print(f"Saving file {output_file_name}.par\n")
    if not isfile(f"{output_file_name}.par"):
        raise IOError("File <%s> not save!\n" % output_file_name)
    #print("Arquivo salvo!\n")
    print("File saved!\n")
def general_call(file_values, file_names):
    #save_file_par(ordenar_parametros(treat_dict(df_sorted(file_values),len(dict_)),names(file_names)))
    save_file_par(ordenar_parametros(treat_dict(df_sorted(file_values)),names(file_names)))  
    #return df

def main() -> None:
    file_values=str(input("Digite o endereco do arquivo de valores de parametros.\nGeralmente, ele se encontra em um <arquivo>.dat\n"))
    file_names=str(input("Digite o endereco do <arquivo>.var.00001 que o programa retornou.\n"))
    general_call(file_values,file_names)
'''
import sys

def main():
    if len(sys.argv) != 3:
        print("Uso: python meu_script.py <arquivo_valores> <arquivo_nomes>")
        sys.exit(1)

    file_values = sys.argv[1]
    file_names = sys.argv[2]
    general_call(file_values, file_names)
'''
if __name__ == '__main__':
    main()
