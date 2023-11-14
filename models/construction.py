import random
import datetime
from threading import Thread, Event

from models.log import Log
from models.database import Database


class Construction(Thread):
    """
    list_of_construction: Esta variavel é o motor dessa classe, atraves dela 
    que a thread é controlada. Assim que a thead for inicada, basta adicionar
    as informações conform padrão abaixo e ela começa a construir, campo por 
    campo, até a fila não ter mais itens
    [
        {
            'village': 'village', 
            'slot_id': 'slot_id',
            'to_level': 'to_level'
        }
    ]

    wait: É um valor ramdomico que 

    """
    def __init__(self, travian):
        super().__init__()

        self.list_of_construction = []
        self.event = Event()
        self.travian = travian
        self.log = Log(travian)
        self.database = Database(travian)

    def add(self, village, slot_id, to_level):
        self.list_of_construction.append({
            'village': village, 
            'slot_id': slot_id,
            'to_level': to_level
            }
        )

    def construction_for_resourses(self, village, toLevel, list_of_ids):
        for to_level in range(1, int(toLevel)+1):
            for slot_id in list_of_ids:

                level = self.travian.villages[village]['slot'][slot_id]['level']
                if int(level) < int(to_level):
                    self.add(village, slot_id, to_level)

    def run(self):
        while not self.event.is_set():
            self.event.wait(1)

            if self.list_of_construction:

                # Essa variavel no futuro será definida delo usuário
                self.wait = random.randint(300, 600)

                construction = self.list_of_construction[0]

                village = construction['village']
                slot_id = construction['slot_id']
                to_level = construction['to_level']

                #atualiza o campo em específico 
                self.travian.update_only_slot(village, slot_id)
                self.database.write(str(self.travian.villages))

                slot_name = self.travian.villages[village]['slot'][slot_id]['name']
                current_level = self.travian.villages[village]['slot'][slot_id]['level']

                # Verifica se já esta no nível desejado
                if int(current_level) >= int(to_level):
                    self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> {slot_name} já atingiu o nível solicitado!')
                    del self.list_of_construction[0]
                else:
                    # Verifica se tem alguma construção já em andamento
                    self.travian.get_upgrade_orders(village)
                    if self.travian.upgrade_orders[village]:
                        time_in_update = datetime.timedelta(minutes=int(self.travian.upgrade_orders[village][0][2] / 60 + 2))

                        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Construção na fila, tempo de espera: {time_in_update} minutos')
                        self.event.wait(int(self.travian.upgrade_orders[village][0][2] + self.wait))

                    else:
                        # Verifica se a aldeia tem recursos para fazer a construção
                        if self.travian.check_resources_for_update_slot(village, slot_id):

                            self.travian.upgrade_to_level(village, slot_id)
                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Construindo {slot_name} para o level {int(current_level) +1}')
                        else:
                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Sem recursos suficientes para construir, vamos aguardar 10 minutos')
                            self.event.wait(600)

                
