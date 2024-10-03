from readchar import readkey
from datetime import datetime
from os import system, path
from pickle import load
from datetime import timedelta

dbs_directory = path.join('dbs')
sales_file_name = path.join(dbs_directory, 'registro_de_ventas.pkl')


def get_sales():
    if path.exists(sales_file_name):
        with open(sales_file_name, 'rb') as file:
            sales = load(file)
        return sales
    else:
        return []


def write_program(year, month, day):
    print('----- ESTADISTICAS DE VENTAS -----')
    print(f'Ventas del dia: {day}/{f'0{month}' if month < 10 else month}/{year}')


def check_date(date: datetime):
    # {'year': date['year'], 'month': date['month'], 'day': date['day']}
    # Dia
    if date.day < 1:
        date = date.replace(day=31)
        date.month -= 1
    elif date.day > 31:
        date = date.replace(day=1)
        date.month += 1
    # Mes
    elif date.month < 1:
        date.month = 12
        date.year -= 1
    elif date.month > 12:
        date.month = 1
        date.year += 1
    return date


def estadisticas_ventas(ventas, date):
    cantidad_total = 0
    total_dia = 0
    for venta in ventas:
        if venta['fecha'].day == date.day and venta['fecha'].month == date.month and venta['fecha'].year == date.year:
            for producto in venta['products']:
                cantidad_total += producto['quantity']
                total_dia += producto['price']

    print("\nEstadísticas de ventas del día:")
    print(f"Total vendido: ${total_dia:.2f}" if total_dia > 0 else "0 pesos generados el dia de hoy")
    print(f"Cantidad total de productos vendidos: {cantidad_total}" if cantidad_total > 0 else "0 productos vendidos el dia de hoy\n")

    print("\nDetalle de ventas:" if total_dia > 0 else "No hay productos a mostrar del dia de hoy")
    for n, venta in enumerate(ventas):
        if venta['fecha'].day == date.day and venta['fecha'].month == date.month and venta['fecha'].year == date.year:
            product_cantidad_total = 0
            print(f"ID de la venta: {n + 1}")
            print(f"Hora: {venta['fecha'].hour}:{venta['fecha'].minute}")
            for product in venta['products']:
                product_cantidad_total += product['quantity']
                print(f"Producto: {product['name']}")
                print(f"Cantidad: {product_cantidad_total}")
                print(f"Precio: ${product['price']:.2f}")
            print(f"Total del carrito: ${venta['final_price']:.2f}\n")


def stats_main():
    system('cls')
    my_key = ''
    date = datetime.now()
    while True:
        print('Presione "D" para avanzar un día, "A" para retroceder un día y "Q" para salir')
        date = check_date(date)
        write_program(date.year, date.month, date.day)
        estadisticas_ventas(get_sales(), date)
        now = datetime.now()
        my_key = readkey()
        if my_key.lower() == "d" and date < now - timedelta(days=1):
            date += timedelta(days=1)
        elif my_key.lower() == "a":
            date -= timedelta(days=1)
        elif my_key.lower() == "q":
            break
        system('cls')


if __name__ == '__main__':
    try:
        stats_main()
    except KeyboardInterrupt:
        pass

