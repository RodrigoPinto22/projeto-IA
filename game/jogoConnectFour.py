from copy import deepcopy

class jogoConnectFour:
    def __init__(self):
        self.NUM_ROWS = 6
        self.NUM_COLS = 7
        self.tabuleiro = [['-' for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        self.jogador_atual = 'X'
        self.ultimo_jogador = None
        self.game_over = False
        self.num_jogadas = self.NUM_ROWS * self.NUM_COLS

    def imprimir_tabuleiro(self):
        for linha in self.tabuleiro:
            print(" ".join(linha))
        print("1 2 3 4 5 6 7")    

    def jogada_valida(self,coluna):
        return self.tabuleiro[0][coluna] == '-'

    def linha_piece(self,coluna):
        i = 0
        while (i <= self.NUM_ROWS-1 and self.tabuleiro[i][coluna] == '-'):
            i +=1
        return i-1

    def drop_piece(self,linha,coluna):
        self.tabuleiro[linha][coluna] = self.jogador_atual
        self.ultimo_jogador = self.jogador_atual
        self.num_jogadas -= 1

    def alterar_jogador(self):
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'

    def piece_ganhou(self,linha,coluna,jogador): 

        def contar_direcao(direcaox, direcaoy):
            contador = 0
            x = linha
            y = coluna
            while 0<=x<self.NUM_ROWS and 0<=y<self.NUM_COLS and self.tabuleiro[x][y] == jogador:
                x += direcaox
                y += direcaoy
                contador += 1
            return contador

        # horizontal
        if contar_direcao(0,-1) + contar_direcao(0,1) - 1 >= 4:
            return True

        # vertical
        if contar_direcao(1,0) >= 4: #nao pode ir para cima na vertical
            return True
    
        # diagonal principal
        if contar_direcao(1,1) + contar_direcao(-1,-1) - 1 >= 4:
            return True

        # diagonal secundária
        if contar_direcao(1,-1) + contar_direcao(-1,1) -1 >=4:
            return True
        return False

    #MONTE CARLO
    
    def jogadas_validas(self):
        return [col for col in range(self.NUM_COLS) if self.jogada_valida(col)]


    def fazer_jogada(self,coluna):

        """vai criar uma copia do jogo, vai aplicar a jogada e retorna o novo estado
        isto é necessario para o MCTS conseguir simular jogadas sem alterar o jogo original/real"""


        novo_estado = deepcopy(self)
        linha = novo_estado.linha_piece(coluna)
        novo_estado.drop_piece(linha,coluna)
        novo_estado.alterar_jogador()

        #altera o jogador para a proxima jogada
        #novo_estado.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
        #novo_estado.jogador = 1 if novo_estado.jogador_atual == 'X' else 2

        #novo_estado.num_jogadas -=1

        return novo_estado        

        
    def fim_do_jogo(self):
    
        for col in range(self.NUM_COLS):
            if self.jogada_valida(col):
                linha = self.linha_piece(col)
                #simula a jogada
                self.tabuleiro[linha][col] = self.jogador_atual
                if self.piece_ganhou(linha, col, self.jogador_atual):
                    self.tabuleiro[linha][col] = '-'
                    return True
                self.tabuleiro[linha][col] = '-'
        return self.num_jogadas == 0


    def resultado(self):

        """casos:
        0 se o jogo ainda nao acabou
        1 se o X ganhar
        2 se o O ganhar
        3 se empatarem"""

        for coluna in range(self.NUM_COLS):
            if self.jogada_valida(coluna):
                linha = self.linha_piece(coluna)
                #simula a jogada
                self.tabuleiro[linha][coluna] = self.jogador_atual
                #self.ultimo_jogador = self.jogador_atual
                if self.piece_ganhou(linha, coluna,self.jogador_atual):
                    self.tabuleiro[linha][coluna] = '-'
                    return 1 if self.jogador_atual == 'X' else 2 #indica quem ganhou
                self.tabuleiro[linha][coluna] = '-' #senao desfaz a simulacao


        if self.num_jogadas == 0:
            return 3 #empate

        return 0 #jogo ainda nao terminou
