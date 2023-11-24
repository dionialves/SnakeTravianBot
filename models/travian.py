import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



BUILDING = {
    'gid0': 'Empty',
    'gid1': 'Woodcutter',
    'gid2': 'Clay Pit',
    'gid3': 'Iron Mine',
    'gid4': 'Cropland',
    'gid5': 'Sawmill ',
    'gid6': 'Brickyard',
    'gid7': 'Iron Foundry',
    'gid8': 'Grain Mill',
    'gid9': 'Bakery',
    'gid10': 'Warehouse',
    'gid11': 'Granary',
    'gid12': 'None',
    'gid13': 'Smithy',
    'gid14': 'None',
    'gid15': 'Main Building',
    'gid16': 'Rally Point',
    'gid17': 'Marketplace',
    'gid18': 'Embassy',
    'gid19': 'Barracks',
    'gid20': 'Stable',
    'gid21': 'Workshop',
    'gid22': 'Academy',
    'gid23': 'Cranny',
    'gid24': 'Town Hall',
    'gid25': 'Residence',
    'gid26': 'Palace',
    'gid27': 'None',
    'gid28': 'None',
    'gid29': "None",
    'gid30': 'None',
    'gid31': 'None',
    'gid32': 'Earth Wall',
    'gid33': 'Palisade',
    'gid34': "Stonemason's Lodge",
    'gid35': "None",
    'gid36': "None",
    'gid37': "Hero's Mansion",
    'gid38': "None",
    'gid39': "None",
    'gid40': "None",
    'gid41': "None",
    'gid42': "Stone Wall"
}

TROOPS = {
    'Roman': {
        'Legionnaire': 't1',
        'Praetorian': 't2',
        'Imperian': 't3',
        'Equites Legati': 't4',
        'Equites Imperatoris': 't5',
        'Equites Caesaris': 't6',
        'Battering ram': 't7',
        'Fire Catapult': 't8',
        'Senator': 't9',
        'Settler': 't10'
    },
    'Teuton': {
        'Clubswinger': 't1',
        'Spearman': 't2',
        'Axeman': 't3',
        'Scout': 't4',
        'Paladin': 't5',
        'Teutonic Knight': 't6',
        'Ram': 't7',
        'Catapult': 't8',
        'Chief': 't9',
        'Settler': 't10'
    },
    'Gaul': {
        'Phalanx': 't1',
        'Swordsman': 't2',
        'Pathfinder': 't3',
        'Theutates Thunder': 't4',
        'Druidrider': 't5',
        'Haeduan': 't6',
        'Ram': 't7',
        'Trebuchet': 't8',
        'Chieftain': 't9',
        'Settler': 't10'
    },
    'Egyptian': {
        'Slave Militia': 't1',
        'Ash Warden': 't2',
        'Khopesh Warrior': 't3',
        'Sopdu Explorer': 't4',
        'Anhur Guard': 't5',
        'Resheph Chariot': 't6',
        'Ram': 't7',
        'Stone Catapult': 't8',
        'Nomarch': 't9',
        'Settler': 't10'
    },
    'Hun': {
        'Mercenary': 't1',
        'Bowman': 't2',
        'Spotter': 't3',
        'Steppe Rider': 't4',
        'Marksman': 't5',
        'Marauder': 't6',
        'Ram': 't7',
        'Catapult': 't8',
        'Logades': 't9',
        'Settler': 't10'
    }

}

