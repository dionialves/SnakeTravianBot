import os


from models.log import Log

class Account:
    def __init__(self):
        self.file = os.path.join(os.getcwd(), 'data', 'account.db') 

    def is_created(self):
        if not os.path.isfile(self.file):
            return False
        return True

    def write(self, data):
        if not os.path.exists('data'):
            os.makedirs('data')

        with open(self.file, 'a') as file:
            file.write(str(data) + '\n')
        file.close()

    def upload_data(self):
        if self.is_created:
            with open(self.file, 'r') as file:
                data = file.readlines()
                return data
  
        return None



