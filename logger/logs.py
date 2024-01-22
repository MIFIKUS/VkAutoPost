from termcolor import cprint
from colorama import init
from datetime import datetime

init()
class Logs:
    def __init__(self):

        self._log_color = 'grey'
        self._warning_color = 'yellow'
        self._error_color = 'red'
        self._success_color = 'green'

    def log(self, text):
        date = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        log_text = f'[LOG] [{date}] {text}'
        print(log_text)

    def warning(self, text):
        date = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        log_text = f'[WARNING] [{date}] {text}'
        cprint(log_text, self._warning_color)

    def success(self, text):
        date = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        log_text = f'[OK] [{date}] {text}'
        cprint(log_text, self._success_color)

    def error(self, text):
        date = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        log_text = f'[ERROR] [{date}] {text}'
        cprint(log_text, self._error_color)

