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

def adiciona_artigo_na_lista(lista, numero_elementos, artigo):
    for i in range(0, numero_elementos):
        artigo_lista = []
        artigo_lista.append(artigo)
        lista.append(artigo)
    return lista

def compara_duas_listas(lista01,lista02):
    TT = {}
    # faz o for na lista 1
    for i in range(0,len(lista01)):
        artigo = limpar_frase(lista01[i][0]).lower()
        # verifica o número de vezes que esse título existe e adiciona no dicionário
        if artigo not in TT:
            TT[artigo] = {"LISTA1": 1, "ANO": lista01[i][1]}
        else:
            TT[artigo]["LISTA1"] = TT[artigo]["LISTA1"] + 1
    # faz o for na lista 2
    for i in range(0, len(lista02)):
        artigo = limpar_frase(lista02[i][0]).lower()
        # verifica se a lista 2 está presente no dicionário e adiciona qntas vezes est[a
        if artigo not in TT:
            TT[artigo] = {"LISTA2": 1,"ANO": lista02[i][1]}
        else:
            if "LISTA2" not in TT[artigo]:
                TT[artigo]["LISTA2"] = 0
            TT[artigo]["LISTA2"] = TT[artigo]["LISTA2"] + 1
    print(TT)
    return TT

def retorna_lista_delta(TT):
    i=0
    lista_novos_artigos = []
    # se está na lista 1 e não está na 2 trata-se de um artigo novo
    for k, v in TT.items():
        if "LISTA1" in v and "LISTA2" not in v:
            lista_novos_artigos= adiciona_artigo_na_lista(lista_novos_artigos, TT[k]['LISTA1'],k)
            i += TT[k]['LISTA1']

    # se está na lista 1 e não está na 2 trata-se de um artigo que não aparece mais na string de busca
    for k, v in TT.items():
        if "LISTA2" in v and "LISTA1" not in v:
            print(f'O artigo com o título "{k}" deixa de existir na string de busca')
            i -= TT[k]['LISTA2']
    # se o mesmo nome aparece 2 vezes na base 1 e passa a aparecer 4.
    #  O artigo aumentou o número de repetições
    for k, v in TT.items():
        if "LISTA2" in v and "LISTA1" in v:
            artigos_que_aumenta_o_numero_de_repeticoes = TT[k]["LISTA1"] - TT[k]['LISTA2']
            if artigos_que_aumenta_o_numero_de_repeticoes > 0:
                print(f'O artigo com o título "{k}" deve ser contabilizado {artigos_que_aumenta_o_numero_de_repeticoes} vezes, '
                      f'pq o número de repetições aumentou ')

                i += artigos_que_aumenta_o_numero_de_repeticoes
                lista_novos_artigos = adiciona_artigo_na_lista(lista_novos_artigos, artigos_que_aumenta_o_numero_de_repeticoes, k)

    print(f'O delta entre as lista é {i}')
    return lista_novos_artigos



if __name__== '__main__':
    #importa os arquivos CSV
    ref01 = classificar_por_coluna("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2024.csv", "Title")
    ref02 = classificar_por_coluna("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2021.csv", "Title")
    #croa lista com o título

    colunas_selecionadas = ["Title", "Year"]

    # Filtra as colunas selecionadas e converte em uma lista de listas
    SCOPUS2024 = ref01[colunas_selecionadas].values.tolist()
    SCOPUS2021 = ref02[colunas_selecionadas].values.tolist()

    dicionario_comparacao_SCOPUS = compara_duas_listas(SCOPUS2024, SCOPUS2021)
    lista_novos_artigos_SCOPUS = retorna_lista_delta(dicionario_comparacao_SCOPUS)
    exporta_lista_para_csv(lista_novos_artigos_SCOPUS, "novos_arquivos_scopus.csv")