class Travian(object):
    def __init__(self):
        self.server = str()
        self.username = str()
        self.password = str()
        self.browser = None
        self.villages = {}
        self.fields = {}
        self.upgrade_orders = {}
        self.resources = {}
        self.troops = {}
        self.farmlist = {'active': False, 'village': None}
        self.logged = False

    def instance_browser(self):
        """
        Essa função é responsável por inicializar a instancia do navegador
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.add_argument("--headless=new")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        self.browser.implicitly_wait(3)

    def login(self, server, username, password):
        """
        Essa função é responsável por logar na pagina do travian
        """
        self.instance_browser()
        
        self.server = server
        self.username = username
        self.password = password
        if not 'https://' in self.server:
            self.server = 'https://' + self.server

        self.browser.get(self.server)

        username = self.browser.find_element(By.NAME, 'name')
        password = self.browser.find_element(By.NAME, 'password')

        username.send_keys(self.username)
        password.send_keys(self.password)

        self.browser.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/form/table/tbody/tr[5]/td[2]/button").click()

        self.is_logged_in()

    def update_initial_information(self):
        # Obtem o nome das aldeias
        self.get_name_villages()
        # Obtem o nome da tribo
        self.get_tribe()
        # Atualiza todos os slots de todas as aldeias

    def update_all(self):
        self.update_initial_information()
        self.update_only_slots()

    def update_only_slots(self):
        # Atualiza as construções e seus leveis de cada aldeia
        for village in self.villages:
            # Acessa a aldeia 
            self.browser.get(self.villages[village]['url']) 
            # inicializando a slot como um dicionário
            self.villages[village]['slot'] = {}
            # Atualizando cada aldeia, recursos e construções
            self.get_slots_resources(village)
            self.get_slots_buildings(village)

    def update_only_slot(self, village, slot):
        
        self.browser.get(self.villages[village]['url'])
        self.browser.get(f'{self.server}/build.php?id={str(slot)}&tt=0')

        xpath = '//*[@id="build"]'

        element = self.browser.find_elements(By.XPATH, xpath)

        if element:                                 
            list_class = element[0].get_attribute('class').split()

            level = list_class[1]
            level = level.split('level')
            level = level[1]

            self.villages[village]['slot'][slot]['level'] = level

    def get_tribe(self):
        self.browser.get(f'{self.server}/profile')

        if self.browser.find_elements(By.CLASS_NAME, "gaul"):
            self.tribe = 'Gaul'
        elif self.browser.find_elements(By.CLASS_NAME, "teuton"):
            self.tribe = 'Teuton'
        elif self.browser.find_elements(By.CLASS_NAME, "egyptian"):
            self.tribe = 'Egyptian'
        else:
            self.tribe = 'Roman'

    def get_slots_resources(self, village):
        """
            Atuliza todos os campos de construção da aldeia, do 1 ao 40. De uma aldeia em uma aldeia específica
        """

        self.browser.get(f'{self.server}/dorf1.php')

        for x in range(2, 20):

            elemento = self.browser.find_element(By.XPATH, f'//*[@id="resourceFieldContainer"]/a[{x}]')
            list_class = elemento.get_attribute('class').split()

            if 'underConstruction' in list_class:
                del list_class[5]

            slot = (list_class[4].split('buildingSlot')[1])
            name = (BUILDING[list_class[3]])

            level = (list_class[5].split('level')[1])

            self.villages[village]['slot'].update(
                {
                    slot: {
                        'name': name,
                        'level': level
                    }
            })

    def get_slots_buildings(self, village):

        self.browser.get(f'{self.server}/dorf2.php')
        

        for x in range(1, 23):

            # Ger information on slot
            elemento = self.browser.find_element(By.XPATH, f'//*[@id="villageContent"]/div[{x}]')
             
            list_class = elemento.get_attribute('class').split()

            slot = (list_class[1].split('a')[1])
            name = (BUILDING[f'gid{list_class[2].split("g")[1]}'])

            if name != 'Empty':
                level = self.browser.find_element(By.XPATH, f'//*[@id="villageContent"]/div[{x}]/a/div').text
            else:
                level = '0'

            self.villages[village]['slot'].update(
                {
                    slot: {
                        'name': name,
                        'level': level
                    }
            })

    def get_name_villages(self):
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

        for x in range(0, len(list_village)):

            if self.browser.find_elements(By.XPATH, f'//*[@id="overview"]/tbody/tr[{x+1}]/td[1]/a'):
                xpathUrl = self.browser.find_element(By.XPATH, f'//*[@id="overview"]/tbody/tr[{x+1}]/td[1]/a')

                url = xpathUrl.get_attribute("href")
                id_village = url.split('=')[1]

                self.villages[list_village[x]] = {'url': url, 'id': id_village}

    def get_upgrade_orders(self, village):

        self.browser.get(self.villages[village]['url'])
        self.browser.get(f'{self.server}/dorf1.php')

        # Pega o tempo maximo espera para a atualização
        self.get_seconds_update(village)

        # Zera inforamções do upgrade orders
        old_list = []
        for order in self.upgrade_orders[village]['upgrades']:
            if order['status'] == 'waiting' or  order['status'] == 'no resources':
                old_list.append(order)
        
        self.upgrade_orders[village]['upgrades'] = []
        new_list = []

        for x in range(2, 20):

            under_construction = self.browser.find_element(By.XPATH, f'//*[@id="resourceFieldContainer"]/a[{x}]')
            list_class = under_construction.get_attribute('class').split()

            if 'underConstruction' in list_class:
                slot = (list_class[4].split('buildingSlot')[1])
                name = (BUILDING[list_class[3]])
                level = (list_class[6].split('level')[1])

                new_list.append(
                    {
                        'slot': slot,
                        'name': name,
                        'level': str(int(level)+1),
                        'status': 'updating'
                })

        self.browser.get(f'{self.server}/dorf2.php')

        level = 0
        for x in range(1, 23):

            under_construction = self.browser.find_elements(By.XPATH, f'//*[@id="villageContent"]/div[{x}]/a') 
            if under_construction:
                if 'underConstruction' in under_construction[0].get_attribute('class').split():

                    element = self.browser.find_element(By.XPATH, f'//*[@id="villageContent"]/div[{x}]')

                    list_class = element.get_attribute('class').split()

                    slot = (list_class[1].split('a')[1])
                    name = (BUILDING[f'gid{list_class[2].split("g")[1]}'])

                    new_list.append(
                        {
                            'slot': slot,
                            'name': name,
                            'level': str(int(level)+1),
                            'status': 'updating'
                    })

        self.upgrade_orders[village]['upgrades'] = new_list + old_list

    def get_seconds_update(self, village):
        drive = self.browser.find_elements(By.XPATH, '//*[@id="contentOuterContainer"]/div/div[2]/div[1]/ul')

        if not self.upgrade_orders.get(village):
            self.upgrade_orders[village] = {}
            self.upgrade_orders[village]['upgrades'] = []

        if drive:
            # Ajustando string
            drive = drive[0].text
            drive = drive.split('\n')

            # Obtendo o tempo em segundos
            construction = drive[:2][1].split(':')
            seconds = (int(construction[0])*3600) + (int(construction[1])*60) + int(construction[2][0:2])

            # Obtendo informações da segunda ordem de construção
            if len(drive) == 4:
                # Obtendo nome,level e segundos do upgrade do segundo upgrade
                construction = drive[2:][1].split(':')
                seconds = (int(construction[0])*3600) + (int(construction[1])*60) + int(construction[2][0:2])
                
            self.upgrade_orders[village]['time'] = seconds

    def auto_send_farmlist(self):

        village = self.farmlist['village']
        
        self.browser.get(self.villages[village]['url'])
        self.browser.get(self.server + '/build.php?id=39&gid=16&tt=99')

        buttonStartAllList = self.browser.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div[3]/div/div[1]/div[2]/button[1]')
        if buttonStartAllList:
            buttonStartAllList[0].click()

    def get_farmlist(self):

        for village in self.villages:
            name = self.villages[village]['slot']['39']['name']
            if name == 'Rally Point':
                self.browser.get(self.villages[village]['url'])
                self.browser.get(self.server + '/build.php?id=39&gid=16&tt=99')
                xpth = '/html/body/div[3]/div[3]/div[3]/div[2]/div/div[3]/div/div[1]/div[2]/button[1]'
                if self.browser.find_elements(By.XPATH, xpth):
                    self.farmlist = {'active': True, 'village': village}
                    break

    def check_construction_resources(self):
        """
        Esta função checa se na aldeia tem os recursos necessários para a construção desejada
        """

        lumber = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[1]/span').text
        clay = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/span').text
        iron = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[3]/span').text
        crop = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[1]/div[1]/div[4]/span').text

        lumber = lumber.replace(',', '').replace('.', '').replace(' ', '')
        clay = clay.replace(',', '').replace('.', '').replace(' ', '')
        iron = iron.replace(',', '').replace('.', '').replace(' ', '')
        crop = crop.replace(',', '').replace('.', '').replace(' ', '')

        return {'lumber': lumber, 'clay': clay, 'iron': iron, 'crop': crop}

    def get_only_crop(self, village):
        croplands = []

        for slot in self.villages[village]['slot']:
            name = self.villages[village]['slot'][slot]['name']
            if name == 'Cropland':
                croplands.append(slot)

        return croplands
    
    def get_no_crop(self, village):
        fields = []

        for slot in self.villages[village]['slot']:
            name = self.villages[village]['slot'][slot]['name']
            if name in ('Woodcutter', 'Clay Pit', 'Iron Mine'):
                fields.append(slot)

        return fields

    def upgrade_to_level(self, village, slot, to_level):
        # Entra na vila
        self.browser.get(self.villages[village]['url'])

        current_level = self.villages[village]['slot'][slot]['level']
        name = self.villages[village]['slot'][slot]['name']

        if name == 'Marketplace':
            code = '&t=0'

        elif name == 'Rally Point' or name == 'Residence' or name == 'Palace':
            code = '&tt=0'

        else:
            code = ''
        
        self.browser.get(f'{self.server}/build.php?id={str(slot)}{code}')


        if int(current_level) < int(to_level):
            
            # Verifico se tenho recursos para realizar o upgrade
            # Atualizo a quantidade de recursos que tenho na aldeia
            self.get_resources(village)

            # Pego a quantidade de recursos necessário para atualizar o slot e verifico se posso atualizar
            resources = self.check_construction_resources()

            # Verifica se tem recursos suficientes para realizar o upgrade
            with_resources = self.check_resources_for_update_slot(village, resources)

            # Se tem recursos e se não tiver ordens em andamento, realiza o upgrade de level
            if not with_resources or self.upgrade_orders[village]['upgrades']:
                status = 'waiting'
                if not with_resources:
                    status = 'no resources'

                self.upgrade_orders[village]['upgrades'].append(
                    {
                        'slot': slot, 
                        'name': self.villages[village]['slot'][slot]['name'],
                        'level': to_level,
                        'status': status
                    }
                )

            elif with_resources:
                # Atualiza o slot
                buttonUpgrade = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[3]/div[1]/button')
                buttonUpgrade.click()

                # Adciona a informação no upgrade_orders
                self.upgrade_orders[village]['upgrades'].insert(0,
                    {
                        'slot': slot, 
                        'name': self.villages[village]['slot'][slot]['name'],
                        'level': to_level,
                        'status': 'updating'
                    }
                )

    def check_resources_for_update_slot(self, village, resources):

        # Verifica se tem os rercursos necessário para fazer a construção
        if (int(self.resources[village]['lumber']) >= int(resources['lumber']) and
            int(self.resources[village]['clay']) >= int(resources['clay'])  and
            int(self.resources[village]['iron']) >= int(resources['iron'])  and
            int(self.resources[village]['crop']) >= int(resources['crop'])):
            return True
        else:
            return False

    def get_resources(self, village):
        """
        Escaneia os recursos disponíveis em uma aldeia
        """

        self.browser.implicitly_wait(4)

        lumber = self.browser.find_element(By.ID, 'l1').text
        clay = self.browser.find_element(By.ID, 'l2').text
        iron = self.browser.find_element(By.ID, 'l3').text
        crop = self.browser.find_element(By.ID, 'l4').text

        self.resources[village] = {
            "lumber": lumber.replace(',', '').replace('.', '').replace(' ', ''),
            "clay": clay.replace(',', '').replace('.', '').replace(' ', ''),
            "iron": iron.replace(',', '').replace('.', '').replace(' ', ''),
            "crop": crop.replace(',', '').replace('.', '').replace(' ', '')
        }

    def get_troops_infantary(self, village):

        is_created, slot = self.get_barracks_is_created(village)
        if is_created:
            self.browser.get(self.villages[village]['url'])

            self.browser.get(f'{self.server}/build.php?id={slot}')

            if not self.troops.get(village):
                self.troops[village] = {}
            infantry = []

            if self.tribe == 'Gaul':
                if self.browser.find_elements(By.NAME, "t1"):
                    infantry.append('Phalanx')

                if self.browser.find_elements(By.NAME, "t2"):
                    infantry.append('Swordsman')

            elif self.tribe == 'Teuton':
                if self.browser.find_elements(By.NAME, "t1"):
                    infantry.append('Clubswinger')

                if self.browser.find_elements(By.NAME, "t2"):
                    infantry.append('Spearman')

                if self.browser.find_elements(By.NAME, "t3"):
                    infantry.append('Axeman')

                if self.browser.find_elements(By.NAME, "t4"):
                    infantry.append('Scout')

            elif self.tribe == 'Roman':
                if self.browser.find_elements(By.NAME, "t1"):
                    infantry.append('Legionnaire')

                if self.browser.find_elements(By.NAME, "t2"):
                    infantry.append('Praetorian')

                if self.browser.find_elements(By.NAME, "t3"):
                    infantry.append('Imperian')

            elif self.tribe == 'Egyptian':
                if self.browser.find_elements(By.NAME, "t1"):
                    infantry.append('Slave Militia')

                if self.browser.find_elements(By.NAME, "t2"):
                    infantry.append('Ash Warden')

                if self.browser.find_elements(By.NAME, "t3"):
                    infantry.append('Khopesh Warrior')

            elif self.tribe == 'Hun':
                if self.browser.find_elements(By.NAME, "t1"):
                    infantry.append('Mercenary')

                if self.browser.find_elements(By.NAME, "t2"):
                    infantry.append('Bowman')

            self.troops[village]['infantry'] = infantry

    def get_troops_cavalry(self, village):

        is_created, slot = self.get_stable_is_created(village)
        if is_created:
            self.browser.get(self.villages[village]['url'])

            self.browser.get(f'{self.server}/build.php?id={slot}')

            if not self.troops.get(village):
                self.troops[village] = {}

            cavalry = []
            if self.tribe == 'Gaul':
                if self.browser.find_elements(By.NAME, "t3"):
                    cavalry.append('Pathfinder')

                if self.browser.find_elements(By.NAME, "t4"):
                    cavalry.append('Theutates Thunder')

                if self.browser.find_elements(By.NAME, "t5"):
                    cavalry.append('Druidrider')

                if self.browser.find_elements(By.NAME, "t6"):
                    cavalry.append('Haeduan')

            elif self.tribe == 'Teuton':
                if self.browser.find_elements(By.NAME, "t5"):
                    cavalry.append('Paladin')

                if self.browser.find_elements(By.NAME, "t6"):
                    cavalry.append('Teutonic Knight')

            elif self.tribe == 'Roman':
                if self.browser.find_elements(By.NAME, "t4"):
                    cavalry.append('Equites Legati')

                if self.browser.find_elements(By.NAME, "t5"):
                    cavalry.append('Equites Imperatoris')

                if self.browser.find_elements(By.NAME, "t6"):
                    cavalry.append('Equites Caesaris')
            
            elif self.tribe == 'Egyptian':
                if self.browser.find_elements(By.NAME, "t4"):
                    cavalry.append('Sopdu Explorer')

                if self.browser.find_elements(By.NAME, "t5"):
                    cavalry.append('Anhur Guard')

                if self.browser.find_elements(By.NAME, "t6"):
                    cavalry.append('Resheph Chariot')
            
            elif self.tribe == 'Hun':
                if self.browser.find_elements(By.NAME, "t3"):
                    cavalry.append('Spotter')

                if self.browser.find_elements(By.NAME, "t4"):
                    cavalry.append('Steppe Rider')

                if self.browser.find_elements(By.NAME, "t5"):
                    cavalry.append('Marksman')

                if self.browser.find_elements(By.NAME, "t6"):
                    cavalry.append('Marauder')

            self.troops[village]['cavalry'] = cavalry

    def infantry_training(self, village, infantry, number_of_trainings):

        is_created, slot = self.get_barracks_is_created(village)

        if is_created:
            self.browser.get(self.villages[village]['url'])

            self.browser.get(f'{self.server}/build.php?id={slot}')

            code = TROOPS[self.tribe][infantry]

            input_number_of_troops = self.browser.find_element(By.NAME, code)
            input_number_of_troops.send_keys(number_of_trainings)

            button = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/form/button')
            button.click()

    def cavalry_training(self, village, cavalry, number_of_trainings):

        is_created, slot = self.get_stable_is_created(village)

        if is_created:
            self.browser.get(self.villages[village]['url'])
            
            self.browser.get(f'{self.server}/build.php?id={slot}')

            code = TROOPS[self.tribe][cavalry]

            input_number_of_troops = self.browser.find_element(By.NAME, code)
            input_number_of_troops.send_keys(number_of_trainings)

            button = self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[3]/div[2]/div/div/form/button')
            button.click()

    def get_barracks_is_created(self, village):
        for slot in self.villages[village]['slot']:
            name = self.villages[village]['slot'][slot]['name']

            if name == 'Barracks':
                return True, slot
            
        return False, None

    def get_stable_is_created(self, village):
        for slot in self.villages[village]['slot']:
            name = self.villages[village]['slot'][slot]['name']

            if name == 'Stable':
                return True, slot
            
        return False, None
    
    def is_logged_in(self):
        try:
            self.browser.find_element(By.ID, 'topBarHero')
            self.logged = True

        except:
            self.logged = False

    def quit(self, *args):
        """
        Responsável por fechar o navegador interno
        """
        
        self.browser.get(f'{self.server}/logout')
        self.browser.quit()


if __name__ == "__main__":
    """ 
    from selenium.common.exceptions import NoSuchWindowException
    from requests.exceptions import ConnectionError

    travian = Village()

    try:
        travian.instance_browser()
        travian.browser.get("https://www.google.com")

    except NoSuchWindowException as e:
        travian.instance_browser()
        time.sleep(1)
        travian.browser.get("https://www.google.com")

    except ConnectionError as e:
        print("Parece que esta sem acesso a internet", e)

    except Exception as e:
        print("Erro genérico:", e)"""
    
    travian = Travian()
    travian.login('ts20.x2.international.travian.com','Diviks', 'aaa' )
    