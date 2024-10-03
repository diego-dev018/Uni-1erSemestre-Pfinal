# Importaciones necesarias
from datetime import datetime
from pickle import load, dump
from getpass import getpass
from os import path, mkdir
from cryptography.fernet import Fernet
from time import sleep
from sys import stdout
# Mis librerias personalizadas
from customer_screens.venta import venta_main
from extra.extra_functions import clear_screen, continuar, write_to_txt, read_to_txt, get_hour
from admin_screen.users_management import *
from admin_screen.admin_page import admin_page_main
from extra.exit_functions import exit_program_main

# Definición de rutas de archivos
db_directory = path.join('dbs')
register_file_name = path.join(db_directory, 'registro_de_usuarios.txt')
encrypt_file_name = path.join(db_directory, 'encrypt_key.pkl')
users_file_name = path.join(db_directory, 'users.pkl')

# Función para la interfaz de vendedores
def customers_screen():
    users = get_users()
    user = {'name': input('Nombre del usuario: ').lower(), 'password': getpass('Contraseña del usuario: ')}
    # Verificación de credenciales
    for i in users:
        if user['name'] == i['name'] and user['password'] == decrypt_password(i['password']):
            if i['type'] != 'customer':
                if not i['status']:
                    print('El usuario esta oculto!')
                    continuar()
                    return 0
                print('PRECAUCION: El tipo del usuario no es de vendedor!')
                continuar()
            break
    else:
        print('Usuario y/o Contraseña invalida!')
        write_to_txt(register_file_name, f'INTENTO DE ENTRADA COMO VENDEDOR '
                                         f'-> {user["name"].capitalize()}')
        continuar()
        return 0
    print('ACCESO CORRECTO... Bienvenido', user['name'].capitalize())
    write_to_txt(register_file_name, f'ENTRADA DE ADMINISTRADOR -> {user["name"].capitalize()}')
    try:
        venta_main()
    except KeyboardInterrupt:
        pass
    continuar(True)

# Función para la interfaz de administradores
def admins_screen():
    users = get_users()
    user = {'name': input('Nombre del usuario: ').lower(), 'password': getpass('Contraseña del usuario: ')}
    # Verificación de credenciales de administrador
    for i in users:
        if user['name'] == i['name'] and user['password'] == decrypt_password(i['password']) and i['type'] in ['admin', 'superadmin']:
            if not i['status']:
                print('Usuario oculto!')
                continuar()
                return 0
            break
    else:
        print('Usuario y/o Contraseña invalida!')
        write_to_txt(register_file_name, f'INTENTO DE ENTRADA COMO ADMINISTRADOR '
                                         f'-> {user["name"].capitalize()}')
        continuar()
        return 0
    print('ACCESO CORRECTO... Bienvenido', user['name'].capitalize())
    write_to_txt(register_file_name, f'ENTRADA DE ADMINISTRADOR -> {user["name"].capitalize()}')
    try:
        admin_page_main()
    except KeyboardInterrupt:
        pass
    continuar(True)

# Función principal del programa
def main():
    options = ['Interfaz de Vendedor', 'Interfaz de Administrador']
    company_name = 'La Perruneria'
    # Crear directorio de base de datos si no existe
    if not path.exists(db_directory):
        mkdir(db_directory)
    while True:
        clear_screen()
        # Mostrar mensaje de bienvenida y opciones
        print(f"""\
BIENVENIDO A TU PROGRAMA DE ADMINISTRACION DE VENTA,
CON ESTE PROGRAMA PODRAS ADMINISTRAR TU INVENTARIO (VENDER,
AGREGAR Y ELIMINAR), ADMINISTRAR VENDEDORES Y ADMINISTRADORES,
ENTRE MAS COSAS...

EMPRESA: {company_name}
HORA DE INICIO: {get_hour()}

{'*' * 15} OPCIONES {'*' * 15}\
""")
        users = get_users()
        # Si no hay usuarios, agregar el primer administrador
        if not users:
            print("NO HAY ADMINISTRADORES!\nPORFAVOR, AGREGA EL PRIMER ADMINISTRADOR\n")
            add_user(type='superadmin')
            continue
        # Mostrar opciones
        for i, option in enumerate(options):
            print(f'{i+1}) {option}')
        user_opt = input('OPCION: ')
        # Manejar la opción seleccionada
        if user_opt == '1':
            customers_screen()
        elif user_opt == '2':
            admins_screen()

# Punto de entrada del programa
if __name__ == '__main__':
    user_exit = False
    users = get_users()
    while not user_exit:
        try:
            main()
        except KeyboardInterrupt:
            clear_screen()
            if not users:
                break
            try:
                users = get_users()
                print(f'{"-" * 15} INTERFAZ DE SALIDA {"-" * 15}')
                user = {'name': input('Nombre del usuario: ').lower(), 'password': getpass('Contraseña del usuario: ')}
                for i in users:
                    if user['name'] == i['name'] and user['password'] == decrypt_password(i['password']) and i['type'] in ['admin', 'superadmin']:
                        user_exit = True
                        exit_program_main()
                        break
                else:
                    print('El usuario no es un administrador')
                    continuar()
                    continue
            except KeyboardInterrupt:
                clear_screen()
                continue
