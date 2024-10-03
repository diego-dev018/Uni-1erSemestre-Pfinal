from extra.extra_functions import clear_screen, get_hour
from time import sleep
from sys import exit


def imprimir_mensaje_grande():
    mensaje = """
     GGGGGGGG  RRRRRRRR     AAAAA     CCCCCCCC  IIIIIIII     AAAAA     SSSSSSSS 
    GG      GG RR      RR  AA   AA   CC      CC    II       AA   AA   SS       
    GG         RR      RR AA     AA  CC            II      AA     AA  SS       
    GG         RRRRRRRR   AAAAAAAAA  CC            II      AAAAAAAAA   SSSSSSS 
    GG   GGGG  RR    RR   AA     AA  CC            II      AA     AA         SS
    GG      GG RR     RR  AA     AA  CC      CC    II      AA     AA         SS
     GGGGGGGG  RR      RR AA     AA   CCCCCCCC  IIIIIIII   AA     AA  SSSSSSSS 
"""
    return mensaje


def imprimir_team():
    mensaje = """\
Team:
- Diego ----> Programacion
- Monica ---> Documentacion
- Andres ---> Testing y documentacion
- Aranza ---> Testing, investigacion y presentacion
- Ixchel ---> Testing
"""
    return mensaje



def exit_program_main():
    try:
        print(f'Hora de salida: {get_hour()}')
        write_time = 0.05
        mensaje = 'Saliendo...'
        sleep(0.20)
        for letra in mensaje:
            print(letra, end='', flush=True)
            sleep(write_time)
        print()
        mensaje = 'Gracias por usar nuestro programa!'
        sleep(0.3)
        for letra in mensaje:
            print(letra, end='', flush=True)
            sleep(write_time)
        print()
        sleep(0.3)
        for letra in imprimir_mensaje_grande():
            print(letra, end='', flush=True)
            sleep(0.02)
        print()
        for letra in imprimir_team():
            print(letra, end='', flush=True)
            sleep(write_time)
        print()
        exit()
    except KeyboardInterrupt:
        clear_screen()

