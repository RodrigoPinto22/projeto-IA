

"""class connectFour:
    def __init__(self):
        self.linhas = 6
        self.colunas = 7
        self.tabela = [['-' for _ in range(self.colunas)] for _ in range(self.linhas)]

    def imprimir_tabela(self):
        numero_linha = 1
        for linha in self.tabela:
            print(f" ".join(linha))
            #print(f"{numero_linha}: " + " ".join(linha))
            #print(" ".join(linha))
            #print("\n")
            numero_linha += 1
        print("1 2 3 4 5 6 7")

jogo = connectFour()
jogo.imprimir_tabela()"""

NUM_ROWS = 6
NUM_COLS = 7

def criar_tabuleiro():
    tabuleiro = [['-' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join(linha))
    print("1 2 3 4 5 6 7")    

def jogada_valida(tabuleiro,coluna):
    return tabuleiro[0][coluna] == '-'

"""def por_peca(tabuleiro,coluna,peca): função luiza
    
    for i in range(5, -1, -1):
        if (tabuleiro[i][coluna - 1] == '-' ):
            tabuleiro[i][coluna - 1] = peca
            break"""


def linha_piece(tabuleiro,coluna):
    i = 0
    while (i <= NUM_ROWS-1 and tabuleiro[i][coluna] == '-'):
        i +=1
    return i-1


def drop_piece(tabuleiro,linha,coluna,piece):
    tabuleiro[linha][coluna] = piece

def piece_ganhou(tabuleiro,linha,coluna,piece): 
    def contar_direcao(direcaox, direcaoy,piece):
        contador = 0
        x = linha
        y = coluna
        while 0<=x<NUM_ROWS and 0<=y<NUM_COLS and tabuleiro[x][y] == piece:
            x += direcaox
            y += direcaoy
            contador += 1
        return contador

    #horizontal
    if contar_direcao(0,-1,piece) + contar_direcao(0,1,piece) - 1 >= 4:
        return True

    #vertical
    if contar_direcao(1,0,piece) >= 4: #nao pode ir para cima na vertical
        return True
    
    #diagonais
    if contar_direcao(1,1,piece) + contar_direcao(-1,-1,piece) - 1 >= 4:
        return True

    #a outra diagonal (n me lembro do nome)
    if contar_direcao(1,-1,piece) + contar_direcao(-1,1,piece) -1 >=4:
        return True
    return False

tabuleiro = criar_tabuleiro()
game_over = False
turn = 'X'

num_jogadas = NUM_ROWS*NUM_COLS
while not game_over:

    imprimir_tabuleiro(tabuleiro)
    print("~~~~~~~~~~~~~")

    print("It is now " + turn + "'s turn.")
    coluna = int(input(("Select a column to drop your piece: "))) - 1

    if jogada_valida(tabuleiro,coluna):
        linha = linha_piece(tabuleiro,coluna) 
        drop_piece(tabuleiro,linha,coluna,turn)
        if piece_ganhou(tabuleiro,linha,coluna,turn):
            imprimir_tabuleiro(tabuleiro)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Congrats!!! Player "+ turn +" wins!")
            game_over = True
        num_jogadas -= 1
        if (num_jogadas == 0 and game_over == False):
            imprimir_tabuleiro(tabuleiro)
            print("~~~~~~~~~~~~~")
            print("Draw!!!")
            break
        
    else:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Invalid choice. That column is full. Try again!")
        continue

    if turn == 'X':
        turn = 'O'
    else: turn = 'X'


