from datetime import datetime
from extra.extra_functions import get_number, write_to_txt, continuar
from os import path, mkdir
from pywhatkit import sendwhatmsg_instantly

# venta = {'fecha': datetime.now(), 'products': [{'name': '', 'cantidad': 0, 'price': 0}], 'final_price': 0}
db_directory = 'dbs'
tickets_path = path.join(db_directory, 'tickets')


def get_phone_number():
    while True:
        numero = input('Ingresa el numero de telefono: ')
        if numero.isdigit():
            return f'+52{numero}'
        elif numero.index(' ') != -1:
            numero = numero.replace(' ', '')
            return f'+52{numero}'
        else:
            print('El valor ingresado no es un numero\nEjemplo: 993 263 2957 -> 9932632957')


def get_ticket(venta: dict, pago_con_tarjeta: bool = False, envio_ticket: bool = False):
    ticket = []

    pago = 0

    cabezera = f"""
{'*' * 13} TICKET DE VENTA {'*' * 13}
*{' ' * 12}  LA PERRUNERIA  {' ' * 12}*
  FECHA: {venta['fecha']}
"""
    ticket.extend(cabezera.split('\n'))
    body = f"""\
*{' ' * 12}    PRODUCTOS    {' ' * 12}*\
"""
    ticket.extend(body.split('\n'))

    for product in venta['products']:
        ticket.append(f"{product['name'].capitalize()} || CANTIDAD: {product['quantity']} || PRECIO: {product['price']}")
    else:
        ticket.append('\n')

    if not pago_con_tarjeta:
        while True:
            print(f'Total: {venta["final_price"]}')
            pago = get_number('Ingrese el pago: ')
            if pago < venta['final_price']:
                print('El pago es menor al precio total')
            else:
                break
    else:
        pago = venta['final_price']

    legs = f"""\
* TOTAL: {venta['final_price']}
* PAGO: {pago if not pago_con_tarjeta else 'Pago con tarjeta!'}
* CAMBIO: {pago - venta['final_price']}
"""
    ticket.extend(legs.split('\n'))

    if not path.exists(tickets_path):
        mkdir(tickets_path)
    date_to_write = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    write_to_txt(path.join(tickets_path, f'{date_to_write}.txt'), '\n'.join(ticket))

    if envio_ticket:
        sendwhatmsg_instantly(get_phone_number(), f"{'\n'.join(ticket)}", 15, True, 3)
        # Ejemplo: sendwhatmsg_instantly('+529932235769', 'Hola, este es un mensaje de prueba', 8, True, 3)

    return '\n'.join(ticket)


def ticket_main(venta):
    pago_con_tarjeta = input('Pago con tarjeta? (s/n): ')
    envio_ticket = input('Enviar ticket por WhatsApp? (s/n): ')
    print(get_ticket(venta, pago_con_tarjeta == 's', envio_ticket == 's'))


if __name__ == '__main__':
    ticket_main({'fecha': datetime.now(), 'products': [{'name': 'manzana', 'quantity': 10, 'price': 100}], 'final_price': 0})
