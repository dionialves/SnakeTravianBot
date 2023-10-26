import random
import datetime
from threading import Thread, Event

from models.log import Log


class Construction(Thread):
    def __init__(self, village):
        super().__init__()
        """
        Esta variavel precisa ser preenchida com a seguinte ordem:
        [
            
            {
                'name_village': 'name_village', 
                'slot_id': 'slot_id',
                'to_level': 'to_level'
            }
            
        ]
        name_village = Nome da aldeia
        slot_id = Slot a ser construido
        to_level = level a ser atualizado

        """
        self.list_of_construction = []
        self.event = Event()
        self.village = village
        self.log = Log(village)

    def run(self):
        while not self.event.is_set():
            if self.list_of_construction:
                construction = self.list_of_construction[0]

                name_village = construction['name_village']
                slot_id = construction['slot_id']
                to_level = construction['to_level']

                #atualiza o campo em específico 
                self.village.update_fields_village(name_village, [slot_id])

                current_level = self.village.fields[name_village]['level'][int(slot_id)-1]
                slot_name = self.village.fields[name_village]["name"][int(slot_id)-1]

                # Verifica se já esta no nível desejado
                if int(current_level) >= int(to_level):
                    self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - {slot_name} já atingiu o nível solicitado!')
                    del self.list_of_construction[0]
                else:
                    # Verifica se tem alguma construção já em andamento
                    self.village.update_building_orders(name_village)
                    if self.village.building_ordens[name_village]:
                        time_in_update = datetime.timedelta(minutes=int(self.village.building_ordens[name_village][0][2] / 60 + 2))

                        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construção na fila, tempo de espera: {time_in_update} minutos')
                        self.event.wait(int(self.village.building_ordens[name_village][0][2] + random.randint(120, 600)))

                    else:
                        # Verifica se a aldeia tem recursos para fazer a construção
                        if self.village.check_resources_for_update_slot(name_village, slot_id):

                            self.village.upgrade_fields_resource(name_village, slot_id)
                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Construindo {slot_name} para o level {int(current_level) +1}')
                        else:
                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} - Sem recursos suficientes para construir, vamos aguardar 10 minutos')
                            self.event.wait(600)