import os
import time
import datetime
import sys
from watchdog.observers import Observer

from models.travian import Travian
from models.construction import Construction
from models.log import Log
from models.farmlist import Farmlist
from models.database import Database
from models.infantrytraining import InfatryTraining
from models.cavalrytraining import CavalryTraining
from models.browser import Browser


class App:
    def __init__(self):
        self.travian = Travian()
        self.current_village = ''

        self.thread_farmlist = {}

        # Inicia thread Construcrion
        self.thread_construction = {}

        # Inicia a thread Browser, classe responsável por ser uma interface entre outros classe e a classe village
        self.browser = Browser(self.travian)
        self.browser.daemon = True
        self.browser.start()

        # Inicia as threads de treino
        self.thread_training_infantry = {}
        self.thread_training_cavalry = {}
        self.travian.troops['infantry'] = {}
        self.travian.troops['cavalry'] = {}

    def gui_get_information_on_account(self):
        os.system('cls')
        print("____________________________________________________________________________________________")
        print("| Forneça as informações do servidor: ")
        server = input('| Server => ')
        username = input('| Username => ')
        password = input('| Password => ')

        return server, username, password

    def login(self):
        print("|___________________________________________________________________________________________")
        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} | Logando na sua conta, aguarde...')

        server, username, password = self.gui_get_information_on_account()

        #self.travian.login(self.travian.server, self.travian.username, self.travian.password)
        self.browser.add(task='login', args={'server': server, 'username': username, 'password': password})
        self.browser.await_task('login')

    def instance(self):
        # busca informações iniciais
        self.browser.add('update')
        self.browser.await_task('update')

        # Inicia Log
        self.log = Log(self.travian)
        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Logado na conta com sucesso')

        # Inicia database
        self.database = Database(self.travian)
        self.database.write(self.travian.villages)

    def run(self):
        self.login()
        self.instance()

        while True:
            option = self.main_menu()

            match option.lower():
                case '1':
                    self.menu_set_village()
                case '2':
                    self.menu_auto_send_farmlist()
                case 'p':
                    self.print_log()
                case 'q':
                    if input('| Deseja realmente sair? S/N: ').lower() == 's':
                        self.menu_quit_of_system()

    def main_menu(self):
        while True:
            self.header()
            print('| Menu Principal')
            print('|')
            print('| 1 - Aldeias')
            print('| 2 - Auto Send Farmlist')
            print('|')
            print("|___________________________________________________________________________________________")
            print(f'| (P) Print of Logs | (Q)uit')
            return  input('| => ')

    def menu_set_village(self):
        while True:
            self.header()
            print('| Main Menu -> Village')
            print('|')
            print("| Selecione o indice para entrar um de suas aldeias: ")
            print('|')

            list_names = []
            aux = 1
            for x in self.travian.villages:
                print(f'| {aux} - {x}')
                list_names.append(x)
                aux = aux + 1
            print('|')
            print('|')
            print("|___________________________________________________________________________________________")
            print(f'| (Q)uit')
            id_village = input('| => ')

            # Entra no menu sair
            if id_village.lower() == 'q':
                break

            if id_village.isdigit():
                if 0 <= (int(id_village)-1) < len(list_names):

                    self.current_village = list_names[int(id_village)-1]

                    if self.database.check_data_of_village(self.current_village):
                        message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {self.current_village} -> Banco de dados carregado com sucesso'
                        self.log.write(message)

                        self.travian.villages = self.database.upload_data()
                    
                    else:
                        message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {self.current_village} -> Aldeia não encontrada no banco de dados'
                        self.log.write(message)
                        print(message)

                        message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {self.current_village} -> Atualizando dados, isso pode levar vários minutos ...' 
                        self.log.write(message)
                        print(message)

                        self.browser.add(task='update')
                        self.browser.await_task('update')
                        self.database.write(self.travian.villages)

                    self.menu_of_village()
                else:
                    print('| Escolha uma das aldeias listada acima!')
                    time.sleep(2)

    def menu_auto_send_farmlist(self):
        while True:
            self.header()
            print(f'| Main Menu -> Auto Sendo Farmlist')
            print('|')
            print('|')
            start_of_interval = 20
            end_of_interval = 40

            if self.travian.farmlist['active']:
                if self.thread_farmlist:
                    print(f'| --> Farmlist esta ativado com intervalo automatico entre {start_of_interval} e {end_of_interval} minutos')
                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (D)isable | (Q)uit')
                    option = input('| => ')

                else:
                    print('| --> Farmlist não esta ativado')
                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (A)ctivate | (Q)uit')
                    option = input('| => ')

                match option.lower():
                    case 'd':
                        if self.thread_farmlist:
                            self.thread_farmlist.event.set()
                            self.thread_farmlist.join()
                            self.thread_farmlist = None

                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Farmlist desativado')
                            print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} | Farmlist desativado')
                            time.sleep(2)

                    case 'a':
                        if not self.thread_farmlist:
                            self.thread_farmlist = Farmlist(self.travian, self.browser)
                            self.thread_farmlist.daemon = True
                            self.thread_farmlist.start()
                        
                            self.thread_farmlist.add(start_of_interval, end_of_interval)

                            print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} | Farmlist Ativado')
                            time.sleep(2)
                    case 'q':
                        break

            else:
                print('| --> Aldeia não tem lista de famrs criada')
                print('|')
                print('|')
                print("|___________________________________________________________________________________________")
                print('| (U)pdate Information | (Q)uit')
                option = input('| => ')

                match option.lower():
                    case 'u':
                        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} | Atualizando informações')
                        # Envia task para a fila de processamento, e obriga do sistema a aguardar o termino dessa atividade
                        self.browser.add(task='get_farmlist')
                        self.browser.await_task('get_farmlist')
                    case 'q':
                        break

    def menu_of_village(self):
        option = ""
        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village}')
            print('|')
            print("| 1 - Recursos e Edifícios")
            print("| 2 - Atualizar Aldeia")
            print("| 3 - Treino de Infantaria")
            print('| 4 - Treino de Cavalaria')
            print("|___________________________________________________________________________________________")
            print("| (Q) Sair")
            option = input("| => ")

            match option.lower():
                case "1": 
                    self.page_resorurses_and_buildings()
                case "2":
                    self.page_update_village()
                case "3":
                    self.page_infantry()
                case "4":
                    self.page_cavalry()
                case "q":
                    break

    def page_resorurses_and_buildings(self):
        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Resources and Buildings')
            print('|')
            print('| Id | Level | Descrição')

            list = []

            for slot in self.travian.villages[self.current_village]['slot']:
                name = self.travian.villages[self.current_village]['slot'][slot]['name']
                level = self.travian.villages[self.current_village]['slot'][slot]['level']


                if name != 'Empty':
                    print(f'| Id:{slot} - ({level}) {name} ')

                    list.append(slot)

            print('|')
            print('|')
            print("|___________________________________________________________________________________________")
            print('| (U)pgrade | (I)n Progress | (A)ll Resources | (Q)uit')
            option = input('| => ')

            match option.lower():
                case 'u':

                    slot_id = input('| Escolha o ID a ser evoluido: ')
                    to_level = input('| Para qual level: ')

                    if slot_id.isdigit() and to_level.isdigit() and slot_id in list:

                        if not self.thread_construction.get(self.current_village):
                            self.thread_construction[self.current_village] = Construction(self.travian, self.browser)
                            self.thread_construction[self.current_village].daemon = True
                            self.thread_construction[self.current_village].start()

                        self.thread_construction[self.current_village].add(self.current_village, slot_id, to_level)

                        print('|')
                        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                        time.sleep(2)
                        os.system('cls')

                    else:
                        print('|')
                        print('| Id incorreto, selecione um Id da lista!')
                        time.sleep(2)

                case 'i':
                    self.page_upgrade_in_progress()
                                
                case 'a':
                    to_level = input('| Para qual level: ')

                    if to_level.isdigit():
                        if not self.thread_construction.get(self.current_village):
                            self.thread_construction[self.current_village] = Construction(self.travian, self.browser)
                            self.thread_construction[self.current_village].daemon = True
                            self.thread_construction[self.current_village].start()
                    
                        for level in range(1, int(to_level)+1):
                            for slot in range(1,19):
                                current_level = self.travian.villages[self.current_village]['slot'][str(slot)]['level']

                                if int(current_level) < int(level):
                                    self.thread_construction[self.current_village].add(self.current_village, str(slot), str(level))

                        print('|')
                        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                        time.sleep(2)
                        os.system('cls')
            
                    else:
                        print('|')
                        print('| Id incorreto, selecione um Id da lista!')
                        time.sleep(2) 
                case 'q':
                    break

    def page_upgrade_in_progress(self):
        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Resources and Buildings - List')
            print('|')

            if self.travian.upgrade_orders.get(self.current_village):
                print(f'| ')
                print(f'| ## Sendo construído no momento:')
                print(f'| ')
                resultados = [d for d in self.travian.upgrade_orders[self.current_village]['upgrades'] if d['status'] == 'updating']

                for order in resultados:
                    print(f'| -> {order["name"]} para o level {order["level"]}')

            print(f'| ')
            if self.thread_construction.get(self.current_village):
                if self.thread_construction[self.current_village].list_of_construction:
                    aux = 1
                    print(f'| ')
                    print(f'| ## Na fila para construção:')
                    print(f'| ')
                    for order in self.thread_construction[self.current_village].list_of_construction:
                        name = self.travian.villages[self.current_village]['slot'][order["slot_id"]]['name']

                        print(f'| {aux} - {name} para o level {order["to_level"]} ')
                        aux += 1

                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (D)elete | (U)pdate | (Q)uit')
                    option = input('| => ')

                    match option.lower():
                        case 'd':
                            is_true = input('| Tem certeza que deseja excluir todos os itens da lista? S/N: ')
                            if is_true.lower() == 's':
                                self.thread_construction[self.current_village].event.set()
                                self.thread_construction[self.current_village].join()
                                self.thread_construction[self.current_village] = {}
                                
                                self.thread_construction[self.current_village] = Construction(self.travian, self.browser)
                                self.thread_construction[self.current_village].daemon = True
                                self.thread_construction[self.current_village].start()

                                print('| Itens excluidos como solicitado.')
                                time.sleep(2)
                        case 'u':
                            self.browser.add(task='get_upgrade_orders', args={'village': self.current_village})
                            self.browser.await_task('get_upgrade_orders')
                        case 'q':
                            break
                                
                else:
                    print('| ')
                    print('| ## Nenhuma construção na fila')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (U)pdate | (Q) Sair')
                    option = input('| => ')

                    match option.lower():
                        case 'u':
                            self.browser.add(task='get_upgrade_orders', args={'village': self.current_village})
                            self.browser.await_task('get_upgrade_orders')
                        case 'q':
                            break
            else:
                print('|')
                print('| ## Nenhuma construção na fila')
                print('|')
                print("|___________________________________________________________________________________________")
                print('| (U)pdate | (Q) Sair')
                option = input('| => ')

                match option.lower():
                    case 'u':
                        self.browser.add(task='get_upgrade_orders', args={'village': self.current_village})
                        self.browser.await_task('get_upgrade_orders')
                    case 'q':
                        break

    def page_update_village(self):
        self.header()
        print(f'| Main Menu -> {self.current_village} -> Update')
        print('|')
        print('|')

        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos')

        self.browser.add(task='update')
        self.browser.await_task('update')
        self.database.write(self.travian.villages)

    def page_infantry(self):

        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Infantry')
            print('|')

            # Verifica o treino já foi iniciado nessa aldeia
            if self.current_village in self.thread_training_infantry:
                print('| O treino já esta ativado para essa aldeia, com a seguinte configuração')
                print('|')

                aux = 1

                for infantry in self.thread_training_infantry[self.current_village].training['infantry']:
                    print(f'| -> {infantry}: {self.thread_training_infantry[self.current_village].training["number_of_trainings"][aux-1]}')
                    aux += 1
                
                if self.thread_training_infantry[self.current_village].next_training:
                    print(f'| O proximo treino será realizado as {self.thread_training_infantry[self.current_village].next_training}')
                print('| ')
                print('| ')
                print("|___________________________________________________________________________________________")
                print('| (D)isable | (Q)uit')
                option = input('| => ')

                match option.lower():
                    case 'd':
                        # Para a execução da thread e deleta a aldeia de dicionário thread_training_infantry
                        self.thread_training_infantry[self.current_village].event.set()
                        self.thread_training_infantry[self.current_village].join()
                        del self.thread_training_infantry[self.current_village]
                    case 'q':
                        break
            else:
                if self.current_village in self.travian.troops and 'infantry' in self.travian.troops[self.current_village]:
                    print('| Infantarias habilitadas para treino:')
                    print('| ')

                    for infantry_available in self.travian.troops[self.current_village]['infantry']:
                        print(f'| -> {infantry_available}')

                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (T)o train | (U)pdate | (Q)uit')
                    option = input('| => ')

                    match option.lower():
                        case 't':
                            self.page_train_infantry()

                        case 'u':
                            self.browser.add(task='get_troops_infantary', args={'village': self.current_village})
                            self.browser.await_task('get_troops_infantary')
                
                        case 'q':
                            break 
                else:
                    print('|')
                    print('| Nenhuma infantaria liberada para treino')
                    print('| Certifique-se que o quartel esta criado')
                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (U)pdate | (Q)uit')
                    option = input('| => ')
                
                    match option.lower():
                        case 'u':
                            self.browser.add(task='get_troops_infantary', args={'village': self.current_village})
                            self.browser.await_task('get_troops_infantary')
                    
                        case 'q':
                            break

    def page_train_infantry(self):
        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Infantry -> To Train')
            print('|')
            print('| Defina abaixo a quantidade tropas a serem treinadas:')
            print('|')

            list_of_train_number = []
            infantry = []
            aux = 1
            for infantry_available in self.travian.troops[self.current_village]['infantry']:
                train_number = input(f'| {aux} - {infantry_available}: ')
                infantry.append(infantry_available)
                list_of_train_number.append(train_number)
                aux += 1
            print('|')
            interval = input('| Por qual intervalo de tempo: ')

            print('|')
            print('|')
            print('| Iniciar o treino? S/N : ')
            option = input('| => ')

            match option.lower():
                case 's':
                    check_only_number = all(element.isdigit() for element in list_of_train_number)
                    if check_only_number and interval.isdigit():
                        self.thread_training_infantry[self.current_village] = {}
                        self.thread_training_infantry[self.current_village] = InfatryTraining(self.travian, self.browser)
                        self.thread_training_infantry[self.current_village].daemon = True
                        self.thread_training_infantry[self.current_village].start()
                        self.thread_training_infantry[self.current_village].add(self.current_village, infantry, list_of_train_number, int(interval)*60)

                        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Treino inicado!')
                        time.sleep(2)
                        break
                    else:
                        print('|')
                        print("| Informe apenas numeros!")
                        time.sleep(2)

                case 'n':
                    break

    def page_cavalry(self):

        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Cavalry')
            print('|')

            # Verifica o treino já foi iniciado nessa aldeia
            if self.current_village in self.thread_training_cavalry:
                print('| O treino já esta ativado para essa aldeia, com a seguinte configuração')
                print('|')

                aux = 1

                for cavalry in self.thread_training_cavalry[self.current_village].training['cavalry']:
                    print(f'| -> {cavalry}: {self.thread_training_cavalry[self.current_village].training["number_of_trainings"][aux-1]}')
                    aux += 1

                # Verificação, pois o sistema pode ser mais rapido que a definição dessa variavel
                # Retornando erro na apresentação dessa informação
                if self.thread_training_cavalry[self.current_village].next_training:
                    print(f'| O proximo treino será realizado as {self.thread_training_cavalry[self.current_village].next_training}')
                print('|')
                print('|')
                print("|___________________________________________________________________________________________")
                print('| (D)isable | (Q)uit')
                option = input('| => ')

                match option.lower():
                    case 'd':
                        # Para a execução da thread e deleta a aldeia de dicionário thread_training_cavalry
                        self.thread_training_cavalry[self.current_village].event.set()
                        self.thread_training_cavalry[self.current_village].join()
                        del self.thread_training_cavalry[self.current_village]
                    case 'q':
                        break
            else:
                if self.current_village in self.travian.troops and 'cavalry' in self.travian.troops[self.current_village]:
                    print('| Cavalarias habilitadas para treino:')
                    print('|')

                    for cavalry_available in self.travian.troops[self.current_village]['cavalry']:
                        print(f'| -> {cavalry_available}')

                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (T)o Train | (U)pdate | (Q)uit')
                    option = input('| => ')

                    match option.lower():
                        case 't':
                            self.page_train_cavalry()
                        case 'u':
                            self.browser.add(task='get_troops_cavalry', args={'village': self.current_village})
                            self.browser.await_task('get_troops_cavalry')
                        case 'q':
                            break 
                else:
                    print('|')
                    print('| Nenhuma cavalaria liberada para treino')
                    print('| Certifique-se que o estabulo esta criado')
                    print('|')
                    print('|')
                    print("|___________________________________________________________________________________________")
                    print('| (U)pdate | (Q) Sair')
                    option = input('| => ')
                
                    match option.lower():
                        case 'u':
                            self.browser.add(task='get_troops_cavalry', args={'village': self.current_village})
                            self.browser.await_task('get_troops_cavalry')
                        case 'q':
                            break

    def page_train_cavalry(self):
        while True:
            self.header()
            print(f'| Main Menu -> {self.current_village} -> Cavalry -> To Train')
            print('|')
            print('|')
            print('| Defina abaixo a quantidade tropas a serem treinadas:')
            print('|')

            list_of_train_number = []
            cavalry = []
            aux = 1
            for cavalry_available in self.travian.troops[self.current_village]['cavalry']:
                train_number = input(f'| {aux} - {cavalry_available}: ')
                cavalry.append(cavalry_available)
                list_of_train_number.append(train_number)
                aux += 1
            print('|')
            interval = input('| Por qual intervalo de tempo: ')

            print('|')
            print('|')
            print('| Iniciar o treino? S/N : ')
            option = input('| => ')

            match option.lower():
                case 's':
                    check_only_number = all(element.isdigit() for element in list_of_train_number)
                    if check_only_number and interval.isdigit():
            
                        self.thread_training_cavalry[self.current_village] = {}
                        self.thread_training_cavalry[self.current_village] = CavalryTraining(self.travian, self.browser)
                        self.thread_training_cavalry[self.current_village].daemon = True
                        self.thread_training_cavalry[self.current_village].start()
                        self.thread_training_cavalry[self.current_village].add(self.current_village, cavalry, list_of_train_number, int(interval)*60)

                        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Treino inicado!')
                        time.sleep(2)
                        break
                    else:
                        print('|')
                        print("| Informe apenas numeros!")
                        time.sleep(2)

                case 'n':
                    break

    def print_log(self):
        log = Log(self.travian)
        log.print_on_file()
        
        observer = Observer()
        observer.schedule(Log(self.travian), path='.', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)

                print('')
                if input('Precione "q" para sair: ').strip().lower() == "q":
                    observer.stop()
                    observer.join()
                    break
        except KeyboardInterrupt:
            observer.stop()

    def header(self):
            os.system('cls')
            print("____________________________________________________________________________________________")
            print(f'| Account: {self.travian.username} ({self.travian.tribe})')
            print(f'| Server: {self.travian.server}')
        
            if self.current_village:
                print(F'| Aldeia: {self.current_village}')

            print("|___________________________________________________________________________________________")

    def menu_quit_of_system(self):
        print(f'| {datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')
        self.travian.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()