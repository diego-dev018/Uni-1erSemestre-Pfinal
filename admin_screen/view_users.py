from os import system, path
from pickle import dump, load
from admin_screen.users_management import *
from extra.extra_functions import get_number
from admin_screen.users_management import add_user

users_path = path.join('dbs', 'users.pkl')


def update_user_status(users: list, user_id: int):
    while True:
        try:
            users[user_id - 1]['status'] = False
            print(f'{users[user_id - 1]["name"].capitalize()} ha sido encontrado y ocultado correctamente!')
            with open(users_file_name, 'wb') as f:
                dump(users, f)
            return 0
        except IndexError:
            print('No existe un usuario con ese ID')
            if input('Deseas intentarlo de nuevo? (S/N): ').lower() == 'n':
                return 0


def print_users(users: list):
    for n, user in enumerate(users):
        if user['status']: 
            print(f'{n + 1}) {user["name"].capitalize()} || {user["type"].capitalize()}')


def delete_user_main(users: list):
    while True:
        clear_screen()
        print('Bienvenido al menu de ocultamiento de usuarios')
        print('Estos son los usuarios registrados:')
        print_users(users)
        user_id = get_number('Introduce el numero del personal a ocultar: ')
        if user_id <= len(users) and user_id > 0:
            if users[user_id - 1]['type'] == 'superadmin':
                print('No puedes ocultar un superadministrador!')
                if input('Deseas intentarlo de nuevo? (S/N): ').lower() == 'n':
                    return 0
            else:
                update_user_status(users, user_id)
                return 0
        else:
            print('Usuario no encontrado!')
            if input('Deseas intentarlo de nuevo? (S/N): ').lower() == 'n':
                return 0
            

def add_user_main(users: list):
    clear_screen()
    print('Bienvenido al menu de manejo de personal!')
    users.append(add_user())
    print(f'Usuario {users[-1]["name"].capitalize()} agregado correctamente!')


def show_users_main(users: list):
    while True:
        clear_screen()
        print('Bienvenido al menu de ocultamiento de usuarios')
        print('Estos son los usuarios registrados y activos:')
        print_users(users)
        options = ['Ocultar usuario', 'Agregar usuario']
        print('\nQue desea hacer?')
        for n, option in enumerate(options):
            print(f'{n + 1}) {option}')
        print('Q) Salir')
        option = input('Introduce la opcion deseada: ').lower()
        if option == '1':
            delete_user_main(users)
            return 0
        elif option == '2':
            users.append(add_user())
            return 0
        elif option == 'q':
            return 0
        else:
            print('Opcion no valida')


if __name__ == "__main__":
    system("cls")
    show_users_main()
