import math 
from collections import Counter

class Agente:
    def _init_(self, id, modelo, posicao):
        #Identidade e posica
        self.id = id # identificador unico do agente
        self.posicao = posicao #coordenadas (x , y) no ambiente
        
        self.modelo = modelo # Tipo de modelo a ser usado (KNN, BAYES ou ARVORE DE DECISAO)
        self.dados_treinaento = [] # Dadodos para o treinamento do modelo
        self.modelo_treinamento = None # Representacao do modelo de treinamento
    
        #Memoria e comunicacao
        self.memoria ={
            'celula_livre' : set(),
            'bombas' : set(),
            'tesouros' : set()
        }
        
        self.comuncacao = [] #Messagens trocadas com outos agentes ???
        
        # Estatistica de desempenho
        self.tesouros_coletados = 0 #Numero de tesouros coletados
        self.caminho_percorrido = [] #Historico de posicoes visitadas
        
        #Estado 
        self.estado = "activo" # 'activo' ou 'inativo' (ex.: destruido por uma bomba)
        self.capacidade = {
            #Vantagens adquiridas
            'desarmar_bomba' : False
        }
        
    def atualizar_posicao(self , nova_posicao):
        if self.estado == "activo":
            self.posicao = nova_posicao
            self.caminho_percorrido.append(nova_posicao)
    
    def coletar_tesouro(self):
        if self.estado == "activo":
            self.tesouros_coletados += 1
            self.capacidade['desarmar_bomba'] = True
            
    def marcar_bomba(self, posicao):
        if self.estado == "activo":
            self.memoria['bombas'].add(posicao)
    
    def compartilhar_informacoes(self, outro_agente):
        if self.estado == "ativo":
            outro_agente.memoria['células_livres'].update(self.memoria['células_livres'])
            outro_agente.memoria['bombas'].update(self.memoria['bombas'])
            outro_agente.memoria['tesouros'].update(self.memoria['tesouros'])

    def treinar_modelo(self, dados):
        # Treinamento do modelo baseado no tipo do agente
        self.dados_treinamento = dados
        if self.modelo == "Decisao":
            self.modelo_treinado = self.treinar_arvore_decisao(dados)
        elif self.modelo == "KNN":
            pass  # Implementar treinamento para KNN
        elif self.modelo == "Bayes":
            pass  # Implementar treinamento para Bayes

    def treinar_arvore_decisao(self, dados):
        # Lógica para treinar uma árvore de decisão (ID3 ou outra implementação)
        def calcular_entropia(data, target_attr):
            counts = Counter(record[target_attr] for record in data)
            total = len(data)
            return -sum((count / total) * math.log2(count / total) for count in counts.values())
        
        def ganho_informacao(data, split_attr, target_attr):
            total_entropy = calcular_entropia(data, target_attr)
            values = set(record[split_attr] for record in data)
            weighted_entropy = sum(
                len()
            )
        return "Arvore de Decisão Treinada"
    
    def treinar_KNN(self, dados):
        return "Agente Treinado com base no modelo KNN"
    
    def treinar_Bayes(self, dados):
        return "Agente treinado com base no modelo de Bayes"