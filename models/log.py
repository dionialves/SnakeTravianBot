import os
from watchdog.events import FileSystemEventHandler

class Log(FileSystemEventHandler):
    def __init__(self, travian):
        self.travian = travian
        self.file = f'data/{self.travian.username}-{self.travian.server[8:]}.log'.lower()

    def on_modified(self, event):
        if event.src_path == f'.\{self.file}':
            self.print_on_file()

    def write(self, message):
        if not os.path.exists('data'):
            os.makedirs('data')
    
        with open(self.file , 'a') as file:
            file.write(message + '\n')

    def print_on_file(self):
        with open(self.file , 'r') as file:
            lines = file.readlines()
            lines = lines[-25:]

        os.system('cls')
        print("____________________________________________________________")
        print(f'Logs da conta: {self.travian.username}')
        print('')

        for line in lines:
            print(line, end='')

