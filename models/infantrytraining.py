import time
import datetime
from threading import Thread, Event

from models.log import Log

class InfatryTraining(Thread):

    def __init__(self, travian):
        super().__init__()

        self.training = {}
        self.event = Event()
        self.travian = travian
        self.log = Log(travian)

    def add(self, village, infantry, train_number, time):
        self.training = {
            'village': village, 
            'infantry': infantry,
            'train_number': train_number,
            'time': time
        }

    def run(self):
        while not self.event.is_set():
            self.event.wait(1)

            if self.training:                
                aux = 1
                for infantry in self.training['infantry']:
                    if int(self.training['train_number'][aux-1]) > 0:
                        #self.travian.train_infantry(self.training['village'], infantry, self.training['train_number'][aux-1])
                        
                        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {self.training["village"]} -> Treinando {self.training["train_number"][aux-1]} unidades de {infantry}')
                    aux += 1

                self.event.wait(int(self.training['time']))


if __name__ == "__main__":
    from village import Village

    travian = Village()
    training = InfatryTraining(travian)

    training.daemon = True
    training.start()

    training.add('Debian', 'Phalanx', 2, 60)

    time.sleep(300)

    training.training = {}
    print('Parado')
    time.sleep(300)


