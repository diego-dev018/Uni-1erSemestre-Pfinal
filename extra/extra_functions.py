from os import system
from platform import platform
from datetime import datetime


def clear_screen():
    system('cls' if 'windows' in platform().lower() else 'clear')


def get_number(ask: str):
    while True:
        num = input(ask)
        try:
            try:
                return 1 if not num else int(num)
            except ValueError:
                return 1 if not num else float(num)
        except ValueError:
            print('NUMERO INVALIDO! NO ES UN NUMERO :(')


def get_hour():
    now = datetime.now()
    return (f'{'12' if now.hour % 12 == 0 else now.hour % 12}:'
          f'{now.minute if now.minute >= 10 else '0' + str(now.minute)} '
          f'{'PM' if now.hour >= 12 else 'AM'}')


def continuar(line_scape: bool = False):
    if not line_scape:
        input('Presiona enter para continuar... ')
    else:
        input('\nPresiona enter para continuar... ')


def read_to_txt(file_name: str):
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return 'FIN DEL REGISTRO!'


def write_to_txt(file_name: str, text_to_write: str):
    file = read_to_txt(file_name)
    with open(file_name, 'w') as f:
        f.write(f'{datetime.now()} | {text_to_write}\n{file}')
    f.close()


if __name__ == '__main__':
    print(get_number('Numero: '))
