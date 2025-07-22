# Avaliação Imobiliária (AvalIm)

Avaliador de Imóveis incluindo as fases de coleta e análise dos dados.

## 1. Instalação
1. Baixe o código e descompacte.
2. Instale as dependências:

    pip install -r requirements

3. Baixe o Chrome e ChromeDriver do sítio [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
   e coloque na pasta *chrome* na raiz da pasta *avalim*.

## 2. Utilização
### 2.1. Coleta dos Dados

A etapa de coleta de dados é essencial e pode ser executada de forma manual ou
automatizada por Raspagem (Web Scraping em inglês).

A coleta por Raspagem pode ser feita utilizando uma extensão de raspagem ou
utilizando uma das interfaces desenvolvidas: ou por meio do
[Django](https://www.djangoproject.com/), ou com a
planilha [Jupyter](https://jupyter.org/) [raspagem.ipynb](./raspagem.ipynb).

Caso seja feita por Raspagem, após um filtro e seleção dos dados desejados,
a amostra pode ser complementada manualmente com dados não
disponíveis em campos padronizados nos sítios de anúncios imobiliários.

#### 2.1.1. Manual

A coleta de dados manual pode ser feita normalmente.

Ao final, deve-se salvar os dados em um arquivo chamado *amostra_bruta.csv*.

#### 2.1.2. Utilizando a Raspagem com a extensão [WebScraper.io](https://webscraper.io/)

A coleta de dados automatizada por Raspagem pode ser feita utilizando a extensão
[WebScraper.io](https://webscraper.io/).

De forma a facilitar o uso da mesma, segue abaixo um modelo de *sitemap* para
importar (*Create new sitemap | Import Sitemap*) nessa extensão:

    {"_id":"ImovelWeb","startUrl":["https://www.imovelweb.com.br/apartamentos-venda-botafogo-rio-de-janeiro-ordem-publicado-maior.html"],
    "selectors":[{"id":"Bairro","parentSelectors":["Anúncios"],"type":"SelectorText","selector":"h2","multiple":false,"regex":""},
    {"id":"Endereço","parentSelectors":["Anúncios"],"type":"SelectorText",
    "selector":"div.postingLocations-module__location-address","multiple":false,
    "regex":""},{"id":"Área","parentSelectors":["Anúncios"],"type":"SelectorText",
    "selector":"span.postingMainFeatures-module__posting-main-features-span:nth-of-type(1)",
    "multiple":false,"regex":""},{"id":"Quartos","parentSelectors":["Anúncios"],
    "type":"SelectorText","selector":"span.postingMainFeatures-module__posting-main-features-span:nth-of-type(2)",
    "multiple":false,"regex":""},{"id":"Banheiros","parentSelectors":["Anúncios"],
    "type":"SelectorText","selector":"span:nth-of-type(3)","multiple":false,"regex":""},
    {"id":"Vagas","parentSelectors":["Anúncios"],"type":"SelectorText","selector":"span:nth-of-type(4)",
    "multiple":false,"regex":""},{"id":"Condomínio","parentSelectors":["Anúncios"],
    "type":"SelectorText","selector":"div.postingPrices-module__expenses","multiple":false,
    "regex":""},{"id":"Preço","parentSelectors":["Anúncios"],"type":"SelectorText",
    "selector":"div.postingPrices-module__[Jupyter](https://jupyter.org/)price","multiple":false,"regex":""},
    {"id":"Link","parentSelectors":["Anúncios"],"type":"SelectorElementAttribute",
    "selector":"a","multiple":false,"extractAttribute":"href"},{"id":"Anúncios",
    "parentSelectors":["_root","Próximos"],"type":"SelectorElement",
    "selector":"div.postingsList-module__card-container","multiple":true,
    "scroll":false,"elementLimit":0},{"id":"Próximos","parentSelectors":["_root","Próximos"],
    "paginationType":"auto","type":"SelectorPagination","selector":"a.paging-module__page-arrow"}]}

Ao final, deve-se salvar os dados em um arquivo chamado *amostra_bruta.csv*.

#### 2.1.3. Utilizando a Raspagem desenvolvida [raspagem.ipynb](./raspagem.ipynb)

A coleta de dados automatizada por Raspagem pode ser feita utilizando a planilha
[Jupyter](https://jupyter.org/) [raspagem.ipynb](./raspagem.ipynb), ou a
interface [Django](https://www.djangoproject.com/).

Ao final, o arquivo chamado *amostra_bruta.csv* será salvo automaticamente.

### 2.2. Preparação dos Dados [preparacao.ipynb](./preparacao.ipynb)

Como a amostra coletada dos anúncios contém dados indesejados é imprescindível
que alguns ajustes, limpezas, filtros, etc sejam realizados neles.

No arquivo [preparacao.ipynb](./preparacao.ipynb) são apresentados alguns
comandos que podem ser utilizados para essa finalidade.

É importante destacar que programas como [LibreOffice](https://pt-br.libreoffice.org/)
ou [Microsoft Excel](https://www.microsoft.com/pt-br/microsoft-365/excel)
também podem ser utilizados.

Ao final, deve-se salvar os dados no arquivo *amostra.csv*.

### 2.3. Análise de Dados [analise.ipynb](./analise.ipynb)

Etapa do projeto onde são extraídas algumas informações dos dados como, por
exemplo, as distribuições das variáveis em relação aos preços, a correlação
entre elas, etc.

### 2.4. Regressão Linear [regressao.ipynb](./regressao.ipynb)

Nessa etapa é executado o modelo de regressão linear com e sem transformações.

