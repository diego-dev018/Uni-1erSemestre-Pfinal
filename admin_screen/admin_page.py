from extra.extra_functions import clear_screen, get_number
from admin_screen.estadisticas_de_venta import stats_main
from admin_screen.view_users import show_users_main
from admin_screen.manejo_de_stock import manejo_de_stock_main
from admin_screen.users_management import get_users


def admin_page_main():
    while True:
        clear_screen()
        options = ['Administrar inventario', 'Administrar personal', 'Reportes y estadisticas']
        print('Bienvenido al menu de administracion!')
        print('Aqui puedes administrar tu inventario, personal y mas!')
        print('Que desea hacer?')
        print(f'{"-" * 15} OPCIONES {"-" * 15}')
        for n, option in enumerate(options):
            print(f'{n + 1}) {option}')
        print('Q) Salir')
        option = input('Introduce la opcion deseada: ').lower()
        if option == '1':
            manejo_de_stock_main()
        elif option == '2':
            show_users_main(get_users())
        elif option == '3':
            stats_main()
        elif option == 'q':
            break


if __name__ == '__main__':
    admin_page_main()
