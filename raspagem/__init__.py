#!/usr/bin/env python3
# coding: utf-8

from avalim.settings import BASE_DIR

def ChromeSessao():
    from os.path                 import join
    from platform                import system
    from selenium.webdriver      import ChromeOptions
    from undetected_chromedriver import Chrome
    
    options = ChromeOptions()
    #options.headless = True
    #options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-default-apps')
    options.add_argument("--window-size=1024,768")
    if system() == "Windows":
        options.binary_location = join(BASE_DIR, 'chrome', 'chrome.exe')
        engine_path             = join(BASE_DIR, 'chrome', 'chromedriver.exe')
    else:
        options.binary_location = join(BASE_DIR, 'chrome', 'chrome')
        engine_path             = join(BASE_DIR, 'chrome', 'chromedriver')
    
    return Chrome(options=options, executable_path=engine_path)


class Raspador():
    """Raspador do sítio Viva Real."""
    
    def __init__(self, perfil):
        self.perfil   = perfil
        self.contador = self.perfil.iniPg
        #self.engine   = ChromeSessao()
    
    def get_pags(self):
        import csv
        import time
        from   bs4                                            import BeautifulSoup
        from   datetime                                       import datetime
        from   selenium.webdriver.common.by                   import By
        from   selenium.common.exceptions                     import TimeoutException
        from   selenium.webdriver.support.ui                  import WebDriverWait
        from   selenium.webdriver.support.expected_conditions import visibility_of_element_located
        
        self.pags  = []
        self.dados = []
        dt_ini     = datetime.now()
        print("{0} - {1} - Raspagem - Início.".format(dt_ini.strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo))
        
        if self.perfil.arquivo:
            with open(self.perfil.arquivo, 'w') as csvarq:
                writer = csv.DictWriter(csvarq, fieldnames = self.perfil.campos, delimiter=';')
                writer.writeheader()
        
        
        for nPage in range(self.perfil.iniPg, self.perfil.qtdPg+1):
            self.engine   = ChromeSessao()
            
            self.engine.get(self.perfil.url.format(self.contador))
            dt_pg = datetime.now()
            print("{0} - {1} {2} - Raspando.".format(dt_pg.strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo, self.contador))
            
            try:
                pag_prox = WebDriverWait(self.engine, self.perfil.timeout).until(visibility_of_element_located((By.CSS_SELECTOR, self.perfil.ESPERA.format(nPage+1))))
                #self.engine.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #Scroll to bottom
                #self.engine.execute_script("window.scrollBy(0, 200);")
                element = self.engine.find_element(By.CSS_SELECTOR, self.perfil.ESPERA.format(nPage+1))
                self.engine.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(self.perfil.tespera)
            except TimeoutException:
                print("{0} - {1} {2} - Não encontrado.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo, self.contador))
                break
            
            self.pags.append(BeautifulSoup(self.engine.page_source, self.perfil.parser))
            dados = self.perfil.get_dados(self.pags[-1], self.perfil.url_base)
            self.dados.extend(dados)
            
            if self.perfil.arquivo:
                with open(self.perfil.arquivo, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames = self.perfil.campos, delimiter=';')
                    writer.writerows(dados)
            print("{0} - {1} {2} - Raspado. Tempo: {3}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo, self.contador, (datetime.now() - dt_pg)))
            
            if nPage < self.perfil.qtdPg:
                try:
                    pag_prox = WebDriverWait(self.engine, self.perfil.timeout).until(visibility_of_element_located((By.CSS_SELECTOR, self.perfil.PAGINADOR.format(nPage+1))))
                    #self.engine.find_element(By.CSS_SELECTOR, self.perfil.PAGINADOR.format(nPage+1)).click()
                    #self.engine.execute_script("arguments[0].click()", pag_prox)
                except TimeoutException:
                    print("{0} - {1} {2} - Não encontrado.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo, self.contador))
                    break
            
            self.contador += 1
            
            self.engine.quit()
            
        print("{0} - {1} - Raspagem - Fim. Tempo: {2}.".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self.perfil.tipo, (datetime.now() - dt_ini)))
        return self.dados

class ImovelWebListaSimples():
    """Perfil de lista simples de anúncios do sítio imobiliário Imovelweb para
       Raspadores imobiliários.
       
    url:   endereço da página inicial.
    
    iniPg: se mais de uma página for raspada, use este parâmetro como "{}"
           para que seja substituído pelo número da página.
    
    qtdPg: quantidade total de páginas. O raspador começará por iniPg e
           terminará em qtdPg.
    
    params: parâmetros da requisição da web.
    
    headers: cabeçalhos da requisição da web."""
    
    CAMPOS    = ['Endereco', 'Bairro', 'Area', 'Quartos', 'Banheiros', 'Vagas', 'Preco', 'Cond.', 'Link', 'Publicado']
    ESPERA    = 'div.paging-module__container-paging'
    # ESPERA    = 'button.l-button.l-button--appearance-iconButton.l-button--context-primary.l-button--no-label.l-button--size-regular'
    PAGINADOR = ESPERA
    # ID      = 0
    PARSERS   = ['html.parser',]
    
    def __init__(self, url, arquivo = '', campos = '*', iniPg = 1, qtdPg = 1, \
                 headers = {}, params = {}, urls_csv = '', tespera  = 3, timeout  = 20):
        self.url      = url
        self.arquivo  = arquivo
        self.campos   = campos
        self.qtdPg    = qtdPg
        self.iniPg    = iniPg
        self.headers  = headers
        self.params   = params
        self.parser   = 'html.parser'
        self.derivado = ''
        self.tipo     = 'Lista'
        self.urls_csv = urls_csv
        self.tespera  = tespera
        self.timeout  = timeout
        # self.__class__.ID += 1
        # self.id       = self.__class__.ID
    
    @property
    def campos(self):
        return self._campos
    
    @campos.setter
    def campos(self, valor):
        self._campos = None
        if isinstance(valor, list):
            self._campos = list(set(self.CAMPOS).intersection(set(valor)))
        if valor == '*':
            self._campos = self.CAMPOS
        if self._campos is None:
            print("{0} não é um objeto válido! Campos configurado como 'None'.".format(valor))
    
    @property
    def url(self):
        return self._url.geturl()
    
    @url.setter
    def url(self, valor):
        from urllib.parse import urlparse, urlunparse
        
        if valor:
            self._url     = urlparse(valor)
            self.url_base = urlunparse(self._url[:2] + ('', '', None, None))
        
    def texto_limpo(self, obj, moeda=False, aparar = True, so_num = False):
        result = obj
        if obj:
            if isinstance(obj, str):
                result = obj
            else:
                result = obj.text
            if so_num:
                texto  = result
                result = ""
                for carac in texto:
                    if carac.isdigit() or carac == "." or carac == ",":
                        result += carac
            if not moeda:
                # TODO: implement locale string replacement
                result = result.replace('R$', '')
            if aparar:
                result = result.strip()
        return result
    
    def get_dados(self, pag, url_base):
        result = []
        
        dados  = pag.find_all('div', class_="postingCardLayout-module__posting-card-container")
        
        for dado in dados:
            dado_r   = {}
            endereco = area = ''
            
            if 'Link' in self.campos:
                try:
                    link           = dado.find('a')['href']
                except:
                    link = None
                if link:
                    link           = link = url_base + link
                else:
                    link = url_base
                dado_r['Endereco'] = dado_r['Link'] = link
            
            if 'Endereco' in self.campos:
                endereco           = dado.find('div', class_="postingLocations-module__location-address postingLocations-module__location-address-in-listing")
                if not endereco:
                    endereco           = dado.find('div', class_="postingLocations-module__location-address postingLocations-module__location-address-in-listing postingLocations-module__location-address-development")
                dado_r['Endereco'] = self.texto_limpo(endereco.text)
            
            if 'Bairro' in self.campos:
                bairro           = self.texto_limpo(dado.find('h2', class_="postingLocations-module__location-text").text)
                dado_r['Bairro'] = bairro
            
            detalhes = dado.find_all('span', class_="postingMainFeatures-module__posting-main-features-span postingMainFeatures-module__posting-main-features-listing")
            i = 1
            for detalhe in detalhes:
                if i == 1:
                    dado_r['Area']      = self.texto_limpo(detalhe.text).replace(' m² tot.', '')
                if i == 2:
                    dado_r['Quartos']   = self.texto_limpo(detalhe.text).replace(' quartos', '').replace(' quarto', '')
                if i == 3:
                    dado_r['Banheiros'] = self.texto_limpo(detalhe.text).replace(' banheiro', '').replace(' ban.', '')
                if i == 4:
                    dado_r['Vagas']     = self.texto_limpo(detalhe.text).replace(' vagas', '').replace(' vaga', '')
                i += 1
                
            if 'Preco' in self.campos:
                preco           = self.texto_limpo(dado.find('div', class_="postingPrices-module__price").text).replace('.', '')
                dado_r['Preco'] = preco
            
            if 'Publicado' in self.campos:
                try:
                    publicado    = self.texto_limpo(dado.find('div', class_="postingCard-module__posting-antiquity-date").text).replace('Publicado hoje', '0').replace('Publicado desde ontem', '1').replace('Publicado há mais de ', '').replace('Publicado há ', '').replace(' dias', '')
                except:
                    publicado = None
                dado_r['Publicado'] = publicado
            
            if 'Cond.' in self.campos:
                try:
                    cond    = self.texto_limpo(dado.find('div', class_="postingPrices-module__expenses postingPrices-module__expenses-property-listing").text).replace('.', '').replace(' Condominio', '')
                except:
                    cond = None
                dado_r['Cond.'] = cond
            
            result.append(dado_r)
            
        return result
