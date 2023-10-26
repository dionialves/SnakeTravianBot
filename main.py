import os
import ast
import time
import datetime
import threading
from random import randint
from watchdog.observers import Observer

from models.village import Village
from models.construction import Construction
from models.log import Log


"""
Essa função é responsável por atualizar um grupo de slots até determinado level, será usada para evoluir campos recursos
pois serão feitos de forma sequencial.

Funções usada para esse processo:

-> update_resources_fields_in_level
-> check_resources_for_construction
-> slot_construction
"""

def update_resources_fields_in_level(village, name_village, toLevel, list_of_ids):
    for to_level in range(1, int(toLevel)+1):
        for slot_id in list_of_ids:
            if int(village.fields[name_village]["level"][int(slot_id)-1]) < int(to_level):

                thread_construction[name_village].list_of_construction.append({
                        'name_village': name_village, 
                        'slot_id': slot_id,
                        'to_level': to_level
                    }
                )
     
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

        message = f'{hours} - Realizado o assalto, o proximo esta programado para as {nextStart}'
        log(village, message)
        time.sleep(timeStart*60)

def get_database(village, name_village):
    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Verificando database'
    log(village, message)
    if os.path.isfile(f'{village.username}.database'):
        message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Carregado database com sucesso'
        log(village, message)

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
    log(village, message)
    print(message)
    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos'
    log(village, message)
    print(message)
    village.update_all_fields_village(name_village)
    set_database(village)

def set_database(village):
    with open(f'{village.username}.database', 'w') as file:
        file.write(str(village.fields))

def log(village, message):
    with open(f'{village.username}.logs', 'a') as file:
        file.write(message + '\n')

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
        print("Escolha a aldeia a evoluir: ")
        print('')
        name_village = ''
        list_names = []
        aux = 1
        for x in village.villages:
            print(f'{aux} - {x}')
            list_names.append(x)
            aux = aux + 1
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

    return name_village

def menu_of_village(village, name_village):
    
    option = ""
    while True:
        os.system('cls')
        print(F'{name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal')
        print('')
        
        print("1 - Recursos e Edifícios")
        print("2 - Atualizar Aldeia")
        print("3 - Auto send farmlist")
        print("4 - Lista de atividades")
        print('')
        print("(Q) Sair")
        option = input("=> ")

        match option.lower():
            case "1": 
                resorurses_and_buildings(village, name_village)
            case "2":
                menu_update_village(village, name_village)
            case "3":
                menu_start_farmlist(village, name_village)
            case "4":
                menu_activities_list()
            case "q":
                break
            case _:
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Por favor escolha umas das opções abaixo')


def resorurses_and_buildings(village, name_village):
        while True:
            os.system('cls')
            print(F'{name_village}')
            print("____________________________________________________________")
            print('Menu -> Menu Principal -> Recursos e Edificações')
            print('')
            print('1 - Listar Campos de Recursos')
            print('2 - Listar Edifícios')
            print('3 - Update Campos de Recursos')
            print('4 - Update Edifícios')
            print('')
            print('(Q) Sair')

            option = input('=> ')

            match option.lower():
                case '1':
                    os.system('cls')
                    print(F'{name_village}')
                    print("____________________________________________________________")
                    print('Menu -> Menu Principal -> Recursos e Edificações -> Listar Campos de Recursos')
                    print('')
                    for slot in range(0, 18):
                        print(f'({village.fields[name_village]["level"][int(slot)]}) {village.fields[name_village]["name"][int(slot)]}')
                    
                    print('')
                    input('Precione qualquer tecla para sair')

                case '2':
                    os.system('cls')
                    print(F'{name_village}')
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
                        print(F'{name_village}')
                        print("____________________________________________________________")
                        print('Menu -> Menu Principal -> Recursos e Edificações -> Update Campos de Recursos')
                        print('')
                        print("1 - Apenas Cereal")
                        print("2 - Apenas Madeira, Barro e Ferro")
                        print("3 - Todos os recuros")
                        option = input("=> ")

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
                            update_resources_fields_in_level(village, name_village, toLevel, list_of_ids)
                            
                            print('')
                            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                            time.sleep(4)
                        os.system('cls')
                        break
                case '4':
                    while True:
                        os.system('cls')
                        print(F'{name_village}')
                        print("____________________________________________________________")
                        print('Menu -> Menu Principal -> Recursos e Edificações -> Update Edifícios')
                        print('')
                        for slot in range(18,40):
                            
                            if village.fields[name_village]['level'][slot] != "0":
                                print(f'id: {slot+1} | ({village.fields[name_village]["level"][slot]}) - {village.fields[name_village]["name"][slot]}')
                        
                        slot_id = input('Id => ')
                        to_level = input('Upgrade para qual nível => ')

                        if slot_id and to_level:
                            thread_construction[name_village].list_of_construction.append({
                                    'name_village': name_village, 
                                    'slot_id': slot_id,
                                    'to_level': to_level
                                }
                            )
                            
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
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando dados, isso pode levar alguns minutos')
    village.update_all_fields_village(name_village)
    set_database(village)

def menu_start_farmlist(village, name_village):
    print('O Inicio da assalto será definido entre um intervalod de tempo, informa abaixo esse itervalo:')
    print('Digite o numero inicial do intervalo (em minutos):')
    minuteStart = input('=> ')

    print('Digite o numero final do intervalo (em minutos:)')
    minuteEnd = input('=> ')

    thread = threading.Thread(name=f'{name_village} - Ativado auto farmlist', 
                              target=start_farm_list, 
                              args=(village, name_village, minuteStart, minuteEnd))
    
    print('')
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Started Automatic farmlist submission')
    time.sleep(4)
    thread.start()

def menu_activities_list():
    
    while True:
        os.system('cls')
        print(F'{name_village}')
        print("____________________________________________________________")
        print('Menu -> Menu Principal -> Lista de Atividades')
        print('')

        print("1 - Listar Atividades")
        print("2 - Excluir uma atividade")
        print('')
        print("(Q) Sair")

        option = input('=> ')

        match option.lower():
            case "1":
                os.system('cls')
                print(F'{name_village}')
                print("____________________________________________________________")
                print('Menu -> Menu Principal -> Lista de Atividades - Listar')
                print('')

                for order in thread_construction[name_village].list_of_construction:
                    print(f' =>{order["name_village"]} construindo {village.fields[name_village]["name"][int(order["slot_id"])-1]} para o level {order["to_level"]} ')
                            
                print('')
                input('Precione qualquer tecla para sair')
            case "2":
                pass
            case "q":
                break

def menu_quit_of_system(village):
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')
    village.quit()


if __name__ == "__main__":
    os.system('cls')
    server, username, password = get_information_on_account()
    print("____________________________________________________________")
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logando na sua conta, aguarde...')
    village = login_on_server(server, username, password)


    # Inicia as threads de construção
    thread_construction = globals()
    for name_village in village.villages:
        thread_construction[name_village] = Construction(village)
        thread_construction[name_village].daemon = True
        thread_construction[name_village].start()

    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logado na conta com sucesso'
    log(village, message)

    os.system('cls')

    while True:
        name_village = menu()
        if name_village:
            menu_of_village(village, name_village)
        else:
            menu_quit_of_system(village)
            break