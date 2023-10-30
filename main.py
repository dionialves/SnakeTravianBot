import os
import time
import datetime
import sys
from watchdog.observers import Observer

from models.village import Village
from models.construction import Construction
from models.log import Log
from models.farmlist import Farmlist
from models.database import Database
from models.infantrytraining import InfatryTraining
from models.cavalrytraining import CavalryTraining

def print_log(travian):
    log = Log(travian)
    log.print_on_file()

    observer = Observer()
    observer.schedule(Log(travian), path=".")
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


"""
As funções abaixo serão utilizadas para manipulação dos menus do sistema
"""
def get_information_on_account():
    print("Forneça as informações do servidor: ")
    server = input('Server => ')
    username = input('Username => ')
    password = input('Password => ')

    return server, username, password

def login_on_server(server, username, password):
    travian = Village()
    travian.server = server
    travian.username = username
    travian.password = password
    travian.login(travian.server, travian.username, travian.password)
    time.sleep(2)

    return travian



""" Funções relacionadas ao Menu"""
def menu():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("____________________________________________________________")
        print('')
        print('1 - Aldeias')
        print('2 - Farmlist')
        print('')
        print('')
        print(f'(P) Print of Logs | (Q) Sair')
        option = input('=> ')

        match option.lower():
            case '1':
                return '1'
            case '2':
                return '2'
            case 'p':
                print_log(travian)
            case 'q':
                if input('Deseja realmente sair? S/N: ').lower() == 's':
                    menu_quit_of_system(travian)


def menu_set_village():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("____________________________________________________________")
        print('')
        print("Selecione o indice para entrar um de suas aldeias: ")
        print('')

        name_village = ''
        list_names = []
        aux = 1
        for x in travian.villages:
            print(f'{aux} - {x}')
            list_names.append(x)
            aux = aux + 1
        print('')
        print('')
        print(f'(Q) Sair')
        idVillage = input('=> ')

        if idVillage.lower() == 'p':
            print_log(travian)

        # Entra no menu sair
        if idVillage.lower() == 'q':
            break

        if 0 <= (int(idVillage)-1) < len(list_names):

            name_village = list_names[int(idVillage)-1]

            if database.check_data_of_village(name_village):
                message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {name_village} -> Banco de dados carregado com sucesso'
                log.write(message)

                travian.fields = database.upload_data()
            
            else:
                message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {name_village} -> Aldeia não encontrada no banco de dados'
                log.write(message)
                print(message)

                message = f'{datetime.datetime.now().strftime("%H:%M:%S")} | {name_village} -> Atualizando dados, isso pode levar vários minutos ...'
                log.write(message)
                print(message)

                travian.update_all_fields_village(name_village)
                database.write(travian.fields)

            menu_of_village(name_village)
        else:
            print('Escolha uma das aldeias listada acima!')
            time.sleep(4)

def menu_of_village(name_village):
    
    option = ""
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal')
        print('')
        print("1 - Recursos e Edifícios")
        print("2 - Atualizar Aldeia")
        print("3 - Treino de Infantaria")
        print('4 - Treino de Cavalaria')
        print('')
        print("(Q) Sair")
        option = input("=> ")

        match option.lower():
            case "1": 
                resorurses_and_buildings(travian, name_village)
            case "2":
                menu_update_village(travian, name_village)
            case "3":
                menu_training_infantry(travian, name_village)
            case "4":
                menu_training_cavalry(travian, name_village)
            case "q":
                break

