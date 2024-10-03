from os import path
from extra.extra_functions import clear_screen, get_number, continuar
from admin_screen.stock_extra_functions import get_stock, add_stock, get_code


db_directory = path.join('dbs')
stock_file = path.join(db_directory, 'stock.pkl')


def print_options(options):
    for i, opt in enumerate(options):
        print(f'{i+1}) {opt.capitalize()}')


def buscar_producto(cat, identificador, stock):
    for producto in stock[cat]:
        if identificador.lower() in producto['name'].lower() or producto['code'] == identificador or producto['code'] == f'#{identificador}':
            return producto
    return None


def gestionar_categoria(cat, stock):
    options = [
        'Ocultar producto', 'Agregar producto', 'Mostrar todos los productos', 
        'Cambiar precio de producto', 'Eliminar cantidad de producto', 
        'Mostrar productos ocultos', 'Desocultar producto', 'Eliminar producto'
    ]
    while True:
        clear_screen()
        print(f'\n----- Menú de {cat} -----')
        print_options(options)
        print('Q) Salir de la categoria')
        user_opt = input('Elige una opción: ')
        
        if user_opt == '1':
            stock = ocultar_producto(cat, stock)
        elif user_opt == '2':
            stock = agregar_producto(cat, stock)
        elif user_opt == '3':
            mostrar_productos(cat, stock)
        elif user_opt == '4':
            stock = cambiar_precio_producto(cat, stock)
        elif user_opt == '5':
            stock = eliminar_cantidad_producto(cat, stock)
        elif user_opt == '6':
            mostrar_productos(cat, stock, ocultos=True)
        elif user_opt == '7':
            stock = desocultar_producto(cat, stock)
        elif user_opt == '8':
            stock = eliminar_producto(cat, stock)
        elif user_opt.lower() == 'q':
            print(f'Saliendo de la categoría {cat}...')
            return 0
        else:
            print('Opción no válida, intenta de nuevo.')
        continuar(line_scape=True)
        add_stock(stock)


def agregar_producto(cat, stock):
    product_name = input('Introduce el nombre del producto: ').lower()
    product_quantity = get_number('Introduce la cantidad a añadir: ')

    producto = buscar_producto(cat, product_name, stock)
    if producto and producto != '':
        producto['quantity'] += product_quantity
        print(f'Se han añadido {product_quantity} a \'{product_name}\'. Nueva cantidad: {producto["quantity"]}')
        return stock


    product_price = get_number('Introduce el precio del producto: ')
    product_code = get_code()
    nuevo_producto = {
        'name': product_name,
        'code': product_code,
        'quantity': product_quantity,
        'price': product_price,
        'active': product_quantity > 0
    }
    stock[cat].append(nuevo_producto)
    print(f'Producto \'{product_name}\' agregado exitosamente!')
    return stock


def ocultar_producto(cat, stock):
    product_name = input('Introduce el nombre o codigo del producto a ocultar: ')
    producto = buscar_producto(cat, product_name, stock)
    if producto:
        producto['active'] = False
        print(f'El producto \'{producto["name"]}\' ha sido ocultado')
    else:
        print(f'El producto \'{product_name}\' no existe en la categoría {cat}')
    return stock


def desocultar_producto(cat, stock):
    product_name = input('Introduce el nombre o codigo del producto a desocultar: ')
    producto = buscar_producto(cat, product_name, stock)
    if producto:
        producto['active'] = True
        print(f'El producto \'{producto["name"]}\' ha sido desocultado')
    else:
        print(f'El producto \'{product_name}\' no existe en la categoría {cat}')
    return stock


def eliminar_producto(cat, stock):
    product_name = input('Introduce el nombre o codigo del producto a eliminar: ')
    producto = buscar_producto(cat, product_name, stock)
    if producto:
        stock[cat].remove(producto)
        print(f'Producto \'{producto["name"]}\' eliminado del inventario.')
    else:
        print(f'El producto \'{product_name}\' no existe en la categoría {cat}.')
    return stock


def eliminar_cantidad_producto(cat, stock):
    product_name = input('Introduce el nombre o codigo del producto del que deseas eliminar cantidad: ')
    producto = buscar_producto(cat, product_name, stock)
    if producto:
        cantidad_eliminar = get_number(f'Introduce la cantidad a eliminar de \'{producto["name"]}\': ')
        if producto["quantity"] >= cantidad_eliminar:
            producto["quantity"] -= cantidad_eliminar
            print(f'Se han eliminado {cantidad_eliminar} unidades de \'{producto["name"]}\'. Cantidad restante: {producto["quantity"]}')
        else:
            print(f'No puedes eliminar más de lo que hay en inventario. Cantidad actual: {producto["quantity"]}')
    else:
        print(f'El producto \'{product_name}\' no existe en la categoría {cat}.')
    return stock


def cambiar_precio_producto(cat, stock):
    product_name = input('Introduce el nombre o codigo del producto al que deseas cambiar el precio: ')
    producto = buscar_producto(cat, product_name, stock)
    if producto:
        nuevo_precio = get_number(f'Introduce el nuevo precio para \'{producto["name"]}\': ')
        producto['price'] = nuevo_precio
        print(f'El precio de \'{producto["name"]}\' ha sido actualizado a {nuevo_precio:.2f}.')
    else:
        print(f'El producto \'{product_name}\' no existe en la categoría {cat}.')
    return stock


def mostrar_productos(cat, stock, ocultos=False):
    dist = ((90 - len('Productos en ' + cat.capitalize())) - 2) // 2
    print(f'\n{"-" * dist} Productos en {cat.capitalize()} {"-" * dist}')
    print(f'{"Nombre":<30} {"Código":<15} {"Cantidad":<15} {"Precio":<15} {"Estado":<15}')
    print('-' * 90)
    for producto in stock[cat]:
        if producto['active'] and not ocultos:
            nombre = producto['name'][:30].ljust(30)
            codigo = producto['code'][:15].ljust(15)
            cantidad = str(producto['quantity']).ljust(15)
            precio = f"{producto['price']:.2f}".ljust(15)
            print(f"{nombre} {codigo} {cantidad} {precio} {'Activo' if producto['active'] else 'Oculto'}")
        elif ocultos:
            nombre = producto['name'][:30].ljust(30)
            codigo = producto['code'][:15].ljust(15)
            cantidad = str(producto['quantity']).ljust(15)
            precio = f"{producto['price']:.2f}".ljust(15)
            print(f"{nombre} {codigo} {cantidad} {precio} {'Activo' if producto['active'] else 'Oculto'}")


def mostrar_productos_ocultos(cat, stock):
    print(f'\n----- Productos ocultos en {cat} -----')
    for producto in stock[cat]:
        if not producto['active']:
            print(f"{producto['name'][:20]} {producto['code'][:10]} {producto['quantity']} {producto['price']}")


def manejo_de_stock_main():
    while True:
        clear_screen()
        stock = get_stock()
        print('----- Menú de Categorías -----')
        print_options(list(stock.keys()))
        print('Q) Salir del stock')
        cat_option = input('Elige una categoría (1-6) o Q para salir: ')
        if cat_option.lower() == 'q':
            print('Saliendo del stock...')
            return 0
        elif cat_option in ['1', '2', '3', '4', '5', '6']:
            cat = list(stock.keys())[int(cat_option)-1]
            gestionar_categoria(cat, stock)
        else:
            print('Opción no válida, intenta de nuevo.')

if __name__ == "__main__":
    try:
        manejo_de_stock_main()
    except KeyboardInterrupt:
        pass
