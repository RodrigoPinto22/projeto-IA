from jogoConnectFour import jogoConnectFour

def jogar_HumanovsHumano():

    jogo = jogoConnectFour()

    while not jogo.game_over:
        jogo.imprimir_tabuleiro()
        print("~~~~~~~~~~~~~")
        print(f"It is now {jogo.jogador_atual}'s turn.")
    
        try:
            coluna = int(input(("Select a column to drop your piece: "))) - 1
        except ValueError:
            print("Invalid input. Pleas enter a number.")
            continue

        if not jogo.jogada_valida(coluna):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Invalid choice. That column is full or out of range. Try again!")
            continue


        linha = jogo.linha_piece(coluna) 
        jogador = jogo.jogador_atual
        jogo.drop_piece(linha,coluna)

        if jogo.piece_ganhou(linha,coluna,jogador):
            jogo.imprimir_tabuleiro()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Congrats!!! Player {jogo.ultimo_jogador} wins!")
            jogo.game_over = True
            break
        
        #jogo.num_jogadas -= 1
        if jogo.num_jogadas == 0: #and jogo.game_over == False:
            jogo.imprimir_tabuleiro()
            print("~~~~~~~~~~~~~")
            print("Draw!!!")
            break

        jogo.alterar_jogador()
