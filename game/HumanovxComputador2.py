from jogoConnectFour import jogoConnectFour
from MCTS import MCTS
import DecisionTree 

def jogar_HumanovsComputador2():

    jogo = jogoConnectFour()
    
    mcts = MCTS(jogo)


    while not jogo.game_over:
        jogo.imprimir_tabuleiro()
        print("~~~~~~~~~~~~~")
        print(f"It is now {jogo.jogador_atual}'s turn.")


        if jogo.jogador_atual == 'X':

            try:
                coluna = int(input("Select a column (1-7) to drop your piece: ")) -1
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if coluna not in jogo.jogadas_validas():
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Invalid choice. That column is full or out of range. Try again!")
                continue

            linha = jogo.linha_piece(coluna)
            jogador = jogo.jogador_atual
            jogo.drop_piece(linha,coluna)
            mcts.aplicar_jogada(coluna)


        else:

            print("Im thinking...")
            mcts.pesquisar(tempo_limite=2)
            coluna = mcts.melhor_jogada()
            nova_coluna = jogo.melhor_decisao(coluna)

            print(f"I choose this column: {coluna+1}")

            linha = jogo.linha_piece(coluna)
            jogador = jogo.jogador_atual
            jogo.drop_piece(linha,coluna)
            mcts.aplicar_jogada(nova_coluna)


           # num_simulacoes, tempo = mcts.estatisticas()
            #print(f"A IA fez {num_simulacoes} simulacoes em {tempo:.2f} segundos")
            

        if jogo.piece_ganhou(linha,coluna,jogador):
            jogo.imprimir_tabuleiro()
            if jogador == 'X':
                print("Congrats!! You won!")
            else:
                print("I won! Good luck next time! :)")
            jogo.game_over = True
            break

        elif jogo.num_jogadas == 0:
            jogo.imprimir_tabuleiro()
            print("Draw!!!")
            break
    
        jogo.alterar_jogador()



if __name__ == "__main__":
    jogar_HumanovsComputador2()

