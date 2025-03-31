from HumanovsComputador import jogar_HumanovsComputador
from ComputadorvsComputador import jogar_ComputadorvsComputador
from HumanovsHumano import jogar_HumanovsHumano


def menu():
    print("~~~~~~~~~~~~~~~~~~~~~~")
    print("  Connect Four MENU  ")
    print("~~~~~~~~~~~~~~~~~~~~~~")
    print("1- Human vs Human")
    print("2- Human vs Computer")
    print("3- Computer vs Computer")
    print("0 - Exit\n")

    while True:
        escolha = input("Choose an option: ")

        if escolha == '1':
            jogar_HumanovsHumano()
            break
        elif escolha == '2':
            jogar_HumanovsComputador()
            break
        elif escolha == '3':
            jogar_ComputadorvsComputador()
            break
        elif escolha == '0':
            print("See you later!")
            break
        else:
            print("Invalid input. Try again!")

if __name__ == "__main__":
    menu()
