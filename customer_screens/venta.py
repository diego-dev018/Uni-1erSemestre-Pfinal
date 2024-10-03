from os import path
from pickle import dump, load
from admin_screen.stock_extra_functions import get_stock, add_stock, get_code
from datetime import datetime
from extra.extra_functions import get_number, continuar, clear_screen, write_to_txt, read_to_txt
from customer_screens.ticket import ticket_main

# {'name': product_name, 'code': product_code, 'quantity': product_quantity, 'price': product_price}
# {'alimentos': [{'name': 'manzana', 'code': 'dpada', 'quantity': 20, 'price': 100, 'active': True}, {'name': 'Sandia', 'code': 'dijawda', 'quantity': 10, 'price': 100, 'active': True}], 'juguetes': [], 'ropa': [], 'salud': [], 'higiene': [], 'accesorios': []}

db_directory = path.join('dbs')
stock_file = path.join(db_directory, 'stock.pkl')
register_file_name = path.join(db_directory, 'registro_de_ventas.txt')
register_pickle_file_name = path.join(db_directory, 'registro_de_ventas.pkl')


def write_to_pickle(file_name, data):
    if path.exists(file_name):
        with open(file_name, 'rb') as file:
            sales = load(file)
        sales.append(data)
    else:
        sales = [data]
    with open(file_name, 'wb') as file:
        dump(sales, file)


def check_product(product, stock):
    product_on_stock = None
    for item in stock.keys():
        for sub_item in stock[item]:
            if sub_item['name'] == product['name'] or sub_item['code'] == f'#{product['name']}' or sub_item['code'] == product['name']:
                product_on_stock = sub_item
                break
    if product_on_stock:
        if product_on_stock['quantity'] >= product['quantity']:
            product_on_stock['quantity'] -= product['quantity']
            return product_on_stock
        else:
            print(f"No hay suficiente stock del producto \'{product_on_stock['name']}\' || Stock disponible: {product_on_stock['quantity']}")
            return None
    else:
        print(f"No se encuentra el producto {product['name']} en el stock")
        return None


def venta_main():
    now = datetime.now()
    stock = get_stock()
    while True:
        clear_screen()
        print(f"""\
----- INTERFAZ DE VENTA -----
HORA DE ACCESO: {now.hour}:{now.minute}
INGRESA 'Q' EN NOMBRE DEL PRODUCTO PARA FINALIZAR COMPRA
PRESIONA 'CTRL + C' PARA SALIR DE LA INTERFAZ DE VENTA!
""")
        total = 0
        products = []
        while True:
            product = {'name': input('Ingrese el nombre del producto: ').lower()}.copy()
            if product['name'].lower() == 'q':
                break
            product['quantity'] = get_number('Cantidad del producto [Default 1]: ')
            product_on_stock = check_product(product, stock)
            if product_on_stock:
                product['name'] = product_on_stock['name']
                for item in products:
                    if item['name'] == product['name']:
                        item['quantity'] += product['quantity']
                        break
                else:
                    products.append(product)
                total += product_on_stock['price'] * product['quantity']
                product['price'] = product_on_stock['price'] * product['quantity']
                print(f"Producto agregado: {product_on_stock['name']} || Cantidad: {product['quantity']} || Precio unitario: {product['price']}")
        print('¡CARRITO DE COMPRA!')
        if len(products) > 0:
            for i, product in enumerate(products):
                print(f"+ {product['name'].capitalize()} || CANTIDAD: {product['quantity']} || PRECIO UNITARIO: {product['price']} || PRECIO TOTAL: {product['price'] * product['quantity']}")
            print(f'TOTAL: {total}')
            if input('ESCRIBE \'CONFIRMAR\' PARA CONFIRMAR LA VENTA: ').lower() == 'confirmar':
                add_stock(stock)
                write_to_txt(register_file_name, f'VENTA REALIZADA -> {[[[f"Nombre: {product["name"].capitalize()}, Cantidad: {product["quantity"]}, Precio: {product["price"]}"], f"Total: {total}"] for product in products]}')
                write_to_pickle(register_pickle_file_name, {'fecha': datetime.now(), 'products': products, 'final_price': total})
                ticket_main({'fecha': datetime.now(), 'products': products, 'final_price': total})
            else:
                eliminate_product = False
                while not eliminate_product:
                    if input('DESEAS ELIMINAR ALGUN PRODUCTO DEL CARRITO? ').lower() in ['si', 's', 'yes', 'y']:
                        print('PRODUCTOS EN EL CARRITO')
                        for i, product in enumerate(products):
                            print(f"+ {product['name']} || CANTIDAD: {product['quantity']} || Codigo: {product['code']}")
                        product_to_delete = input('INGRESA EL NOMBRE DEL PRODUCTO QUE DESEAS ELIMINAR: ').lower()
                        for product in products:
                            if product['name'] == product_to_delete or product['code'] == product_to_delete:
                                to_del = get_number(f'Cuantas \'{product["name"]}\' deseas eliminar? ')
                                product['quantity'] -= to_del
                                product_on_stock = check_product(product, stock)
                                product_on_stock['quantity'] += to_del
                                print(f'Nuevo stock general de {product_on_stock["name"]}: {product_on_stock["quantity"]} y stock en el carrito: {product["quantity"]}')
                                add_stock(stock)
                                print(f'PRODUCTO ELIMINADO: {product_to_delete}')
                                eliminate_product = True
                                break
                        else:
                            print('NO SE ENCONTRO EL PRODUCTO!')
                            if input('DESEAS INTENTAR CON OTRO PRODUCTO? ').lower() in ['si', 's', 'yes', 'y']:
                                continue
                            else:
                                break
                    else:
                        if input('Deseas cancelar la venta? ').lower() in ['si', 's', 'yes', 'y']:
                                print('VENTA CANCELADA!')
                                break
        else:
            print('No hay productos en el carrito!')
        continuar()
    # venta = {'fecha': datetime.now(), 'products': [{'name': '', 'cantidad': 0, 'price': 0}], 'final_price': 0}


if __name__ == '__main__':
    venta_main()
    # check_product({'name': 'manzana', 'quantity': 10}, {'alimentos': [{'name': 'manzana', 'code': 'dpada', 'quantity': 20, 'price': 100, 'active': True}, {'name': 'Sandia', 'code': 'dijawda', 'quantity': 10, 'price': 100, 'active': True}], 'juguetes': [], 'ropa': [], 'salud': [], 'higiene': [], 'accesorios': []})
