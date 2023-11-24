from threading import Thread, Event


class Browser(Thread):
    def __init__(self, travian):
        super().__init__()

        self.event = Event()
        self.travian = travian
        self.tasks = []

    def login(self, server, username, password):
        self.travian.login(server, username, password)

        return True

    def get_farmlist(self):
        self.travian.get_farmlist()

        return True

    def get_upgrade_orders(self, village):
        self.travian.get_upgrade_orders(village)

        return True
    
    def get_troops_infantary(self, village):
        self.travian.get_troops_infantary(village)

        return True

    def get_troops_cavalry(self, village):
        self.travian.get_troops_cavalry(village)

        return True
    
    def update_initial_information(self):
        self.travian.update_initial_information()

        return True

    def update_all(self) -> bool:
        self.travian.update_all()

        return True
    
    def update_only_slots(self) -> bool:
        self.travian.update_only_slots()

        return True

    def update_only_slot(self, village, slot):
        self.travian.update_only_slot(village, slot)
        
        return True

    def auto_send_farmlist(self) -> bool:
        self.travian.auto_send_farmlist()

        return True
    
    def upgrade_to_level(self, village, slot, to_level) -> bool:
        self.travian.upgrade_to_level(village, slot, to_level)

        return True

    def cavalry_training(self, village, cavalry, number_of_trainings) -> bool:
        self.travian.cavalry_training(village, cavalry, number_of_trainings)

        return True

    def infantry_training(self, village, infantry, number_of_trainings) -> bool:
        self.travian.infantry_training(village, infantry, number_of_trainings)

        return True

    def qualquercoisa(self):
        """
        Erros a serem tratados:

        selenium.common.exceptions.NoSuchWindowException
        -> quando s janela não esta mais ativa

        selenium.common.exceptions.NoSuchElementException
        -> quando o selenium não encontra algum elemento

        Erro por não estar logado


        
        """
        pass

    def await_task(self, task):
        while True:
            self.event.wait(1)
            is_task = False

            for t in self.tasks:
                if task in t[0]:
                    is_task = True

            if not is_task:
                break

    def add(self, task=None, args={}):
        match task:
            case 'login':
                self.tasks.append([task, {'server': args['server'], 'username': args['username'], 'password': args['password']}])

            case 'get_farmlist':
                self.tasks.append([task])

            case 'get_upgrade_orders':
                self.tasks.append([task, {'village': args['village']}])

            case 'get_troops_infantary':
                self.tasks.append([task, {'village': args['village']}])

            case 'get_troops_cavalry':
                self.tasks.append([task, {'village': args['village']}])

            case 'update_initial_information':
                self.tasks.append([task])

            case 'update_all':
                self.tasks.append([task])

            case 'update_only_slots':
                self.tasks.append([task])

            case 'update_only_slot':
                self.tasks.append([task, {'village': args['village'], 'slot': args['slot']}])

            case 'auto_send_farmlist':
                self.tasks.append([task])

            case 'upgrade_to_level':
                self.tasks.append([task, {'village': args['village'], 'slot': args['slot'], 'to_level': args['to_level']}])

            case 'cavalry_training':
                self.tasks.append([task, {
                    'village': args['village'], 
                    'cavalry': args['cavalry'], 
                    'number_of_trainings': args['number_of_trainings']
                }])
        
            case 'infantry_training':
                self.tasks.append([task, {
                    'village': args['village'], 
                    'infantry': args['infantry'], 
                    'number_of_trainings': args['number_of_trainings']
                }])

    def run(self):
        attempts = 1

        while not self.event.is_set():
            self.event.wait(1)
            

            if self.tasks:
                task = self.tasks[0]
            
                match task[0]:
                    case 'login':
                        no_errors = self.login(task[1]['server'], task[1]['username'], task[1]['password'])

                    case 'get_farmlist':
                        no_errors = self.get_farmlist()

                    case 'get_upgrade_orders':
                        no_errors = self.get_upgrade_orders(task[1]['village'])

                    case 'get_troops_infantary':
                        no_errors = self.get_troops_infantary(task[1]['village'])

                    case 'get_troops_cavalry':
                        no_errors = self.get_troops_cavalry(task[1]['village'])

                    case 'update_initial_information':
                        no_errors = self.update_initial_information()

                    case 'update_all':
                        no_errors = self.update_all()

                    case 'update_only_slots':
                        no_errors = self.update_only_slots()

                    case 'update_only_slot':
                        no_errors = self.update_only_slot(task[1]['village'], task[1]['slot'])

                    case 'auto_send_farmlist':
                        no_errors = self.auto_send_farmlist()

                    case 'upgrade_to_level':
                        no_errors = self.upgrade_to_level(task[1]['village'], task[1]['slot'], task[1]['to_level'])

                    case 'infantry_training':
                        no_errors = self.infantry_training(task[1]['village'], task[1]['infantry'], task[1]['number_of_trainings'])

                    case 'cavalry_training':
                        no_errors = self.cavalry_training(task[1]['village'], task[1]['cavalry'], task[1]['number_of_trainings'])

                    case _:
                        del self.tasks[0]

                if no_errors:
                    del self.tasks[0]
                    attempts = 1

                elif attempts > 2:
                    del self.tasks[0]
                    attempts = 1

                else:
                    attempts =+ 1




                