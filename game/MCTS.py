import random
import time
import math
from copy import deepcopy
#from jogoConnectFourAdaptador import jogoConnect4Adaptador

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
        while not estado.fim_do_jogo():
            jogada = random.choice(estado.jogadas_validas())
            estado = estado.fazer_jogada(jogada) 

        #returna 1,2 ou 3 (X ganhou, 0 ganhou ou empate)
        return estado.resultado()


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

        #vai executar simulacoes ate alcançar o tempo limite
        while time.process_time() - inicio < tempo_limite:
            no, estado = self.selecionar_no()
            resultado = self.simular(estado)
            self.backpropagate(no,estado.ultimo_jogador,resultado)
            self.num_simulacoes += 1

        self.tempo_total = time.process_time() - inicio #guarda o tempo total de execucao

    """def melhor_jogada(self):
        if self.estado_raiz.fim_do_jogo():
            return -1

        filhos_validos = [f for f in self.raiz.filhos.values() if f.jogada is not None and f.jogada>=0]
        #filhos = self.raiz.filhos.values() #jogadas possiveis a partir da raiz

        if not filhos_validos:
            #se nao conseguir expandir por falta de tempo
            jogadas_possiveis=self.estado_raiz.jogadas_validas()
            if jogadas_possiveis:
                return random.choice(jogadas_possiveis)
            else:
                return -1

        max_visitas = max(filho.visitas for filho in filhos_validos)
        melhores = [filho for filho in filhos_validos if filho.visitas == max_visitas]
        melhor = random.choice(melhores)

        #retorna a jogada associada ao melhor filho
        return melhor.jogada"""

    def melhor_jogada(self):
        jogadas_possiveis = self.estado_raiz.jogadas_validas()
        if not jogadas_possiveis:
            return -1  #o jogo realmente acabou

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
