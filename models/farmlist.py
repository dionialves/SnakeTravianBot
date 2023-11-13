from random import randint
import datetime
from threading import Thread, Event

from models.log import Log
from models.browser import Browser


class Farmlist(Thread):
    """
    Esta variavel precisa ser preenchida com a seguinte ordem:
    [
        {
            'start_of_interval': 20,
            'end_of_interval': 40
        }
    ]
    slot_id = Slot a ser construido
    to_level = level a ser atualizado

    """
    def __init__(self, travian, browser):
        super().__init__()

        self.order_auto_send_farmlist = {}
        self.event = Event()
        self.log = Log(travian)
        self.browser = browser

    def add(self, start_of_interval, end_of_interval):
        self.order_auto_send_farmlist = {
            'start_of_interval': start_of_interval,
            'end_of_interval': end_of_interval
        }

    def run(self):
        while not self.event.is_set():
            self.event.wait(1)

            if self.order_auto_send_farmlist:

                self.browser.add('auto_send_farmlist')
                #self.travian.start_all_farm_list()

                interval_in_minutes = randint(
                    int(self.order_auto_send_farmlist['start_of_interval']), 
                    int(self.order_auto_send_farmlist['end_of_interval'])
                )
                
                nextStart = datetime.datetime.now() + datetime.timedelta(minutes=interval_in_minutes)
                nextStart = nextStart.strftime("%H:%M:%S")

                self.log.write(f'{datetime.datetime.now().strftime("%H:%M:%S")} | Iniciando FarmList, o proximo esta programado para as {nextStart}')
                self.event.wait(interval_in_minutes*60)