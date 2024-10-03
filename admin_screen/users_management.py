from cryptography.fernet import Fernet
from pickle import dump, load
from os import path
from extra.extra_functions import clear_screen, continuar, write_to_txt, read_to_txt
from getpass import getpass

db_directory = path.join('dbs')
register_file_name = path.join(db_directory, 'registro_de_usuarios.txt')
encrypt_file_name = path.join(db_directory, 'encrypt_key.pkl')
users_file_name = path.join(db_directory, 'users.pkl')


def get_encrypt_key():
    if path.exists(encrypt_file_name):
        with open(encrypt_file_name, 'rb') as f:
            return load(f)
    else:
        key = Fernet.generate_key()
        with open(encrypt_file_name, 'wb') as f:
            dump(key, f)
        return key


def encrypt_password(blank_password: str):
    return Fernet(get_encrypt_key()).encrypt(blank_password.encode())


def decrypt_password(encrypted_password: str):
    return Fernet(get_encrypt_key()).decrypt(encrypted_password).decode()



def get_users() -> list:
    if path.exists(users_file_name):
        with open(users_file_name, 'rb') as f:
            try:
                return load(f)
            except EOFError:
                return []
    else:
        return []
    

def load_users(user: dict):
    users = get_users()
    users.append(user)
    with open(users_file_name, 'wb') as f:
        dump(users, f)


def add_user(type = None, random_password: bool = False):
    def get_type(type):
        while True:
            if not type:
                type = input('Tipo de usuario: ').lower()
            if type in ['admin', 'administrador', 'administrator', 'administradores', 'administradores']:
                return 'admin'
            elif type in ['customer', 'vendedor', 'seller', 'vendedores', 'vendedores']:
                return 'customer'
            elif type in ['superadmin', 'superadministrador', 'superadministrators', 'superadministradores', 'superadministradores']:
                return 'superadmin'
            else:
                print('Tipo de usuario no valido!')
                type = None
    user = {'name': input('Nombre del usuario: ').lower(),
             'password': encrypt_password(getpass('Contraseña del usuario: ')),
             'type': get_type(type),
             'status': True}
    load_users(user)
    write_to_txt(register_file_name, f'USUARIO AGREGADO -> {user["name"].capitalize()}:{user["type"]}')
    return user


if __name__ == '__main__':
    print(add_user())
