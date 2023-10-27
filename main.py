import os
import ast
import time
import datetime
import sys
from random import randint
from watchdog.observers import Observer

from models.village import Village
from models.construction import Construction
from models.log import Log
from models.autosendfarmlist import AutoSendFarmlist

 
"""
Esta função será utilizada para iniciar assaltos e usará como base a lista de farms de cada vila
"""
def start_farm_list(village, name_village, minuteStart, minuteEnd):
    while True:
        village.start_all_farm_list(name_village)

        timeStart = randint(int(minuteStart), int(minuteEnd))
        hours = datetime.datetime.now().strftime("%H:%M:%S")
        nextStart = datetime.datetime.now() + datetime.timedelta(minutes=timeStart)
        nextStart = nextStart.strftime("%H:%M:%S")

        log.write(f'{hours} - Realizado o assalto, o proximo esta programado para as {nextStart}')
        time.sleep(timeStart*60)

def get_database(village, name_village):

    log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Verificando database')

    if os.path.isfile(f'{village.username}.database'):
        log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Carregado database com sucesso')

        with open(f'{village.username}.database', 'r') as file:
            fields = file.read()
        fields = ast.literal_eval(fields)
        village.fields = fields

        if not name_village in village.fields:
            create_database(village, name_village)
    else:
        create_database(village, name_village)

def create_database(village, name_village):
    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Identificado que é o primeiro acesso nessa aldeia'
    log.write(message)
    print(message)

    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos'
    log.write(message)
    print(message)

    village.update_all_fields_village(name_village)
    set_database(village)

def set_database(village):
    with open(f'{village.username}.database', 'w') as file:
        file.write(str(village.fields))

def print_log(village):
    log = Log(village)
    log.print_on_file()

    observer = Observer()
    observer.schedule(Log(village), path=".")
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
    village = Village()
    village.server = server
    village.username = username
    village.password = password
    village.login(village.server, village.username, village.password)
    time.sleep(2)
    village.update_name_villages()

    return village


















""" Funções relacionadas ao Menu"""
def menu():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {village.username}')
        print(f'Server: {village.server}')
        print("____________________________________________________________")
        print('')
        print('1 - Aldeias')
        print('2 - Farmlist')
        print('')
        print('')
        print('')
        print(f'(P) Print of Logs | (Q) Sair')
        print(f'')
        option = input('=> ')

        match option.lower():
            case '1':
                return '1'
            case '2':
                return '2'
            case 'p':
                print_log(village)
            case 'q':
                menu_quit_of_system(village)

def menu_set_village():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {village.username}')
        print(f'Server: {village.server}')
        print("____________________________________________________________")
        print('')
        print("Selecione o indice para entrar um de suas aldeias: ")
        print('')

        name_village = ''
        list_names = []
        aux = 1
        for x in village.villages:
            print(f'{aux} - {x}')
            list_names.append(x)
            aux = aux + 1
        print('')
        print('')
        print('')
        print(f'(P) Print of Logs | (Q) Sair')
        print(f'')
        idVillage = input('=> ')

        if idVillage.lower() == 'p':
            print_log(village)

        # Entra no menu sair
        if idVillage.lower() == 'q':
            break

        try:
            name_village = list_names[int(idVillage)-1]
            get_database(village, name_village)
            break
        except:
            print('Escolha uma das aldeias listada acima!')

    menu_of_village(name_village)

def menu_of_village(name_village):
    
    option = ""
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {village.username}')
        print(f'Server: {village.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal')
        print('')
        print("1 - Recursos e Edifícios")
        print("2 - Atualizar Aldeia")
        print("3 - Fila de construções")
        print('')
        print('')
        print('')
        print("(Q) Sair")
        print(f'')
        option = input("=> ")

        match option.lower():
            case "1": 
                resorurses_and_buildings(village, name_village)
            case "2":
                menu_update_village(village, name_village)
            case "3":
                menu_activities_list(name_village)
            case "q":
                break


