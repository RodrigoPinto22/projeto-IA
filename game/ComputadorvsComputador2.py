import pandas as pd
from jogoConnectFour import jogoConnectFour
#from jogoConnectFourAdaptador import jogoConnect4Adaptador
from MCTS import MCTS
from copy import deepcopy

data = []


def jogar_ComputadorvsComputador2():
    jogo = jogoConnectFour()
    

    computador_X = MCTS(deepcopy(jogo))
    computador_O = MCTS(deepcopy(jogo))

    
    print("\nWhich one is going to win?\n")

    while not jogo.game_over:
        jogo.imprimir_tabuleiro()
        print("~~~~~~~~~~~~~")
        print(f"It is now {jogo.jogador_atual}'s turn.")

        if jogo.jogador_atual == 'X':
            computador = computador_X
        else:
            computador = computador_O

        print(f"Player {jogo.jogador_atual} is thinking...")
        computador.pesquisar(tempo_limite=2.0)
        coluna = computador.melhor_jogada()
        nova_coluna = jogo.melhor_decisao(coluna)

        print(f"Player {jogo.jogador_atual} chose the column {coluna+1}")

        linha = jogo.linha_piece(nova_coluna)
        jogador = jogo.jogador_atual
        jogo.drop_piece(linha,nova_coluna)

        computador_X.aplicar_jogada(nova_coluna)
        computador_O.aplicar_jogada(nova_coluna)

        num_simulacoes, tempo = computador.estatisticas()
        print(f"Simulations: {num_simulacoes} in {tempo:.2f} seconds")

        if jogo.piece_ganhou(linha,coluna,jogo.jogador_atual):
            jogo.imprimir_tabuleiro()
            if jogador == 'X':
                print("Player X wins!!!")
            else:
                print("Player O wins!!!")
            break

        elif jogo.num_jogadas == 0:
            jogo.imprimir_tabuleiro()
            print(f"Draw!!!")
            break

        jogo.alterar_jogador()

if __name__ == "__main__":
    jogar_ComputadorvsComputador2()
