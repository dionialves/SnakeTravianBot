import os
import time
import datetime
import threading
import tkinter as tk
from random import randint

from models.village import Village

"""
Melhorias

- Fazer o upgrade seguencia, por exemplo, se os recursos estão no level 3 e o
  usuário deseja atualizar para o level 5, fazer seguenciamente, primeiro, todos
  par ao level 4 e depois para o level 5!

- Tratar erros quando o selenium por qualquer motivo não encontra o elemento

- Colocar as mensagens em um novo terminal

- Quando tem mais de um id para fazer o upgrade, 
"""



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

    
def check_resources_for_construction(village, name_village, id_field):
    # Atualiza os recursos da aldeia
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando quantidades de recursos na aldeia')
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
        
        if int(village.fields[name_village]['level'][int(id_field)-1]) >= int(level):
            # Verifica se ele esta abaixo do nível desejado
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - {village.fields[name_village]["name"][int(id_field)-1]} já atingiu o nível solicitado!')
            break

        village.update_building_orders(name_village)
        if village.building_ordens[name_village]:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construção na fila, tempo de espera: {datetime.timedelta(minutes=int(village.building_ordens[name_village][0][2] / 60 + 2))} minutos')
            time.sleep(int(village.building_ordens[name_village][0][2] + 120))
        else:
            # Entra na função para fazer a verificação se tem recursos para update
            if check_resources_for_construction(village, name_village, id_field):
                village.upgrade_fields_resource(name_village, id_field)

                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construindo {village.fields[name_village]["name"][int(id_field)-1]} para o level {int(village.fields[name_village]["level"][int(id_field)-1])+1}')
            else:
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos')
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

        print(f'{hours} - Realizado o assalto, o proximo esta programado para as {nextStart} ')
        time.sleep(timeStart*60)


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
    village.login(server, username, password)
    time.sleep(2)
    village.update_name_villages()

    return village


""" Funções relacionadas ao Menu"""
def menu():
    while True:
        print("____________________________________________________________")
        print("Escolha a aldeia a evoluir: ")
        
        list_names = []
        aux = 1
        for x in village.villages:
            print(f'{aux} - {x}')
            list_names.append(x)
            aux = aux + 1

        idVillage = input('=> ')
        try:
            if int(idVillage) >= 1:
                name_village = list_names[int(idVillage)-1]
                break
        except:
            print('Escolha uma das aldeias listada acima!')

    os.system('cls')
    option = ""
    while (option not in ('1', '2', '3', '4', '5')):

        print("Quais tarefas deseja fazer:")
        print("1 - Upgrade de recursos")
        print("2 - Upgrade de Edifícios")
        print("3 - Start lista de farms")
        print("4 - Lista de atividades")
        print("5 - Sair")
        option = input("=> ")

    return name_village, option

def menu_update_fields(village, name_village):
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando campos')
        village.update_all_fields_village(name_village)

        print("Deseja evoluir quais tipos de recurso: ")
        print("1 - Apenas Cereal")
        print("2 - Apenas Madeira, Barro e Ferro")
        print("3 - Todos os recuros")
        option_resources = input("=> ")

        print("Escolha qual level deseja evoluir os recursos: ")
        toLevel = input('=> ')

        match option_resources:
            case "1":
                fields_id = village.get_only_crop(name_village)
            case "2":
                fields_id = village.get_no_crop(name_village)
            case "3":
                fields_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            case _:
                pass

        thread = threading.Thread(name=f'Update recursos para o Nível {toLevel}', 
                                  target=update_resources_fields_in_level, 
                                  args=(village, name_village, toLevel, fields_id))
        thread.start()

def menu_update_buildings(village, name_village):
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando campos')
        village.update_all_fields_village(name_village)
        
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Listando construções disponíveis para upgrade:')
        for x in range(19,41):
            
            if village.fields[name_village]['level'][x-1] != "0":
                print(f'id: {x} | ({village.fields[name_village]["level"][x-1]}) - {village.fields[name_village]["name"][x-1]}')
        
        builder_id = input('Id => ')
        toLevel = input('Upgrade para qual nível => ')

        thread = threading.Thread(name=f'Construindo {village.fields[name_village]["name"][x-1]} para o Nível {toLevel}', 
                                  target=upgrade_slot_to_level, 
                                  args=(village, name_village, builder_id, toLevel))
        thread.start()

def menu_start_farmlist(village, name_village):
    print('O Inicio da assalto será definido entre um intervalod de tempo, informa abaixo esse itervalo:')
    print('Digite o numero inicial do intervalo (em minutos):')
    minuteStart = input('=> ')

    print('Digite o numero final do intervalo (em minutos:)')
    minuteEnd = input('=> ')

    thread = threading.Thread(name=f'Assaltando via farmlist da aldeia {name_village}', 
                              target=start_farm_list, 
                              args=(village, name_village, minuteStart, minuteEnd))
    thread.start()

def menu_activities_list():
    print("____________________________________________________________")
    print("Abaixo o que já esta sendo feito na aldeia:")
    for t in threading.enumerate():
        if t.name != 'MainThread':
            print(f'=> {t.name}')

def menu_quit_of_system():
    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')



if __name__ == "__main__":
    os.system('cls')
    server, username, password = get_information_on_account()
    village = login_on_server(server, username, password)

    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Logado na conta, bom jogo')

    while True:
        name_village, option = menu()

        match option:
            case "1": 
                menu_update_fields(village, name_village)
            case "2":
                menu_update_buildings(village, name_village)
            case "3":
                menu_start_farmlist(village, name_village)
            case "4":
                menu_activities_list()
            case "5":
                menu_quit_of_system()
                break
            case _:
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Por favor escolha umas das opções abaixo')