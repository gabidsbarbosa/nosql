from usuario import menu_usuario
from vendedor import menu_vendedor

def menu():
    while True:
        print("\033[1mMenu Principal:\033[0m")
        print("1 - Menu Usuário")
        print("2 - Menu Vendedor")
        print("0 - Sair")
        
        key = input("Digite a opção desejada: ")

        if key == '0':
            break

        if key == '1':
            menu_usuario()
        elif key == '2':
            menu_vendedor()

if __name__ == "__main__":
    menu()
