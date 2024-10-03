from os import path
from pickle import load, dump
from extra.extra_functions import get_number

db_directory = path.join('dbs')
stock_file = path.join(db_directory, 'stock.pkl')


def get_code():
    code = input('Introduce el codigo del producto: ')
    if code.isdigit():
        return f'#{code}'
    else:
        print('El codigo debe ser un numero')
        return f'#{get_number('Introduce el codigo del producto: ')}'
    

def get_stock():
    if path.exists(stock_file):
        with open(stock_file, 'rb') as f:
            return load(f)
    new_stock = {"alimentos": [], "juguetes": [], "ropa": [], "salud": [], "higiene": [], "accesorios": []}
    with open(stock_file, 'wb') as f:
        dump(new_stock, f)
    return new_stock


def add_stock(stock):
    with open(stock_file, 'wb') as f:
        dump(stock, f)


