from jogoConnectFour import jogoConnectFour
#from jogoConnectFourAdaptador import jogoConnect4Adaptador
from MCTS import MCTS
from copy import deepcopy


def jogar_ComputadorvsComputador():
    jogo = jogoConnectFour()
    #estado = deepcopy(jogo)

    computador_X = MCTS(deepcopy(jogo))
    computador_O = MCTS(deepcopy(jogo))

    #jogador_atual = 'X'

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
        computador.pesquisar(tempo_limite=3.0)
        coluna = computador.melhor_jogada()

        print(f"Player {jogo.jogador_atual} chose the column {coluna+1}")

        linha = jogo.linha_piece(coluna)
        jogador = jogo.jogador_atual
        jogo.drop_piece(linha,coluna)

        computador_X.aplicar_jogada(coluna)
        computador_O.aplicar_jogada(coluna)

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
    jogar_ComputadorvsComputador()
