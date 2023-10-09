from village import Village
from selenium.webdriver.common.by import By
import time

#Coloque aqui as informações de conexão com o servidor
server = ""
username = ""
password = ""


village = Village()
village.login(server, username, password)

time.sleep(5)
print("##########################################################################")

# Pegar lista das vilas
village.update_name_villages()
print(village.villages)

print("##########################################################################")

# Atualizar lista de campos e seus leveis de uma vila
#for vil in village.villages:
#    village.update_fields_village(vil)
#    print(vil)
#    print("--------------------------------")
#    for x in range(40):
#        print(village.fields[vil]['name'][x] + " - " + village.fields[vil]['level'][x])

#print("##########################################################################")

#for vil in village.villages:
#    village.update_building_orders(vil)
#    print(village.building_ordens[vil])

#print("##########################################################################")

for vil in village.villages:
    village.get_resources(vil)
print(village.resources)

while True:

    print("Verificando se tem construções na fila")
    village.update_building_orders('Aldeia do diviks')

    if not village.building_ordens['Aldeia do diviks']:
        print("Iniciando construção")
        print("Atualizando campos")
        village.update_fields_village('Aldeia do diviks')

        for x in range(18):
            print("iniciando laço de numero " + str(x+1))
            
            print("verificando se campo é menor que 5")
            if int(village.fields['Aldeia do diviks']['level'][x]) < 5:
                print("Construindo campo")

                # Atualiza os recursos da aldeia
                village.get_resources('Aldeia do diviks')

                # retorna lista com recursos necessários para fazer a construção
                resources = village.check_construction_resources(x+1)

                if (int(village.resources['Aldeia do diviks']['lumber']) >= int(resources['lumber']) and
                    int(village.resources['Aldeia do diviks']['clay']) >= int(resources['clay'])  and
                    int(village.resources['Aldeia do diviks']['iron']) >= int(resources['iron'])  and
                    int(village.resources['Aldeia do diviks']['crop']) >= int(resources['crop'])):

                    village.upgrade_fields_resource('Aldeia do diviks', x+1)
                    village.update_building_orders('Aldeia do diviks')
                    break

            else:
                print("Campo já esta no nível desejado")

    else:
        print("Identificado que já tem construções na fila")

    if village.building_ordens['Aldeia do diviks']:
        print(f'Tempo de espera: {round(int(village.building_ordens["Aldeia do diviks"][0][2]) / 60 + 2, 0)} minutos')
        time.sleep(int(village.building_ordens['Aldeia do diviks'][0][2] + 120))
    
    else:
        print("Sem recursos suficientes para construir, vamos aguardar 20 minutos")
        time.sleep(600)