def resorurses_and_buildings(village, name_village):
        while True:
            os.system('cls')
            print("____________________________________________________________")
            print(f'Account: {village.username}')
            print(f'Server: {village.server}')
            print("")
            print(F'Aldeia: {name_village}')
            print("____________________________________________________________")
            print('Menu -> Menu Principal -> Recursos e Edificações')
            print('')
            print('1 - Listar Campos de Recursos')
            print('2 - Listar Edifícios')
            print('3 - Update Campos de Recursos')
            print('4 - Update Edifícios')
            print('')
            print('')
            print('')
            print('(Q) Sair')
            print(f'')
            option = input('=> ')

            match option.lower():
                case '1':
                    os.system('cls')
                    print("____________________________________________________________")
                    print(f'Account: {village.username}')
                    print(f'Server: {village.server}')
                    print("")
                    print(F'Aldeia: {name_village}')
                    print("____________________________________________________________")
                    print('Menu -> Menu Principal -> Recursos e Edificações -> Listar Campos de Recursos')
                    print('')
                    for slot in range(0, 18):
                        print(f'({village.fields[name_village]["level"][int(slot)]}) {village.fields[name_village]["name"][int(slot)]}')
                    
                    print('')
                    input('Precione qualquer tecla para sair')

                case '2':
                    os.system('cls')
                    print("____________________________________________________________")
                    print(f'Account: {village.username}')
                    print(f'Server: {village.server}')
                    print("")
                    print(F'Aldeia: {name_village}')
                    print("____________________________________________________________")
                    print('Menu -> Menu Principal -> Recursos e Edificações -> Listar Edificios')
                    print('')
                    for slot in range(18, 40):
                        print(f'id: {int(slot + 1)} - ({village.fields[name_village]["level"][int(slot)]}) {village.fields[name_village]["name"][int(slot)]}')
                    
                    print('')
                    input('Precione qualquer tecla para sair')

                case '3':
                    while True:
                        os.system('cls')
                        print("____________________________________________________________")
                        print(f'Account: {village.username}')
                        print(f'Server: {village.server}')
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
                                list_of_ids = village.get_only_crop(name_village)
                            case "2":
                                list_of_ids = village.get_no_crop(name_village)
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
                        print(f'Account: {village.username}')
                        print(f'Server: {village.server}')
                        print("")
                        print(F'Aldeia: {name_village}')
                        print("____________________________________________________________")
                        print('Menu -> Menu Principal -> Recursos e Edificações -> Update Edifícios')
                        print('')
                        for slot in range(18,40):
                            
                            if village.fields[name_village]['level'][slot] != "0":
                                print(f'id: {slot+1} | ({village.fields[name_village]["level"][slot]}) - {village.fields[name_village]["name"][slot]}')
                        
                        slot_id = input('Id => ')
                        to_level = input('Upgrade para qual nível => ')

                        if slot_id and to_level:

                            thread_construction[name_village].add(name_village, slot_id, to_level)

                            print('')
                            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                            time.sleep(4)
                        os.system('cls')
                        break
                        
                case 'q':
                    break
                case _:
                    os.system('cls')

def menu_update_village(village, name_village):
    os.system('cls')
    print("____________________________________________________________")
    print(f'Account: {village.username}')
    print(f'Server: {village.server}')
    print("")
    print(F'Aldeia: {name_village}')
    print("____________________________________________________________")
    print('Menu -> Menu Principal -> Atualizar Aldeia')
    print('')
    print('')

    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos')
    village.update_all_fields_village(name_village)
    set_database(village)

def menu_start_farmlist():
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {village.username}')
        print(f'Server: {village.server}')
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
            print(f'')
            option = input('=> ')

        else:
            print('--> Farmlist não esta ativado')
            print('')
            print('')
            print('')
            print('(A) Ativar Farmlist | (Q) Sair')
            print(f'')
            option = input('=> ')

        match option.lower():
            case 'd':
                    thread_farmlist.order_auto_send_farmlist = {}

                    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Farmlist desativado'
                    log.write(message)
                    print(message)
                    time.sleep(4)

            case 'a':
                if not thread_farmlist.order_auto_send_farmlist:
                    thread_farmlist.add(start_of_interval, end_of_interval)

                    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Farmlist Ativado'
                    log.write(message)
                    print(message)
                    time.sleep(4)
            case 'q':
                break

def menu_activities_list(name_village):
    
    while True:
        os.system('cls')
        print("____________________________________________________________")
        print(f'Account: {village.username}')
        print(f'Server: {village.server}')
        print("")
        print(F'Aldeia: {name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Lista de Atividades')
        print('')

        print("1 - Listar Atividades")
        print("2 - Excluir uma atividade")
        print('')
        print('')
        print('')
        print("(Q) Sair")
        print(f'')
        option = input('=> ')

        match option.lower():
            case "1":
                os.system('cls')
                print("____________________________________________________________")
                print(f'Account: {village.username}')
                print(f'Server: {village.server}')
                print("")
                print(F'Aldeia: {name_village}')
                print("____________________________________________________________")
                print('Menu -> Menu Principal -> Lista de Atividades - Listar')
                print('')

                for order in thread_construction[name_village].list_of_construction:
                    print(f' => {order["name_village"]} construindo {village.fields[name_village]["name"][int(order["slot_id"])-1]} para o level {order["to_level"]} ')
                            
                print('')
                input('Precione qualquer tecla para sair')
            case "2":
                pass
            case "q":
                break

def menu_quit_of_system(village):
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')
    village.quit()
    sys.exit()

if __name__ == "__main__":
    os.system('cls')
    server, username, password = get_information_on_account()
    print("____________________________________________________________")
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logando na sua conta, aguarde...')
    village = login_on_server(server, username, password)

    # Iniciando class Log
    log = Log(village)

    # INicializando Variavel de farmlist
    thread_farmlist = AutoSendFarmlist(village)
    thread_farmlist.daemon = True
    thread_farmlist.start()

    
    # Inicia as threads de construção
    thread_construction = {}
    for name_village in village.villages:
        thread_construction[name_village] = Construction(village)
        thread_construction[name_village].daemon = True
        thread_construction[name_village].start()

    log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logado na conta com sucesso')

    os.system('cls')

    while True:
        id_menu = menu()
        match id_menu:
            case '1':
                menu_set_village()
            case '2':
                menu_start_farmlist()
