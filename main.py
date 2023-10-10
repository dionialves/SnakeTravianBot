from village import Village
from selenium.webdriver.common.by import By
import time
import datetime

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

def update_resources_fields_in_level(nameVillage, toLevel, list_ids):
    village.update_building_orders(nameVillage)

    if not village.building_ordens[nameVillage]:

        for x in list_ids:
            if int(village.fields[nameVillage]['level'][int(x)-1]) < int(toLevel):
                print(f'{datetime.datetime.now().strftime("%I:%M")} - Construindo {village.fields[nameVillage]["name"][int(x)-1]} para o level {toLevel}')

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
                    break
                else:
                    print(f'{datetime.datetime.now().strftime("%I:%M")} - Sem recursos suficientes para construir')

    else:
        print(f'{datetime.datetime.now().strftime("%I:%M")} - Identificado que já tem construções na fila')

    if village.building_ordens[nameVillage]:
        print(f'{datetime.datetime.now().strftime("%I:%M")} - Tempo de espera: {round(int(village.building_ordens[nameVillage][0][2]) / 60 + 2, 0)} minutos')
        time.sleep(int(village.building_ordens[nameVillage][0][2] + 120))

    else:
        if not level_up(nameVillage, toLevel):
            print(f'{datetime.datetime.now().strftime("%I:%M")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos')
            time.sleep(600)

def level_up(nameVillage, toLevel):
    for x in range(18):
        if int(village.fields[nameVillage]["level"][x]) < int(toLevel):
            return False
    return True


if __name__ == "__main__":
    """
    Inicializa e loga na conta, pegando informações basicas da aldeia
    """
    village = Village()
    village.login(server, username, password)
    time.sleep(2)
    village.update_name_villages()

    """
    Pega informação da aldeia a ser atualizada e o level dos recursos
    """
    print("Escolha a aldeia a evoluir: ")
    aux = 1
    list_names = []
    for x in village.villages:
        print(f'{aux} - {x}')
        list_names.append(x)
    idVillage = input('=> ')

    print("Quais tarefas desefa fazer:")
    print("1 - Upgrade de recursos")
    print("2 - Upgrade de Edifícios")
    option = input("=> ")

    if option == "1":
        """
        ###########################################################################
        Upgrade de recursos
        """
        toLevel = input("Escolha qual level deseja evoluir os recursos: ")
        
        """
        Inicia o loop do programa
        """

        list_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        print(f'{datetime.datetime.now().strftime("%I:%M")} - Atualizando campos')
        village.update_fields_village(list_names[int(idVillage)-1], list_ids)

        while True:
            update_resources_fields_in_level(list_names[int(idVillage)-1], toLevel, list_ids)
            
            if level_up(list_names[int(idVillage)-1], toLevel):
                print(f'Aldeia já atingiu o nível solicitado!')
                break

    elif option == "2":
        village.update_fields_village(list_names[int(idVillage)-1], range(1,41))

        print(f'{datetime.datetime.now().strftime("%I:%M")} - Listando construções disponíveis para upgrade:')
        for x in range(19,41):
            
            if village.fields[list_names[int(idVillage)-1]]['level'][x-1] != "0":
                print(f'id: {x} | ({village.fields[list_names[int(idVillage)-1]]["level"][x-1]}) - {village.fields[list_names[int(idVillage)-1]]["name"][x-1]}')
        
        builderUpdate = input('Id => ')
        toLevel = input('Upgrade para qual nível => ')

        while True:
            update_resources_fields_in_level(list_names[int(idVillage)-1], toLevel, [builderUpdate])