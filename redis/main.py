from usuario import menu_usuario
from vendedor import menu_vendedor
from produto import menu_produto
from compras import menu_compras
from favoritos import menu_favoritos

if __name__ == "__main__":
    while True:
        print("\033[1mMenu Principal:\033[0m")
        print("1 - Menu Usuário")
        print("2 - Menu Vendedor")
        print("3 - Menu Produto")
        print("4 - Menu Compras")
        print("5 - Menu Favoritos")
        print("0 - Sair")
        
        key = input("Digite a opção desejada: ")

        if key == '0':
            break

        if key == '1':
            menu_usuario()

        elif key == '2':
            menu_vendedor()

        elif key == '3':
            menu_produto()

        elif key == '4':
            menu_compras()

        elif key == '5':
            menu_favoritos()

if __name__ == "__main__":
    menu_usuario()