def menu_training_infantry(travian, name_village):
    travian.get_troops_infantary(name_village)

    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Treino de Infantaria')
        print('')

        # Verifica o treino já foi iniciado nessa aldeia
        if name_village in thread_training_infantry:
            print('O treino já esta ativado para essa aldeia, com a seguinte configuração')
            print('')

            aux = 1

            for infantry in thread_training_infantry[name_village].training['infantry']:
                print(f'-> {infantry}: {thread_training_infantry[name_village].training["train_number"][aux-1]}')
                aux += 1

            print(f'O proximo treino será realizado as {thread_training_infantry[name_village].next_training}')
            print('')
            print('')
            print('(D) Desativar | (Q) Sair')
            option = input('=> ')

            match option.lower():
                case 'd':
                    # Para a execução da thread e deleta a aldeia de dicionário thread_training_infantry
                    thread_training_infantry[name_village].event.set()
                    thread_training_infantry[name_village].join()
                    del thread_training_infantry[name_village]
                case 'q':
                    break
        else:
            print('Infantarias habilitadas para treino:')
            print('')

            for infantry_available in travian.troops['infantry']:
                print(f'-> {infantry_available}')

            print('')
            print('')
            print('(T) Treinar | (Q) Sair')
            option = input('=> ')

            match option.lower():
                case 't':
                    while True:
                        os.system('cls')
                        print("____________________________________________________________")
                        print(f'Account: {travian.username}')
                        print(f'Server: {travian.server}')
                        print("")
                        print(F'Aldeia: {name_village}')
                        print("____________________________________________________________")
                        print('Menu -> Menu Principal -> Treino de Infantaria -> Treinar')
                        print('')
                        print('Defina abaixo a quantidade tropas a serem treinadas:')
                        print('')

                        list_of_train_number = []
                        infantry = []
                        aux = 1
                        for infantry_available in travian.troops['infantry']:
                            train_number = input(f'{aux} - {infantry_available}: ')
                            infantry.append(infantry_available)
                            list_of_train_number.append(train_number)
                            aux += 1
                        print('')
                        interval = input('Por qual intervalo de tempo: ')

                        print('')
                        print('')
                        print('Iniciar o treino? S/N : ')
                        option = input('=> ')

                        match option.lower():
                            case 's':
                                thread_training_infantry[name_village] = {}
                                thread_training_infantry[name_village] = InfatryTraining(travian)
                                thread_training_infantry[name_village].daemon = True
                                thread_training_infantry[name_village].start()
                                thread_training_infantry[name_village].add(name_village, infantry, list_of_train_number, int(interval)*60)

                                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Treino inicado!')
                                time.sleep(4)
                                break

                            case 'n':
                                break

                case 'q':
                    break 

def menu_training_cavalry(travian, name_village):
    travian.get_troops_cavalry(name_village)

    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Treino de Cavalaria')
        print('')

        # Verifica o treino já foi iniciado nessa aldeia
        if name_village in thread_training_cavalry:
            print('O treino já esta ativado para essa aldeia, com a seguinte configuração')
            print('')

            aux = 1

            for cavalry in thread_training_cavalry[name_village].training['cavalry']:
                print(f'-> {cavalry}: {thread_training_cavalry[name_village].training["train_number"][aux-1]}')
                aux += 1

            # Verificação, pois o sistema pode ser mais rapido que a definição dessa variavel
            # Retornando erro na apresentação dessa informação
            if thread_training_cavalry[name_village].next_training:
                print(f'O proximo treino será realizado as {thread_training_cavalry[name_village].next_training}')
            print('')
            print('')
            print('(D) Desativar | (Q) Sair')
            option = input('=> ')

            match option.lower():
                case 'd':
                    # Para a execução da thread e deleta a aldeia de dicionário thread_training_cavalry
                    thread_training_cavalry[name_village].event.set()
                    thread_training_cavalry[name_village].join()
                    del thread_training_cavalry[name_village]
                case 'q':
                    break
        else:
            print('Cavalarias habilitadas para treino:')
            print('')

            for cavalry_available in travian.troops['cavalry']:
                print(f'-> {cavalry_available}')

            print('')
            print('')
            print('(T) Treinar | (Q) Sair')
            option = input('=> ')

            match option.lower():
                case 't':
                    while True:
                        os.system('cls')
                        print("____________________________________________________________")
                        print(f'Account: {travian.username}')
                        print(f'Server: {travian.server}')
                        print("")
                        print(F'Aldeia: {name_village}')
                        print("____________________________________________________________")
                        print('Menu -> Menu Principal -> Treino de Cavalaria -> Treinar')
                        print('')
                        print('Defina abaixo a quantidade tropas a serem treinadas:')
                        print('')

                        list_of_train_number = []
                        cavalry = []
                        aux = 1
                        for cavalry_available in travian.troops['cavalry']:
                            train_number = input(f'{aux} - {cavalry_available}: ')
                            cavalry.append(cavalry_available)
                            list_of_train_number.append(train_number)
                            aux += 1
                        print('')
                        interval = input('Por qual intervalo de tempo: ')

                        print('')
                        print('')
                        print('Iniciar o treino? S/N : ')
                        option = input('=> ')

                        match option.lower():
                            case 's':
                                thread_training_cavalry[name_village] = {}
                                thread_training_cavalry[name_village] = CavalryTraining(travian)
                                thread_training_cavalry[name_village].daemon = True
                                thread_training_cavalry[name_village].start()
                                thread_training_cavalry[name_village].add(name_village, cavalry, list_of_train_number, int(interval)*60)

                                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Treino inicado!')
                                time.sleep(4)
                                break

                            case 'n':
                                break
                case 'q':
                    break 

