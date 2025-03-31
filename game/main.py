from board import criar_tabuleiro, imprimir_tabuleiro, jogada_valida, linha_piece, drop_piece
from game_logic import piece_ganhou

def main():
    while True:
        try:
            num_rows = 6 #int(input("Enter number of rows: "))
            num_cols = 7 #int(input("Enter number of columns: "))
            if num_rows >= 4 and num_cols >= 4:  # Minimum size for Connect Four
                break
            else:
                print("Rows and columns must be at least 4.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    tabuleiro = criar_tabuleiro(num_rows, num_cols)
    game_over = False
    turn = 'X'
    num_jogadas = num_rows * num_cols

    while not game_over:
        imprimir_tabuleiro(tabuleiro, num_cols)
        print("~~~~~~~~~~~~~")

        print(f"It is now {turn}'s turn.")
        try:
            coluna = int(input(f"Select a column (1-{num_cols}) to drop your piece: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 0 <= coluna < num_cols and jogada_valida(tabuleiro, coluna):
            linha = linha_piece(tabuleiro, coluna, num_rows)
            drop_piece(tabuleiro, linha, coluna, turn)

            if piece_ganhou(tabuleiro, linha, coluna, turn, num_rows, num_cols):
                imprimir_tabuleiro(tabuleiro, num_cols)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"Congrats!!! Player {turn} wins!")
                game_over = True
                break

            num_jogadas -= 1
            if num_jogadas == 0:
                imprimir_tabuleiro(tabuleiro, num_cols)
                print("~~~~~~~~~~~~~")
                print("Draw!!!")
                break

            turn = 'O' if turn == 'X' else 'X'
        else:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Invalid choice. That column is full or out of range. Try again!")

if __name__ == "__main__":
    main()
