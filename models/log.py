import os
from watchdog.events import FileSystemEventHandler

class Log(FileSystemEventHandler):
    def __init__(self, village):
        self.village = village
        self.file = f'{self.village.username}.logs'

    def on_modified(self, event):
        if event.src_path == f'.\{self.file}':
            self.print_on_file()

    def write(self, message):
        with open(self.file , 'a') as file:
            file.write(message + '\n')

    def print_on_file(self):
        with open(self.file , 'r') as file:
            lines = file.readlines()
            lines = lines[-15:]

        os.system('cls')
        print("____________________________________________________________")
        print(f'Logs da conta: {self.village.username}')
        print('')

        for line in lines:
            print(line, end='')

