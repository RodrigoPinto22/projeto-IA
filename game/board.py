def criar_tabuleiro(num_rows, num_cols):
    return [['-' for _ in range(num_cols)] for _ in range(num_rows)]

def imprimir_tabuleiro(tabuleiro, num_cols):
    for linha in tabuleiro:
        print(" ".join(linha))
    print(" ".join(str(i+1) for i in range(num_cols)))  # Print column numbers dynamically

def jogada_valida(tabuleiro, coluna):
    return tabuleiro[0][coluna] == '-'

def linha_piece(tabuleiro, coluna, num_rows):
    i = 0
    while i <= num_rows - 1 and tabuleiro[i][coluna] == '-':
        i += 1
    return i - 1

def drop_piece(tabuleiro, linha, coluna, piece):
    tabuleiro[linha][coluna] = piece
