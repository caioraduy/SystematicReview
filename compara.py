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
        dataframe = pandas.read_csv(arquivo_csv, delimiter=None)  # Alterei para ';' como delimitador
        if coluna_nome not in dataframe.columns:
            raise ValueError(f"A coluna '{coluna_nome}' não está presente no DataFrame.")

        dataframe_selecionado = dataframe[[coluna_nome]]
        #print(dataframe_selecionado)
        return dataframe_selecionado

    except Exception as e:
        print(f"Erro ao classificar os dados: {e}")
        return None


# Nome do arquivo CSV que você deseja criar
def exporta_lista_para_csv(sua_lista, nome_arquivo):
    # Dividir a string em uma lista de caracteres
    sua_lista = list(sua_lista)

    # Escrever a lista para o arquivo CSV
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escrever cada caractere como um elemento em uma lista
        csvwriter.writerow(sua_lista)

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
            TT[artigo] = {"LISTA1": 1}
        else:
            TT[artigo]["LISTA1"] = TT[artigo]["LISTA1"] + 1
    # faz o for na lista 2
    for i in range(0, len(lista02)):
        artigo = limpar_frase(lista02[i][0]).lower()
        # verifica se a lista 2 está presente no dicionário e adiciona qntas vezes est[a
        if artigo not in TT:
            TT[artigo] = {"LISTA2": 1}
        else:
            if "LISTA2" not in TT[artigo]:
                TT[artigo]["LISTA2"] = 0
            TT[artigo]["LISTA2"] = TT[artigo]["LISTA2"] + 1
    #print(TT)
    return TT

def compara_as_4_bases(listas_bases):
    dicionario_comparacao_geral = {}
    # faz o for na lista 1
    print(listas_bases)
    for j in range(0, len(listas_bases)):
        print(listas_bases[j])
        for i in range(0,len(listas_bases[j])):
            artigo = limpar_frase(listas_bases[j][i]).lower()
            # verifica o número de vezes que esse título existe e adiciona no dicionário
            if artigo not in dicionario_comparacao_geral:
                dicionario_comparacao_geral[artigo] = 'FILTRADO' \
                                                      ''

    return dicionario_comparacao_geral

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
    print(lista_novos_artigos)
    return lista_novos_artigos

def compara_base_2021_2024(path_2024, path_2021, titulo, arquivo_export):
    # importa os arquivos CSV
    ref01 = classificar_por_coluna(path_2024, titulo)
    ref02 = classificar_por_coluna(path_2021, titulo)

    colunas_selecionadas = [titulo]

    # Filtra as colunas selecionadas e converte em uma lista de listas
    resultados_2024 = ref01[colunas_selecionadas].values.tolist()
    resultados_2021 = ref02[colunas_selecionadas].values.tolist()

    dicionario_comparacao = compara_duas_listas(resultados_2024, resultados_2021)
    lista_novos_artigos = retorna_lista_delta(dicionario_comparacao)
    exporta_lista_para_csv(lista_novos_artigos, arquivo_export)

    return lista_novos_artigos



if __name__== '__main__':
    #SCOPUS
    NOVOS_SCOPUS =compara_base_2021_2024("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2024.csv",
                                        "C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SCOPUS2021.csv",
                                         "Title", "novos_arquivos_scopus.csv")

    # SPRINGER
    NOVOS_SPRINGER = compara_base_2021_2024("C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SPRINGER2024.csv",
                                          "C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\SPRINGER2021.csv",
                                          "Item Title", "novos_arquivos_springer.csv")

    # ACM
    NOVOS_ACM = compara_base_2021_2024('C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\ACM2024.csv',
                                            "C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\ACM2021.csv",
                                            "Title", "novos_arquivos_ACM.csv")

    # IEEE
    NOVOS_IEEE = compara_base_2021_2024('C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\IEEE2024.csv',
                                       "C:\\Users\\raduy\\PycharmProjects\\pythonProject12\\IEEE2021.csv",
                                       "Document Title", "novos_arquivos_IEEE.csv")

    lista_de_bases = [NOVOS_IEEE, NOVOS_SCOPUS, NOVOS_ACM, NOVOS_SPRINGER]

    dic_filtrados = compara_as_4_bases(lista_de_bases)

    print(dic_filtrados)