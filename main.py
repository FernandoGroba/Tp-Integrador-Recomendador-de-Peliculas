from services.catalogo import Catalogo
from UI.terminal import Terminal


def main()->None:

    catalogo = Catalogo()
    catalogo.cargar_json('data/data.json')
    print(f'Se cargaron {len(catalogo)} elementos.')
    menu = Terminal(catalogo)
    menu.iniciar()

if __name__ == '__main__':
    main()