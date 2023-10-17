import time
import datetime
from village import Village
from random import randint
import threading

"""
Melhorias

- Fazer o upgrade dos recursos aleatórios e não como uma seguencia do 1 ao 18
- Fazer o upgrade seguencia, por exemplo, se os recursos estão no level 3 e o
  usuário deseja atualizar para o level 5, fazer seguenciamente, primeiro, todos
  par ao level 4 e depois para o level 5!

"""

#Coloque aqui as informações de conexão com o servidor
server = "ts3.x1.america.travian.com"
username = "diviks"
password = "alves625"
"""
server = "ts30.x3.international.travian.com"
username = "dionialves"
password = "ranaeu21"
"""
def update_resources_fields_in_level(nameVillage, toLevel, list_ids):
    while True:
        village.update_building_orders(nameVillage)

        if not village.building_ordens[nameVillage]:
            for x in list_ids:
                if int(village.fields[nameVillage]['level'][int(x)-1]) < int(toLevel):
                    print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construindo {village.fields[nameVillage]["name"][int(x)-1]} para o level {toLevel}')

                    # Atualiza os recursos da aldeia
                    village.get_resources(nameVillage)

                    # retorna lista com recursos necessários para fazer a construção
                    resources = village.check_construction_resources(x)

                    if (int(village.resources[nameVillage]['lumber']) >= int(resources['lumber']) and
                        int(village.resources[nameVillage]['clay']) >= int(resources['clay'])  and
                        int(village.resources[nameVillage]['iron']) >= int(resources['iron'])  and
                        int(village.resources[nameVillage]['crop']) >= int(resources['crop'])):

                        village.upgrade_fields_resource(nameVillage, x)
                        village.update_building_orders(nameVillage)
                        # Atualiza manualmente o nivel do campo
                        village.fields[nameVillage]['level'][int(x)-1] = str(int(village.fields[nameVillage]['level'][int(x)-1]) + 1)

                        break
                    else:
                        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir')

        else:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Identificado que já tem construções na fila')

        if village.building_ordens[nameVillage]:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Tempo de espera: {datetime.timedelta(minutes=int(village.building_ordens[nameVillage][0][2] / 60 + 2))} minutos')
            time.sleep(int(village.building_ordens[nameVillage][0][2] + 120))

        else:
            if not level_up(nameVillage, toLevel):
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos')
                time.sleep(600)

        if level_up(list_names[int(idVillage)-1], toLevel):
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construção já atingiu o nível solicitado!')
            break

def level_up(nameVillage, toLevel):
    for x in range(18):
        if int(village.fields[nameVillage]["level"][x]) < int(toLevel):
            return False
    return True

def start_farm_list(timeStart, timeEnd):
    while True:
        village.start_all_farm_list(list_names[int(idVillage)-1])

        timeStart = randint(int(minuteStart), int(timeEnd))
        hours = datetime.datetime.now().strftime("%H:%M:%S")
        nextStart = datetime.datetime.now() + datetime.timedelta(minutes=timeStart)
        nextStart = nextStart.strftime("%H:%M:%S")

        print(f'{hours} - Realizado o assalto, o proximo esta programado para as {nextStart} ')
        time.sleep(timeStart*60)



if __name__ == "__main__":
    """
    Inicializa e loga na conta, pegando informações basicas da aldeia
    """
    village = Village()
    village.login(server, username, password)
    time.sleep(2)
    village.update_name_villages()

    while True:
        """
        Pega informação da aldeia a ser atualizada e o level dos recursos
        """

        print("____________________________________________________________")
        print("Escolha a aldeia a evoluir: ")
        aux = 1
        list_names = []
        for x in village.villages:
            print(f'{aux} - {x}')
            list_names.append(x)
        idVillage = input('=> ')

        print("Quais tarefas deseja fazer:")
        print("1 - Upgrade de recursos")
        print("2 - Upgrade de Edifícios")
        print("3 - Start lista de farms")
        print("4 - Lista de atividades")
        print("5 - Sair")
        option = input("=> ")

        if option == "1":
            toLevel = input("Escolha qual level deseja evoluir os recursos: ")

            list_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando campos')
            village.update_fields_village(list_names[int(idVillage)-1], list_ids)

            thread = threading.Thread(name=f'Update recursos para o Nível {toLevel}', target=update_resources_fields_in_level, args=(list_names[int(idVillage)-1], toLevel, list_ids))
            thread.start()

        elif option == "2":
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Atualizando aldeia, aguarde...')
            village.update_fields_village(list_names[int(idVillage)-1], range(1,41))

            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Listando construções disponíveis para upgrade:')
            for x in range(19,41):
                
                if village.fields[list_names[int(idVillage)-1]]['level'][x-1] != "0":
                    print(f'id: {x} | ({village.fields[list_names[int(idVillage)-1]]["level"][x-1]}) - {village.fields[list_names[int(idVillage)-1]]["name"][x-1]}')
            
            builderUpdate = input('Id => ')
            toLevel = input('Upgrade para qual nível => ')

            thread = threading.Thread(name=f'Construindo {village.fields[list_names[int(idVillage)-1]]["name"][x-1]} para o Nível {toLevel}', target=update_resources_fields_in_level, args=(list_names[int(idVillage)-1], toLevel, [builderUpdate]))
            thread.start()

        elif option == "3":

            print('O Inicio da assalto será definido entre um intervalod de tempo, informa abaixo esse itervalo:')
            print('Digite o numero inicial do intervalo (em minutos):')
            minuteStart = input('=> ')

            print('Digite o numero final do intervalo (em minutos:)')
            minuteEnd = input('=> ')

            thread = threading.Thread(name=f'Assaltando via farmlist da aldeia {list_names[int(idVillage)-1]}', target=start_farm_list, args=(minuteStart, minuteEnd))
            thread.start()

        elif option == "4":
            print("____________________________________________________________")
            print("Abaixo o que já esta sendo feito na aldeia:")
            for t in threading.enumerate():
                if t.name != 'MainThread':
                    print(f'=> {t.name}')

        elif option == "5":
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Saindo do Travian Village Bot')
            break

        else:
            print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Por favor escolha umas das opções abaixo')