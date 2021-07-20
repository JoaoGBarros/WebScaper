# WebScaper
Script Web Scraper desenvolvido em Python utilizando as bibliotecas Selenium, BeautifulSoup e Pandas


O programa é feito de modo que o usuário digita o produto que deseja e o nome que deseja que o arquivo .csv possua, após isso o programa acessa o site https://www.mercadolivre.com.br/ utilizando o chrome driver e rapidamente coleta os dados e depois mostra os resultados no arquivo. O programa também faz um proceso de filtragem dos produtos, so lendo e armazendando dados que possuam o produto buscado. Ex: Caso vc porcure "Mario Party Switch", so sera armazenado os produtos que possuam no nome "Mario Party Switch", evitando assim a tediosa busca por precos e produtos.

A tabela .csv eh composta por 4 colunas:
  . Nome - Titulo do anuncio no site
  . Preco - Preco do anunciante
  . Frete - Caso o frete seja grátis ou não
  . Link - Link direto para o produto de sua escolha


Pagina de download do ChromeDriver: https://chromedriver.chromium.org/downloads

Utilize o programa na mesma pasta que o ChromeDriver, caso execute o terminal o erro que aparece pode ser desconsiderado

Espere a janela do Chrome fechar para abrir o arquivo .csv

