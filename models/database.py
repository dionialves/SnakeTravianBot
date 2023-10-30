import datetime
import os
import ast

from models.log import Log

class Database:
    def __init__(self, travian):
        self.travian = travian
        self.log = Log(travian)
        self.file = f'{self.travian.username}.db'.lower()

    def is_created(self):
         if not os.path.isfile(self.file):
            return False
         return True
    
    def check_data_of_village(self, village):
        if self.is_created():
            data = self.upload_data()
            if data:
                if village in data:
                    return True
            return False
        return False

    def write(self, data):
        with open(self.file, 'w') as file:
            file.write(str(data))
        file.close()

    def upload_data(self):
        if self.is_created:
            with open(self.file, 'r') as file:
                data = file.read()
                
            if data:
                data = ast.literal_eval(data)
                file.close()
                return data
            
        return None



