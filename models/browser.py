from threading import Thread, Event


class Browser(Thread):
    def __init__(self, travian):
        super().__init__()

        self.event = Event()
        self.travian = travian
        self.tasks = []

    def update_slots(self, village) -> bool:
        self.travian.update_all_fields_village(village)

        return True

    def auto_send_farmlist(self, village) -> bool:
        self.travian.start_all_farm_list()

        return True
    
    def construction(self, village, slot) -> bool:
        self.travian.upgrade_fields_resource(village, slot)

        return True

    def cavalry_training(self, village, cavalry, number_of_trainings) -> bool:
        self.travian.cavalry_training(village, cavalry, number_of_trainings)

        return True

    def infantry_training(self, village, cavalry, number_of_trainings) -> bool:
        self.travian.infantry_training(village, cavalry, number_of_trainings)

        return True

    def add(self, task, args={}):
        match task:
            case 'update_slots':
                self.tasks.append([task, {'village': args['village']}])

            case 'auto_send_farmlist':
                self.tasks.append([task, {'village': args['village']}])

            case 'construction':
                self.tasks.append([task, {'village': args['village'], 'slot': args['slot']}])

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
                    case 'update_slots':
                        no_errors = self.update_slots(task[1]['village'])

                    case 'auto_send_farmlist':
                        no_errors = self.auto_send_farmlist(task[1]['village'])

                    case 'construction':
                        no_errors = self.construction(task[1]['village'], task[1]['slot'])

                    case 'cavalry_training':
                        no_errors = self.cavalry_training(task[1]['village'], task[1]['cavalry'], task[1]['number_of_trainings'])

                    case 'infantry_training':
                        no_errors = self.infantry_training(task[1]['village'], task[1]['infantry'], task[1]['number_of_trainings'])

                if no_errors:
                    del self.tasks[0]
                    attempts = 1

                elif attempts > 2:
                    del self.tasks[0]
                    attempts = 1

                else:
                    attempts =+ 1




                