import os
import sys
from watchdog.events import FileSystemEventHandler

class Log(FileSystemEventHandler):
    def __init__(self, travian):
        self.travian = travian

        file_name = f'{self.travian.username}-{self.travian.server[8:]}.log'.lower()
        self.file = os.path.join(os.getcwd(), 'data', file_name) 

        
    def on_modified(self, event):
        if event.src_path == f'{self.file}':
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

        if sys.platform.startswith('linux'):
            os.system('clear')
        elif sys.platform.startswith('win'):
            os.system('cls')

        print("____________________________________________________________")
        print(f'Logs da conta: {self.travian.username}')
        print('')

        for line in lines:
            print(line, end='')

