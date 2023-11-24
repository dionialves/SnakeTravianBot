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
    def __init__(self, travian, browser):
        super().__init__()

        self.list_of_construction = []
        self.event = Event()
        self.travian = travian
        self.log = Log(travian)
        self.database = Database(travian)
        self.browser = browser

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
                """
                A lista a ser manipulada, será a de ordens de upgrade, adicionando na ultima posição o status de possível de ser atualizada.
                É preciso rodar uma função, pegar a primeira posição na lista a ser atualização e verificar se tem os recursos necessários
                se tiver, coloca um status de "pronto para atualziação".

                Nessa classe, iremos pegar esse item que esta pronto para atualização e atualizar, caso não esteja, será necessario aguardar.
                """

                # Essa variavel no futuro será definida delo usuário
                self.wait = random.randint(300, 600)

                construction = self.list_of_construction[0]

                village = construction['village']
                slot_id = construction['slot_id']
                to_level = construction['to_level']

                self.browser.add(task='update_only_slot', args={'village': village, 'slot': slot_id})
                self.browser.await_task('update_only_slot')
                self.database.write(self.travian.villages)

                slot_name = self.travian.villages[village]['slot'][slot_id]['name']
                current_level = self.travian.villages[village]['slot'][slot_id]['level']


                if int(current_level) >= int(to_level):
                    self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> {slot_name} já atingiu o nível solicitado!')
                    del self.list_of_construction[0]

                else:
                    self.browser.add(task='get_upgrade_orders', args={'village': village})
                    self.browser.await_task('get_upgrade_orders')

                    updating = [d for d in self.travian.upgrade_orders[village]['upgrades'] if d['status'] == 'updating']

                    if not updating:
                        self.browser.add(task='upgrade_to_level', args={'village': village, 'slot': slot_id, 'to_level': to_level})
                        self.browser.await_task('upgrade_to_level')

                        slot_in_update = [d for d in self.travian.upgrade_orders[village]['upgrades'] if d['slot'] == slot_id and d['level'] == to_level]

                        if slot_in_update[0]['status'] == 'updating':
                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Construindo {slot_name} para o level {int(current_level) +1}')
                            
                        elif slot_in_update[0]['status'] == 'no resources':
                            
                            self.travian.upgrade_orders[village]['upgrades'] = [d for d in self.travian.upgrade_orders[village]['upgrades'] if d['slot'] != slot_id]

                            self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Sem recursos suficientes para construir, vamos aguardar 10 minutos')
                            self.event.wait(600)

                    else:
                        time_in_update = datetime.timedelta(minutes=int(self.travian.upgrade_orders[village]['time']) / 60 + (self.wait / 60))

                        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Construção na fila, tempo de espera: {time_in_update} minutos')
                        self.event.wait(int(self.travian.upgrade_orders[village]['time'] + self.wait))

                
