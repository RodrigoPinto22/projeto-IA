def piece_ganhou(tabuleiro, linha, coluna, piece, num_rows, num_cols):
    def contar_direcao(direcaox, direcaoy, piece):
        contador = 0
        x, y = linha, coluna
        while 0 <= x < num_rows and 0 <= y < num_cols and tabuleiro[x][y] == piece:
            x += direcaox
            y += direcaoy
            contador += 1
        return contador

    # Check horizontal
    if contar_direcao(0, -1, piece) + contar_direcao(0, 1, piece) - 1 >= 4:
        return True

    # Check vertical
    if contar_direcao(1, 0, piece) >= 4:  # No need to check upward
        return True

    # Check diagonal (bottom-left to top-right)
    if contar_direcao(1, 1, piece) + contar_direcao(-1, -1, piece) - 1 >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    if contar_direcao(1, -1, piece) + contar_direcao(-1, 1, piece) - 1 >= 4:
        return True

    return False