def resorurses_and_buildings(travian, name_village):
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Recursos e Edificações')
        print('')
        print('1 - Listar Campos de Recursos')
        print('2 - Listar Edifícios')
        print('3 - Update Campos de Recursos')
        print('4 - Update Edifícios')
        print('5 - Fila de Construções')
        print('')
        print('')
        print('(Q) Sair')
        option = input('=> ')

        match option.lower():
            case '1':
                os.system('cls')
                print("____________________________________________________________")
                print(f'Account: {travian.username}')
                print(f'Server: {travian.server}')
                print("")
                print(F'Aldeia: {name_village}')
                print("____________________________________________________________")
                print('Menu -> Menu Principal -> Recursos e Edificações -> Listar Campos de Recursos')
                print('')
                for slot in range(0, 18):
                    print(f'({travian.fields[name_village]["level"][int(slot)]}) {travian.fields[name_village]["name"][int(slot)]}')
                
                print('')
                input('Precione qualquer tecla para sair')

            case '2':
                os.system('cls')
                print("____________________________________________________________")
                print(f'Account: {travian.username}')
                print(f'Server: {travian.server}')
                print("")
                print(F'Aldeia: {name_village}')
                print("____________________________________________________________")
                print('Menu -> Menu Principal -> Recursos e Edificações -> Listar Edificios')
                print('')
                for slot in range(18, 40):
                    print(f'id: {int(slot + 1)} - ({travian.fields[name_village]["level"][int(slot)]}) {travian.fields[name_village]["name"][int(slot)]}')
                
                print('')
                input('Precione qualquer tecla para sair')

            case '3':
                while True:
                    os.system('cls')
                    print("____________________________________________________________")
                    print(f'Account: {travian.username}')
                    print(f'Server: {travian.server}')
                    print("")
                    print(F'Aldeia: {name_village}')
                    print("____________________________________________________________")
                    print('Menu -> Menu Principal -> Recursos e Edificações -> Update Campos de Recursos')
                    print('')
                    print("1 - Apenas Cereal")
                    print("2 - Apenas Madeira, Barro e Ferro")
                    print("3 - Todos os recuros")
                    print(f'')
                    option = input("=> ")

                    print(f'')
                    print("Escolha qual level deseja evoluir os recursos: ")
                    toLevel = input('=> ')

                    match option:
                        case "1":
                            list_of_ids = travian.get_only_crop(name_village)
                        case "2":
                            list_of_ids = travian.get_no_crop(name_village)
                        case "3":
                            list_of_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                        case _:
                            pass
                        
                    if option and toLevel:
                        
                        thread_construction[name_village].construction_for_resourses(name_village, toLevel, list_of_ids)
                        
                        print('')
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                        time.sleep(4)
                    os.system('cls')
                    break
            case '4':
                while True:
                    os.system('cls')
                    print("____________________________________________________________")
                    print(f'Account: {travian.username}')
                    print(f'Server: {travian.server}')
                    print("")
                    print(F'Aldeia: {name_village}')
                    print("____________________________________________________________")
                    print('Menu -> Menu Principal -> Recursos e Edificações -> Update Edifícios')
                    print('')
                    for slot in range(18,40):
                        
                        if travian.fields[name_village]['level'][slot] != "0":
                            print(f'id: {slot+1} | ({travian.fields[name_village]["level"][slot]}) - {travian.fields[name_village]["name"][slot]}')
                    
                    slot_id = input('Id => ')
                    to_level = input('Upgrade para qual nível => ')

                    if slot_id and to_level:

                        thread_construction[name_village].add(name_village, slot_id, to_level)

                        print('')
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                        time.sleep(4)
                    os.system('cls')
                    break
            case '5':
                menu_activities_list(name_village)
            case 'q':
                break
            case _:
                os.system('cls')

