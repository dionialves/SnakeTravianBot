import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class Village(object):
    def __init__(self):
        self.server = str()
        self.username = str()
        self.password = str()
        self.browser = None
        self.is_logged = False

        self.villages = {}
        self.fields = {}
        self.building_ordens = {}
        self.resources = {}
        self.order_queue = None

    def instance_browser(self):
        """
        Essa função é responsável por inicializar a instancia do navegador
        """

        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.browser.implicitly_wait(1)

    def login(self, server, username, password):
        """
        Essa função é responsável por logar na pagina do travian
        """
        self.instance_browser()
        
        self.server = server
        self.username = username
        self.password = password
        self.server = 'https://' + self.server

        self.browser.get(self.server)

        username = self.browser.find_element(By.NAME, 'name')
        password = self.browser.find_element(By.NAME, 'password')

        username.send_keys(self.username)
        password.send_keys(self.password)

        self.browser.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/form/table/tbody/tr[5]/td[2]/button").click()

        self.check_for_login()

    def check_for_login(self):
        """
            Verifica se o objeto realmente esta logado no servidor
        """
        if self.browser.current_url == self.server + '/dorf1.php':
            self.is_logged = True

        else:
            self.is_logged = False

    def update_fields_village(self, village, idsFields):
        """
            Atuliza os campos de construção da aldeia, conforme o id passado pela na função.
        """

        self.browser.get(self.villages[village]['url'])

        for id in idsFields:
            self.browser.get(f'{self.server}/build.php?id={id}')
            name = self.browser.find_elements(By.XPATH, '//*[@id="content"]/h1')[0].text

            if self.browser.find_elements(By.CLASS_NAME, 'buildingWrapper'):
                name_and_level = ['Zona Livre', '0']
            else:
                name_and_level = self.separate_name(name)

            self.fields[village]['name'][int(id)-1] = name_and_level[0]
            self.fields[village]['level'][int(id)-1] = name_and_level[1]

    def update_all_fields_village(self, village):
        """
            Atuliza todos os campos de construção da aldeia, do 1 ao 40. De uma aldeia em uma aldeia específica
        """
        fields = {}
        list_fields = []
        list_level = []

        self.browser.get(self.villages[village]['url'])

        for x in range(1,41):
            self.browser.get(f'{self.server}/build.php?id={x}')
            name = self.browser.find_elements(By.XPATH, '//*[@id="content"]/h1')[0].text

            if self.browser.find_elements(By.CLASS_NAME, 'buildingWrapper'):
                name_and_level = ['Zona Livre', '0']
            else:
                name_and_level = self.separate_name(name)

            list_fields.append(name_and_level[0])
            list_level.append(name_and_level[1])

        fields['name'] = list_fields
        fields['level'] = list_level

        self.fields[village] = fields


    def update_name_villages(self):
        """
        Autiliza o nome da aldeia e também sua URL de acesso
        """

        self.browser.get(self.server + '/dorf3.php')
        drive = self.browser.find_elements(By.XPATH, '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]')

        list_village = []
        if drive:
            drive = drive[0].text
            drive = drive.split('\n')

            for x in drive:
                aux = x.replace('\u202d', '').replace('\u202c', '')
                if aux and (aux[:1] != '('):
                    list_village.append(aux)

        for village in list_village:

            xpathUrl = self.browser.find_elements(By.XPATH, '//*[@id="overview"]/tbody/tr/td[1]/a')
            for i in xpathUrl: url = i.get_attribute("href")

            id_village = url.split('=')[1]

            self.villages[village] = {'url': url,
                                      'id': id_village}

    def update_building_orders(self, village):
        """
        Escaneia de todas de uma ldeia específica as ordens de construção.
        """

        self.browser.get(self.villages[village]['url'])

        drive = self.browser.find_elements(By.XPATH, '//*[@id="contentOuterContainer"]/div/div[2]/div[1]/ul')

        orders = []
        if drive:
            # Ajustando string
            drive = drive[0].text
            drive = drive.split('\n')

            # Obtendo as informações da primeira ordem de construção
            orders.append(self.separate_name(drive[0]))
            orders[0].append(self.convert_string_to_secunds(drive[1]))

            # Obtendo informações da segunda ordem de construção
            if len(drive) == 4:
                orders.append(self.separate_name(drive[2]))
                orders[1].append(self.convert_string_to_secunds(drive[3]))

        self.building_ordens[village] = orders

    def get_resources(self, village):
        """
        Escaneia os recursos disponíveis em uma aldeia

        Criar um validador de informação, pois o recurso lumber esta retornando com a seguinte informação: \u202d2878\u202c
        """

        self.browser.get(self.villages[village]['url']) 

        self.browser.implicitly_wait(4)

        lumber = self.browser.find_element(By.ID, 'l1').text
        clay = self.browser.find_element(By.ID, 'l2').text
        iron = self.browser.find_element(By.ID, 'l3').text
        crop = self.browser.find_element(By.ID, 'l4').text

        self.resources[village] = {
            "lumber": lumber.replace('.', ''),
            "clay": clay.replace('.', ''),
            "iron": iron.replace('.', ''),
            "crop": crop.replace('.', '')
        }

    def upgrade_fields_resource(self, village, idField):
        """
        Nesta função realizaremos a construção ou o upgrade de recursos, recebendo a aldeia e o id do campo
        """

        self.browser.get(self.villages[village]['url'])
        self.browser.get(self.server + '/build.php?id=' + str(idField))
        buttonUpgrade = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[3]/div[1]/button')
        
        buttonUpgrade.click()

    def start_all_farm_list(self, idVillage):
        """
        Nesta função iniciamos o assalto de todas as listas de farms contidas na aldeia
        """

        self.browser.get(self.villages[idVillage]['url'])
        self.browser.get(self.server + '/build.php?id=39&gid=16&tt=99')

        buttonStartAllList = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div[3]/div/div[1]/div[2]/button[1]')
        buttonStartAllList.click()


    def check_construction_resources(self, idField):
        """
        Esta função checa se na aldeia tem os recursos necessários para a construção desejada
        """

        self.browser.get(self.server + '/build.php?id=' + str(idField))

        lumber = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[1]/span').text
        clay = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/span').text
        iron = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[3]/span').text
        crop = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[4]/span').text
    
        return {'lumber': lumber.replace('.', ''), 'clay': clay.replace('.', ''), 'iron': iron.replace('.', ''), 'crop': crop.replace('.', '')}


    def separate_name(self, name):
        """
        Utilitário para limpar a string recebida do site
        """
        result = []
        result.append(name[0:name.find('N')-1])
        result.append(name[len(name)-2:len(name)].split()[0])
        return result
    
    def convert_string_to_secunds(self, time):
        construction = time.split(':')
        secunds = (int(construction[0])*3600) + (int(construction[1])*60) + int(construction[2][0:2])

        return secunds

    def close_browser(self, *args):
        """
        Responsável por fechar o navegador interno
        """
        
        self.is_logged = False
        self.browser.close()