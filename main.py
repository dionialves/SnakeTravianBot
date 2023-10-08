from village import Village
from selenium.webdriver.common.by import By
import time

server = "ts3.x1.america.travian.com"
username = "diviks"
password = "alves625"


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
            
            print("verificando se campo é menor que 4")
            if int(village.fields['Aldeia do diviks']['level'][x]) < 4:
                print("Construindo campo")
                village.upgrade_fields_resource('Aldeia do diviks', x+1)
                break

            else:
                print("Campo já esta no nível desejado")

    else:
        print("Identificado que já tem construções na fila")
            
    print("iniciando espera de 20minutos")
    time.sleep(1200)

