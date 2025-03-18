

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

def criar_tabuleiro():
    tabuleiro = [['-' for _ in range(7)] for _ in range(6)]
    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join(linha))
    print("1 2 3 4 5 6 7")    

#def posicao_valida(tabuleiro,coluna):

#def por_peca(tabuleiro,coluna,peca): drop_piece

#def peca_ganhou(tabuleiro,coluna,peca): 

#def linha_peca(tabuleiro,coluna) ?? 

tabuleiro = criar_tabuleiro()
#imprimir_tabuleiro(tabuleiro)
game_over = False
turn = 'X'

while not game_over:

    imprimir_tabuleiro(tabuleiro)
    print("~~~~~~~~~~~~~")

    if turn == 'X':
        print("It is now X's turn.")
        coluna = int(input(("Select a column to drop your piece: ")))


    else:
         print("It is now O's turn.")
         coluna = int(input("Select a column to drop your piece: "))
         

    if turn == 'X':
        turn = 'O'
    else: turn = 'X'

