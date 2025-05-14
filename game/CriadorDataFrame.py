import pandas as pd
import os
from jogoConnectFour import jogoConnectFour
from MCTS import MCTS
from copy import deepcopy

def gerador(nJogos):

    ficheiro = "DataFrame_connectfour.csv"
    
    dataset = []
    for i in range (nJogos):
        jogo = jogoConnectFour()
        jogadorX = MCTS(deepcopy(jogo))
        jogadorO = MCTS(deepcopy(jogo))

        while not jogo.game_over:
            if jogo.jogador_atual == 'X':
                jogador = jogadorX
            else:
                jogador = jogadorO
            jogador.pesquisar(tempo_limite=2.0)
            coluna = jogador.melhor_jogada()
            
            estado_dict = {}
            tabuleiro = jogo.tabuleiro
            contador = 0
            for col in range(6):
                for row in range(7):
                    contador += 1
                    posicao = tabuleiro[col][row]
                    if posicao == 'X':
                        estado_dict[f'Pos {contador}'] = 'X'
                    elif posicao =='O':
                        estado_dict[f'Pos {contador}'] = 'O'
                    else:
                        estado_dict[f'Pos {contador}'] = None
            estado_dict['Melhor jogada'] = coluna
            estado_dict['Nº Vitorias'] = (jogador.raiz.valor_total/jogador.raiz.visitas)*100 
            dataset.append(estado_dict)

            linha = jogo.linha_piece(coluna)
            jogo.drop_piece(linha, coluna)
            jogadorX.aplicar_jogada(coluna)
            jogadorO.aplicar_jogada(coluna)

            if jogo.piece_ganhou(linha,coluna,jogo.jogador_atual):
                break
             
            jogo.alterar_jogador()

    dados = pd.DataFrame(dataset)
    escrever = not os.path.exists(ficheiro)
    dados.to_csv(ficheiro, mode='a', header = escrever, index = False)
    return


if __name__ == "__main__":
    gerador(10)
