
# sendwhatmsg_instantly('+529932632957', 'Hola, este es un mensaje de prueba', 8, True, 3)
# '993 263 2957'

def get_number(msj: str):
    try:
        numero = int(input(msj))
        return numero
    except ValueError:
        print('El valor ingresado no es un numero')

numero = get_number('Ingresa el numero de telefono: ')
print(f'+52{numero}')
