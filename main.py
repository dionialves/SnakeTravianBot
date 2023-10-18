import time
import datetime
import tkinter as tk
from village import Village
from random import randint
import threading

"""
Melhorias

- Fazer o upgrade seguencia, por exemplo, se os recursos estão no level 3 e o
  usuário deseja atualizar para o level 5, fazer seguenciamente, primeiro, todos
  par ao level 4 e depois para o level 5!

- Colocar as mensagens em um novo terminal
"""

class MenssageOutput(object):
    def __init__(self):
        self.root = tk.Tk()
        self.text = tk.Text(self.root, bg = 'black', fg='white', height=20, width=80)
        self.text.pack(side=tk.LEFT, fill=tk.Y)


    def inset_text(self, text):
        self.text.insert(tk.END, text)
        
def update_resources_fields_in_level(village, nameVillage, toLevel, list_of_ids):
    while True:
        village.update_building_orders(nameVillage)
        
        if not village.building_ordens[nameVillage]:
            for x in list_of_ids:

                #atualiza o campo em específico
                village.update_fields_village(nameVillage, [x])

                # Verifica se ele esta abaixo do nível desejado
                if int(village.fields[nameVillage]['level'][int(x)-1]) < int(toLevel):

                    # Atualiza os recursos da aldeia
                    village.get_resources(nameVillage)

                    # retorna lista com recursos necessários para fazer a construção
                    resources = village.check_construction_resources(x)

                    # Verifica se tem os rercursos necessário para fazer a construção
                    if (int(village.resources[nameVillage]['lumber']) >= int(resources['lumber']) and
                        int(village.resources[nameVillage]['clay']) >= int(resources['clay'])  and
                        int(village.resources[nameVillage]['iron']) >= int(resources['iron'])  and
                        int(village.resources[nameVillage]['crop']) >= int(resources['crop'])):

                        village.upgrade_fields_resource(nameVillage, x)
                        village.update_building_orders(nameVillage)

                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construindo {village.fields[nameVillage]["name"][int(x)-1]} para o level {int(village.fields[nameVillage]["level"][int(x)-1])+1}')

                        break
                    else:
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos')
                        time.sleep(600)

                else:
                    # Verifica se ele esta abaixo do nível desejado
                    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construção já atingiu o nível solicitado!')
                    break

        else:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Identificado que já tem construções na fila')

        if village.building_ordens[nameVillage]:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Tempo de espera: {datetime.timedelta(minutes=int(village.building_ordens[nameVillage][0][2] / 60 + 2))} minutos')
            time.sleep(int(village.building_ordens[nameVillage][0][2] + 120))

def start_farm_list(village, name_village, minuteStart, minuteEnd):
    while True:
        village.start_all_farm_list(name_village)

        timeStart = randint(int(minuteStart), int(minuteEnd))
        hours = datetime.datetime.now().strftime("%H:%M:%S")
        nextStart = datetime.datetime.now() + datetime.timedelta(minutes=timeStart)
        nextStart = nextStart.strftime("%H:%M:%S")

        print(f'{hours} - Realizado o assalto, o proximo esta programado para as {nextStart} ')
        time.sleep(timeStart*60)

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
    print("____________________________________________________________")
    print("Escolha a aldeia a evoluir: ")
    aux = 1
    list_names = []
    for x in village.villages:
        print(f'{aux} - {x}')
        list_names.append(x)
    idVillage = input('=> ')
    name_village = list_names[int(idVillage)-1]

    print("Quais tarefas deseja fazer:")
    print("1 - Upgrade de recursos")
    print("2 - Upgrade de Edifícios")
    print("3 - Start lista de farms")
    print("4 - Lista de atividades")
    print("5 - Sair")
    option = input("=> ")

    return name_village, option

def menu_update_fields(village, name_village):
        print("Escolha qual level deseja evoluir os recursos: ")
        toLevel = input('=> ')

        fields_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando campos')
        village.update_all_fields_village(name_village)

        thread = threading.Thread(name=f'Update recursos para o Nível {toLevel}', 
                                  target=update_resources_fields_in_level, 
                                  args=(village, name_village, toLevel, fields_id))
        thread.start()

def menu_update_buildings(village, name_village):
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando aldeia, aguarde...')
        village.update_all_fields_village(name_village)

        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Listando construções disponíveis para upgrade:')
        for x in range(19,41):
            
            if village.fields[name_village]['level'][x-1] != "0":
                print(f'id: {x} | ({village.fields[name_village]["level"][x-1]}) - {village.fields[name_village]["name"][x-1]}')
        
        builder_id = input('Id => ')
        toLevel = input('Upgrade para qual nível => ')

        thread = threading.Thread(name=f'Construindo {village.fields[name_village]["name"][x-1]} para o Nível {toLevel}', 
                                  target=update_resources_fields_in_level, 
                                  args=(village, name_village, toLevel, [builder_id]))
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
    server, username, password = get_information_on_account()
    village = login_on_server(server, username, password)

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