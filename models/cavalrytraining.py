import time
import random
import datetime
from threading import Thread, Event

from models.log import Log

class CavalryTraining(Thread):

    def __init__(self, travian, browser):
        super().__init__()

        self.training = {}
        self.event = Event()
        self.travian = travian
        self.log = Log(travian)
        self.next_training = None
        self.browser = browser

    def add(self, village, cavalry, number_of_trainings, time):
        self.training = {
            'village': village, 
            'cavalry': cavalry,
            'number_of_trainings': number_of_trainings,
            'time': time
        }

    def ramdow_time(self, wait):
        """
        Essa função randomiza o time de treino, para numca ser o mesmo.
        """
        if int(wait) >= 600:
            new_wait = random.randint(int(wait)-600, int(wait)+600)
            return new_wait
        return wait
    
    def get_new_training(self, wait):
        """
        Aqui formata a saída do proximo treino em horas
        """
        time_now = datetime.datetime.now()
        minutes = datetime.timedelta(minutes=int(wait/60))

        next_training = time_now + minutes

        self.next_training = next_training.strftime("%H:%M:%S")

    def run(self):
        while not self.event.is_set():
            self.event.wait(1)

            if self.training:
                aux = 1
                for cavalry in self.training['cavalry']:
                    if int(self.training['number_of_trainings'][aux-1]) > 0:

                        village = self.training['village']
                        number_of_trainings = self.training['number_of_trainings'][aux-1]
                        
                        self.browser.add(task='cavalry_training', args={'village': village, 'cavalry': cavalry, 'number_of_trainings': number_of_trainings})

                        self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | {self.training["village"]} -> Treinando {self.training["number_of_trainings"][aux-1]} unidades de {cavalry}')
                    aux += 1

                wait = self.ramdow_time(int(self.training['time']))
                self.get_new_training(wait)
                self.event.wait(wait)

if __name__ == "__main__":
    pass