def menu_update_village(travian, name_village):
    os.system('cls')
    print("____________________________________________________________")
    print(f'Account: {travian.username}')
    print(f'Server: {travian.server}')
    print("")
    print(F'Aldeia: {name_village}')
    print("____________________________________________________________")
    print('Menu -> Menu Principal -> Atualizar Aldeia')
    print('')
    print('')

    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos')
    travian.update_all_fields_village(name_village)
    database.write(travian.fields)

def menu_start_farmlist():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print("____________________________________________________________")
        print('Menu -> Auto Send Farmlist')
        print('')
        print('')
        start_of_interval = 20
        end_of_interval = 40

        if thread_farmlist.order_auto_send_farmlist:
            print(f'--> Farmlist esta ativado com intervalo automatico entre {start_of_interval} e {end_of_interval} minutos')
            print('')
            print('')
            print('')
            print('(D) Desativar Farmlist | (Q) Sair')
            option = input('=> ')

        else:
            print('--> Farmlist não esta ativado')
            print('')
            print('')
            print('')
            print('(A) Ativar Farmlist | (Q) Sair')
            option = input('=> ')

        match option.lower():
            case 'd':
                    thread_farmlist.order_auto_send_farmlist = {}

                    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Farmlist desativado')
                    time.sleep(4)

            case 'a':
                if not thread_farmlist.order_auto_send_farmlist:
                    thread_farmlist.add(start_of_interval, end_of_interval)

                    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Farmlist Ativado')
                    time.sleep(4)
            case 'q':
                break

def menu_activities_list(name_village):
    
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {travian.username}')
        print(f'Server: {travian.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Lista de Atividades')
        print('')

        print("1 - Listar Atividades")
        print("2 - Excluir uma atividade")
        print('')
        print('')
        print("(Q) Sair")
        option = input('=> ')

        match option.lower():
            case "1":
                os.system('cls')
                print("____________________________________________________________")
                print(f'Account: {travian.username}')
                print(f'Server: {travian.server}')
                print("")
                print(F'Aldeia: {name_village}')
                print("____________________________________________________________")
                print('Menu -> Menu Principal -> Lista de Atividades - Listar')
                print('')

                for order in thread_construction[name_village].list_of_construction:
                    print(f' => {order["village"]} construindo {travian.fields[name_village]["name"][int(order["slot_id"])-1]} para o level {order["to_level"]} ')
                            
                print('')
                input('Precione qualquer tecla para sair')
            case "2":
                pass
            case "q":
                break

def menu_quit_of_system(travian):
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')
    travian.quit()
    sys.exit()

if __name__ == "__main__":
    os.system('cls')
    server, username, password = get_information_on_account()
    print("____________________________________________________________")
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Logando na sua conta, aguarde...')
    travian = login_on_server(server, username, password)

    # get name village and tribe
    travian.update_name_villages()
    travian.get_tribe()

    # Iniciando class Log
    log = Log(travian)

    # Inicializa database
    database = Database(travian)

    # INicializando Variavel de farmlist
    thread_farmlist = Farmlist(travian)
    thread_farmlist.daemon = True
    thread_farmlist.start()

    # Inicia as threads de construção
    thread_construction = {}
    for name_village in travian.villages:
        thread_construction[name_village] = Construction(travian)
        thread_construction[name_village].daemon = True
        thread_construction[name_village].start()

    # Inicia as threads de treino
    thread_training_infantry = {}
    thread_training_cavalry = {}

    log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logado na conta com sucesso')

    os.system('cls')

    while True:
        id_menu = menu()
        match id_menu:
            case '1':
                menu_set_village()
            case '2':
                menu_start_farmlist()
