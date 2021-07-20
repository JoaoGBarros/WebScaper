import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import os


def produtoCerto(produto_encontrado, produto_procurado):

    #  Funcao que compara o titulo do anuncio encontrado com o produto procurado. Caso todas as palavras do produto
    # procurado estejam presentes, retorna True, caso nao, retorna False

    soma = 0
    for i in range(len(produto_procurado)):
        if produto_procurado[i] in produto_encontrado:
            soma += 1

    if soma == len(produto_procurado):
        return True
    else:
        return False


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    site = "https://www.mercadolivre.com.br/" #Site que sera utilizado
    print("------- Servico de Busca Automatizada no site " + site + " -------")
    produto = input("Produto que deseja buscar: ")
    arquivo = input("Nome do arquivo que sera gerado: ")
    arquivo = arquivo + '.csv'
    lista_links = []
    lista_titulos = []
    lista_precos = []
    lista_fretes = []
    local = os.getcwd()  # Pede ao usuario o local do Chrome Driver
    local = local + "/chromedriver.exe"
    print("Espere a janela do Chrome fechar para abrir o arquivo .csv")
    navegador = webdriver.Chrome(local, options=options)   # Abre o executavel do chrome driver
    navegador.minimize_window()
    navegador.get(site)  #Entra no site
    pesquisa = navegador.find_element_by_class_name('nav-search-input')  # Procura pelo elemento da barra de pesquisa
    # utilizando sua classe no html
    pesquisa.send_keys(produto)  # Digita na barra de pesquisa o produto
    pesquisa.send_keys(Keys.RETURN)  # ENTER
    navegador.implicitly_wait(5)  # Espera 2 segundos antes de comecar a coleta de dados para dar tempo da pagina
    # carregar completamente
    conteudo = navegador.page_source
    soup = BeautifulSoup(conteudo, features="html.parser")  # Cria um novo objeto de BeautifulSoup contendo as
    # informacoes da pagina
    existe_proxima = True  # Inicia a condicao para o loop


    while existe_proxima:
        proxima = None  # Inicializa a verificacao para caso exista uma proxima pagina

        #  Faz a busca dentro da div que possua a classe especificada
        for a in soup.find_all('div', attrs={'class': 'ui-search-result__wrapper'}):
            # a.find -> De todos os elementos presentes dentro da div, procura os com as especificacoes
            nome = a.find('div', attrs={'class': 'ui-search-item__group ui-search-item__group--title'})
            if produtoCerto(nome.text, produto):
                #  Caso a condicao seja verdadeira, armazena os dados do anuncio
                link = a.find('a', attrs={'class': 'ui-search-link'})
                if "click" not in link.attrs['href']:
                    lista_links.append(link.attrs['href'])
                preco = a.find('span', attrs={'class': 'price-tag-amount'})
                frete = a.find('p', attrs={'class': 'ui-search-item__shipping ui-search-item__shipping--free'})
                lista_titulos.append(nome.text)
                lista_precos.append(preco.text)
                if isinstance(frete, type(None)):
                    lista_fretes.append("Sem fretis gratis")
                else:
                    lista_fretes.append(frete.text)

        #  Procura pelo botao para mudar de pagina, seguindo apenas para proximas paginas
        for a in soup.find_all('div', attrs={'class': 'ui-search-pagination'}):
            proxima = a.find('a', attrs={'class': 'andes-pagination__link ui-search-link', 'title': 'Seguinte'})


        # Caso a proxima pagina nao exista, o loop eh finalizado
        if isinstance(proxima, type(None)):
            existe_proxima = False
            navegador.quit()  #Fecha o navegador
        else:
            # Caso contrario o programa carrega a proxima pagina
            site = proxima.attrs['href']
            navegador.get(site)
            conteudo = navegador.page_source
            soup = BeautifulSoup(conteudo, features="html.parser")

    # Criacao do .csv utilizando o nome dado pelo usuario

    if not os.path.exists("Relatorios"):
        os.mkdir("Relatorios")
    arquivo = os.getcwd() + "/Relatorios/" + arquivo
    data = pd.DataFrame(zip(lista_precos, lista_titulos, lista_fretes, lista_links), columns=['Preco', 'Produto', 'Frete', 'Link'])
    data.to_csv(arquivo, index=False, encoding='utf-8')

    print("Fim do programa! O .csv esta disponivel na pasta Relatorios!")

