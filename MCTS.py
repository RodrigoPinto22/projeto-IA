import random
import time
import math
from copy import deepcopy
#from jogoConnectFourAdaptador import jogoConnect4Adaptador
import concurrent.futures
import os # To potentially get cpu count

class NoBusca:
    def __init__(self,jogada,pai):
        self.jogada = jogada        #a coluna que levou a este no
        self.pai = pai              
        self.visitas = 0            
        self.valor_total = 0        #semelhante ao numero de vitorias
        """a vitoria, perda e empate vao ter valores diferentes. por exemplo,
        vitoria +=1 perda +=0 e empate +=0.5. como pode se tratar de um numero fracionario
        chamar a variavel de vitorias levaria a confusao """
        self.filhos = {}
        self.resultado = 0          #se o estado for terminal armazena 1,2 ou 3


    def adicionar_filhos(self, filhos):
        """ 
        Adiciona filhos ao dicionário da instância.

        Args:
            filhos (dict): Dicionário onde os valores são objetos com atributo 'jogada'.

        Returns:
            None
        """
        for filho in filhos:
            self.filhos[filho.jogada] = filho


    def valor(self, exploracao: float = math.sqrt(2)):
        #se o no nunca foi visitado entao deve ser explorado
        if self.visitas == 0:
            #se exploracao for 0 quer dizer que nao tenho necessidade de explorar nos nao visitados
            #caso nao seja 0, quero explorar esse antes de qualquer outro
            return 0 if exploracao == 0 else float('inf')

        
        #UCT
        media = self.valor_total / self.visitas
        fator_exploracao = exploracao * math.sqrt(math.log(self.pai.visitas)/self.visitas)
        return media + fator_exploracao

