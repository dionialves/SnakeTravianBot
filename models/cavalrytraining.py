import time
import datetime
from threading import Thread, Event

from models.log import Log

class CavalryTraining(Thread):

    def __init__(self, travian):
        super().__init__()

        self.training = {}
        self.event = Event()
        self.travian = travian
        self.log = Log(travian)

    def add(self, village, cavalry, train_number, time):
        self.training = {
            'village': village, 
            'cavalry': cavalry,
            'train_number': train_number,
            'time': time
        }

    def run(self):
        while not self.event.is_set():
            self.event.wait(1)

            if self.training:

                village = self.training['village']
                cavalry = self.training['cavalry']
                train_number = self.training['train_number']
                time = self.training['time']
                
                self.travian.train_cavalry(village, cavalry, train_number)
                self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {village} -> Treinando {train_number} unidades de {cavalry}')

                self.event.wait(int(time))


if __name__ == "__main__":
    from village import Village

    travian = Village()
    training = CavalryTraining(travian)

    training.daemon = True
    training.start()

    training.add('Debian', 'Theutates Thunder', 2, 60)

    time.sleep(300)

    training.training = {}
    print('Parado')
    time.sleep(300)


