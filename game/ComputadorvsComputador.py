from jogoConnectFour import jogoConnectFour
#from jogoConnectFourAdaptador import jogoConnect4Adaptador
from MCTS import MCTS
from copy import deepcopy


def jogar_ComputadorvsComputador():
    jogo = jogoConnectFour()
    estado = jogoConnect4Adaptador(jogo)

    computador_X = MCTS(deepcopy(estado))
    computador_O = MCTS(deepcopy(estado))

    jogador_atual = 'X'

    print("\nWhich one is going to win?\n")

    while not jogo.game_over:
        jogo.imprimir_tabuleiro()

        computador = computador_X if jogador_atual == 'X' else computador_O

        print(f"Player {jogador_atual} is thinking...")
        computador.pesquisar(tempo_limite=1.5)
        coluna = computador.melhor_jogada()

        print(f"Player {jogador_atual} chose the column {coluna+1}")

        linha = jogo.linha_piece(coluna)
        jogo.drop_piece(linha,coluna)

        computador_X.aplicar_jogada(coluna)
        computador_O.aplicar_jogada(coluna)

        if jogo.piece_ganhou(linha,coluna):
            jogo.imprimir_tabuleiro()
            print(f"Player {jogador_atual} won!!!")
            break

        elif jogo.num_jogadas == 0:
            jogo.imprimir_tabuleiro()
            print(f"Draw!!!")
            break

        jogador_atual = 'O' if jogador_atual == 'X' else 'X'

if __name__ == "__main__":
    jogar_ComputadorvsComputador()
