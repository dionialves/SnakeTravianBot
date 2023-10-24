import os
import ast
import time
import datetime
import threading
from random import randint

from models.village import Village


"""
Essa função é responsável por atualizar um grupo de slots até determinado level, será usada para evoluir campos recursos
pois serão feitos de forma sequencial.

Funções usada para esse processo:

-> update_resources_fields_in_level
-> check_resources_for_construction
-> slot_construction
"""

def update_resources_fields_in_level(village, name_village, toLevel, list_of_ids):
    for level in range(1, int(toLevel)+1):
        for id_field in list_of_ids:
            if int(village.fields[name_village]["level"][int(id_field)-1]) < int(level):
                upgrade_slot_to_level(village, name_village, id_field, level)
    
    time.sleep(2)   
    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Todos os recursos já foram atualizados para o level {toLevel}'
    log(village, message)
    

def check_resources_for_construction(village, name_village, id_field):
    # Atualiza os recursos da aldeia
    message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando quantidades de recursos na aldeia'
    log(village, message)
    village.get_resources(name_village)

    # retorna lista com recursos necessários para fazer a construção
    resources = village.check_construction_resources(id_field)

    # Verifica se tem os rercursos necessário para fazer a construção
    if (int(village.resources[name_village]['lumber']) >= int(resources['lumber']) and
        int(village.resources[name_village]['clay']) >= int(resources['clay'])  and
        int(village.resources[name_village]['iron']) >= int(resources['iron'])  and
        int(village.resources[name_village]['crop']) >= int(resources['crop'])):
        return True
    else:
        return False
    
"""
Esta função será utiliza para realizar o upgrade de um determinado edificio até o nível desejado.
Serão usados para isso os slots que já possuirem uma construção 
"""
def upgrade_slot_to_level(village, name_village, id_field, level):

    while True:
        #atualiza o campo em específico 
        village.update_fields_village(name_village, [id_field])
        set_database(village)

        if int(village.fields[name_village]['level'][int(id_field)-1]) >= int(level):
            # Verifica se ele esta abaixo do nível desejado
            message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - {village.fields[name_village]["name"][int(id_field)-1]} já atingiu o nível solicitado!'
            log(village, message)
            break

        village.update_building_orders(name_village)
        if village.building_ordens[name_village]:
            message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construção na fila, tempo de espera: {datetime.timedelta(minutes=int(village.building_ordens[name_village][0][2] / 60 + 2))} minutos'
            log(village, message)
            time.sleep(int(village.building_ordens[name_village][0][2] + 120))
        else:
            # Entra na função para fazer a verificação se tem recursos para update
            if check_resources_for_construction(village, name_village, id_field):
                village.upgrade_fields_resource(name_village, id_field)

                message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construindo {village.fields[name_village]["name"][int(id_field)-1]} para o level {int(village.fields[name_village]["level"][int(id_field)-1])+1}'
                log(village, message)
            else:
                message = f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos'
                log(village, message)
                time.sleep(600)

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
    os.system('cls')
    print('Print of Logs')
    print("____________________________________________________________")
    print('Menu -> Logs')
    print('')
    with open(f'{village.username}.logs', 'r') as file:
        lines = file.readlines()
        lines = lines[-15:]

    for line in lines:
        print(line, end='')

    print('')
    input('Precione qualquer tecla para sair')


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
                                fields_id = village.get_only_crop(name_village)
                            case "2":
                                fields_id = village.get_no_crop(name_village)
                            case "3":
                                fields_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                            case _:
                                pass
                        if option and toLevel:
                            thread = threading.Thread(name=f'{name_village} - Update recursos para o Nível {toLevel}', 
                                                    target=update_resources_fields_in_level, 
                                                    args=(village, name_village, toLevel, fields_id))
                            
                            print('')
                            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                            time.sleep(4)
                            thread.start()
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
                        
                        builder_id = input('Id => ')
                        toLevel = input('Upgrade para qual nível => ')

                        if builder_id and toLevel:
                            thread = threading.Thread(name=f'{name_village} - Construindo {village.fields[name_village]["name"][int(builder_id)-1]} para o Nível {toLevel}', 
                                                    target=upgrade_slot_to_level, 
                                                    args=(village, name_village, builder_id, toLevel))
                            
                            print('')
                            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Ordem de construção adicionado na fila')
                            time.sleep(4)
                            thread.start()
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
                for thread in threading.enumerate():
                    if thread.name != 'MainThread':
                        if name_village in thread.name:
                            print(f'=> {thread.name}')
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