class MCTS:
    def __init__(self,estado_inicial):
        self.estado_raiz = deepcopy(estado_inicial) #fazemos uma copia do estado do jogo atual
        self.raiz = NoBusca(jogada=None, pai=None)
        self.tempo_total = 0
        self.num_simulacoes = 0
        self.debug_mostrado = False

    def selecionar_no(self):
        no = self.raiz
        estado = deepcopy(self.estado_raiz) #assim podemos fazer simulacoes à vontade

        #vai percorrer a arvore ate encontrar o melhor no nao explorado (no.visitas==0)
        while len(no.filhos) != 0:
            filhos = no.filhos.values()

            valores = [filho.valor() for filho in filhos] #calcula o UCT de cada filho
            melhor_valor = max(valores)
            

            #filtra os que têm melhor valor
            melhores = [filho for filho in filhos if filho.valor() == melhor_valor]
            no = random.choice(melhores) #escolhe aleatoriamente um dos melhores e atualiza o no atual

            estado = estado.fazer_jogada(no.jogada) #atualiza o estado (aplica a jogada)

            if no.visitas == 0: #paramos se o no ainda nao foi explorado
                return no, estado

        #se nao havia filhos ou se todos ja foram explorados, tentamos expandir
        if self.expandir(no,estado):
            #escolhe aleatoriamente um dos filhos criados
            lista_de_filhos = list(no.filhos.values())
            no = random.choice(lista_de_filhos)
            estado = estado.fazer_jogada(no.jogada)

        return no,estado


    def expandir(self, no_pai, estado):

        if estado.fim_do_jogo():
            return False #se o jogo acabou, nao tem pq expandir

        #cria um filho para cada jogada valida
        filhos = [NoBusca(jogada,no_pai) for jogada in estado.jogadas_validas()]
        no_pai.adicionar_filhos(filhos)
        return True


    def simular(self,estado):
        #simula um jogo a partir do estado atual

        #as colunas centrais dao mais oportunidades de vitoria h/v/d
        def jogadas_centrais_primeiro(jogadas):
            centro = estado.NUM_COLS // 2
            return sorted(jogadas, key=lambda x: abs(x - centro))

        
        #vai analisar se a jogada permite q o adversario venca na proxima rodada
        #heuristica de defesa
        def jogada_segura(jogada, estado_atual):
            #simula a jogada do jogador atual sem alterar o estado
            jogador_atual = estado_atual.jogador_atual
            adversario = 'O' if jogador_atual == 'X' else 'X'
            linha_jog = estado_atual.simular_jogada_temporaria(jogada, jogador_atual)
            estado_atual.alterar_jogador()

            insegura = False
            for col in estado_atual.jogadas_validas():
                linha_adv = estado_atual.simular_jogada_temporaria(col, adversario)
                if estado_atual.piece_ganhou(linha_adv, col, adversario):
                    insegura = True
                estado_atual.desfazer_jogada(linha_adv, col)
                if insegura:
                    break

            estado_atual.alterar_jogador()
            estado_atual.desfazer_jogada(linha_jog, jogada)

            return not insegura

        simulado = estado.clone()
        while not simulado.fim_do_jogo():
            jogadas = simulado.jogadas_validas()
            if not jogadas:
                break
            jogadas = jogadas_centrais_primeiro(jogadas)

            jogada_escolhida = None

            #heuristica de ataque
            for jog in jogadas:
                linha = simulado.simular_jogada_temporaria(jog, simulado.jogador_atual)
                
                if simulado.piece_ganhou(linha, jog, simulado.jogador_atual):
                    simulado.desfazer_jogada(linha, jog)
                    jogada_escolhida = jog
                    break

                simulado.desfazer_jogada(linha, jog)

            #se nenhuma jogada vencer uso a heuristica de defesa
            if jogada_escolhida is None:
                for jog in jogadas:
                    testar_estado = simulado.clone()
                    if jogada_segura(jog, testar_estado):
                        jogada_escolhida = jog
                        break

            #caso nenhuma seja segura, escolhe a mais central
            if jogada_escolhida is None:
                jogada_escolhida = jogadas[0]

            #aplica jogada escolhida
            linha = simulado.linha_piece(jogada_escolhida)
            simulado.tabuleiro[linha][jogada_escolhida] = simulado.jogador_atual
            simulado.num_jogadas -= 1
            simulado.alterar_jogador()

        #returna 1,2 ou 3 (X ganhou, 0 ganhou ou empate)
        return simulado.resultado()


    def backpropagate(self,no,jogador,resultado):
        #1 se o jogador em questao venceu, 0 se perdeu
        if (resultado == 1 and jogador == 'X') or (resultado == 2 and  jogador == 'O'):
            recompensa = 1
        elif resultado == 3:
            recompensa = 0.5
        else:
            recompensa = 0

        while no is not None:
            no.visitas +=1
            no.valor_total +=recompensa

            if resultado == 3:
                recompensa = 0.5
            else:
                recompensa = 1 - recompensa #vamos alterar a recompensa entre os niveis da arvore

            no = no.pai

    def pesquisar(self,tempo_limite):
        inicio = time.process_time()
        self.num_simulacoes = 0
        # Determine the number of threads, e.g., based on CPU cores or a fixed number
        # Using min(4, os.cpu_count() or 1) as a reasonable default to avoid overwhelming systems
        num_workers = min(4, os.cpu_count() or 1) 

        # Use ThreadPoolExecutor for parallel simulations
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # vai executar simulacoes ate alcançar o tempo limite
            while time.process_time() - inicio < tempo_limite:
                
                futures = []
                nodes_and_states = [] # Store nodes and original player for backpropagation

                # Launch parallel simulations based on available workers
                # We select nodes sequentially but simulate in parallel
                for _ in range(num_workers):
                     # Check time before starting a new batch of selections/simulations
                    if time.process_time() - inicio >= tempo_limite:
                        break

                    no, estado = self.selecionar_no()
                    
                    # If expansion leads to a terminal state, simulate might not be needed
                    # or handle appropriately. Here we assume simulation is always run.
                    # We need the player *before* the simulation potentially changes it.
                    ultimo_jogador_antes_sim = estado.ultimo_jogador 

                    # Submit simulation task to the executor
                    # Crucially, pass a clone of the state to each simulation
                    future = executor.submit(self.simular, estado.clone())
                    futures.append(future)
                    nodes_and_states.append((no, ultimo_jogador_antes_sim)) # Store node and player for backpropagation

                if not futures: # Break if no futures were submitted (e.g., time ran out)
                     break
                     
                # Collect results and backpropagate
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    try:
                        resultado = future.result()
                        no_orig, jogador_orig = nodes_and_states[i]
                        # Backpropagate results sequentially to avoid race conditions on node updates
                        self.backpropagate(no_orig, jogador_orig, resultado)
                        self.num_simulacoes += 1
                    except Exception as e:
                        print(f"Error during simulation or backpropagation: {e}")
                        # Decide how to handle errors, e.g., log them, skip backpropagation for this sim

        self.tempo_total = time.process_time() - inicio #guarda o tempo total de execucao


    def melhor_jogada(self):
        jogadas_possiveis = self.estado_raiz.jogadas_validas()
        jogador = self.estado_raiz.jogador_atual
        if not jogadas_possiveis:
            return -1  #o jogo realmente acabou


        #ataque
        for col in jogadas_possiveis:
            estado_teste = self.estado_raiz.clone()
            try:
                linha = estado_teste.simular_jogada_temporaria(col, jogador)
                if estado_teste.piece_ganhou(linha, col, jogador):
                    return col
            except:
                continue

        #defesa
        adversario = 'O' if jogador == 'X' else 'X'
        for col in jogadas_possiveis:
            estado_teste = self.estado_raiz.clone()
            try:
                linha = estado_teste.simular_jogada_temporaria(col, adversario)
                if estado_teste.piece_ganhou(linha, col, jogador):
                    return col
            except:
                continue


        filhos_validos = [f for f in self.raiz.filhos.values() if f.jogada in jogadas_possiveis]

        if not filhos_validos:
            #nao teve tempo para expandir
            return random.choice(jogadas_possiveis)

        max_visitas = max(filho.visitas for filho in filhos_validos)
        melhores = [filho for filho in filhos_validos if filho.visitas == max_visitas]
        melhor = random.choice(melhores)

        return melhor.jogada

    def aplicar_jogada(self,jogada):

        if jogada in self.raiz.filhos:
            self.estado_raiz = self.estado_raiz.fazer_jogada(jogada)
            self.raiz = self.raiz.filhos[jogada]

        else:
            self.estado_raiz = self.estado_raiz.fazer_jogada(jogada)
            self.raiz = NoBusca(jogada=None,pai=None)

    def estatisticas(self):
        return self.num_simulacoes, self.tempo_total
        
