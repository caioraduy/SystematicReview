import re
import pandas
import csv

def limpar_frase(frase):
    # Remover caracteres especiais e pontuações
    frase_limpa = re.sub(r'[^a-zA-Z0-9\s]', ' ', frase)

    # Remover espaçamentos extras
    frase_limpa = re.sub(r'\s+', ' ', frase_limpa).strip()

    return frase_limpa


def classificar_por_coluna(arquivo_csv, coluna_nome):
    try:
        dataframe = pandas.read_csv(arquivo_csv, delimiter=None)
        #dataframe_classificado = dataframe.sort_values(by=coluna_nome)
        #print(dataframe_classificado)
        return dataframe

    except Exception as e:
        print(f"Erro ao classificar os dados: {e}")

# Nome do arquivo CSV que você deseja criar
def exporta_lista_para_csv(sua_lista, nome_arquivo):
# Escrever a lista para o arquivo CSV
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(sua_lista)

    print(f'A lista foi exportada para o arquivo CSV: {nome_arquivo}')


if __name__== '__main__':
    #importa os arquivos CSV
    ref01 = classificar_por_coluna("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2024.csv", "Title")
    ref02 = classificar_por_coluna("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2021.csv", "Title")
    #croa lista com o título
    lista01 = ref01["Title"]
    lista02 = ref02["Title"]


    # cria dicionário vazio
    TT = {}
    # faz o for na lista 1
    for k in lista01:
        k = limpar_frase(k).lower()
        # verifica o número de vezes que esse título existe e adiciona no dicionário
        if k not in TT:
            TT[k] = {"LISTA1": 1}
        else:
            TT[k]["LISTA1"] = TT[k]["LISTA1"] + 1
    # faz o for na lista 2
    for k in lista02:
        k = limpar_frase(k).lower()
        # verifica se a lista 2 está presente no dicionário e adiciona qntas vezes est[a
        if k not in TT:
            TT[k] = {"LISTA2": 1}
        else:
            if "LISTA2" not in TT[k]:
                TT[k]["LISTA2"] = 0
            TT[k]["LISTA2"] = TT[k]["LISTA2"] + 1
    # cria lista vazia para adicionar os arquivos
    lista_novos_artigos = []
    # se está na lista 1 e não está na 2 trata-se de um artigo novo
    for k, v in TT.items():
        if "LISTA1" in v and "LISTA2" not in v:
            for i in range(0, TT[k]['LISTA1']):
                artigo =[]
                artigo.append(k)
                lista_novos_artigos.append(artigo)
            print(TT[k]['LISTA1'])
            i += TT[k]['LISTA1']
    # se está na lista 1 e não está na 2 trata-se de um artigo que não aparece mais na string de busca
    for k, v in TT.items():
        if "LISTA2" in v and "LISTA1" not in v:
            i -= TT[k]['LISTA2']
    # se o mesmo nome aparece 2 vezes na base 1 e passa a aparecer 4.
    #  O artigo aumentou o número de repetições
    for k,v in TT.items():
        if "LISTA2" in v and "LISTA1" in v:
            atigos_que_aumenta_o_numero_de_repeticoes = TT[k]["LISTA1"] - TT[k]['LISTA2']
            if atigos_que_aumenta_o_numero_de_repeticoes > 0:
                print(f'O artigo {k} passa a aparecer  {atigos_que_aumenta_o_numero_de_repeticoes} vezes ')
                i += atigos_que_aumenta_o_numero_de_repeticoes
                for i in range(0, atigos_que_aumenta_o_numero_de_repeticoes):
                    artigo = []
                    artigo.append(k)
                    lista_novos_artigos.append(artigo)





    #print(lista_novos_artigos)
    print("count",i)
    exporta_lista_para_csv(lista_novos_artigos, "novos_arquivos_scopus.csv")