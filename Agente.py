import math 
from collections import Counter
import random

class Agente:
    def __init__(self, id, modelo, posicao):
        self.id = id  # Identificador único do agente
        self.posicao = posicao  # Coordenadas (x, y) no ambiente
        
        self.modelo = modelo  # Tipo de modelo a ser usado (KNN, BAYES ou ARVORE DE DECISAO)
        self.dados_treinamento = []  # Dados para o treinamento do modelo
        self.modelo_treinado = None  # Representação do modelo treinado
    
        # Inicialização do dicionário para Árvore de Decisão
        self.arvore_decisao = {}

        # Memória e comunicação
        self.memoria = {
            'celulas_livres': set(),
            'bombas': set(),
            'tesouros': set()
        }
        
        self.comunicacao = []  # Mensagens trocadas com outros agentes
        
        # Estatística de desempenho
        self.tesouros_coletados = 0  # Número de tesouros coletados
        self.caminho_percorrido = []  # Histórico de posições visitadas
        
        # Estado 
        self.estado = "ativo"  # 'ativo' ou 'inativo' (ex.: destruído por uma bomba)
        self.capacidade = {
            # Vantagens adquiridas
            'desarmar_bomba': False
        }
        
    def atualizar_posicao(self, nova_posicao):
        if self.estado == "ativo":
            self.posicao = nova_posicao
            self.caminho_percorrido.append(nova_posicao)
    
    def coletar_tesouro(self):
        if self.estado == "ativo":
            self.tesouros_coletados += 1
            self.capacidade['desarmar_bomba'] = True
            
    def marcar_bomba(self, posicao):
        if self.estado == "ativo":
            self.memoria['bombas'].add(posicao)
    
    def compartilhar_informacoes(self, outro_agente):
        if self.estado == "ativo" and outro_agente.estado == "ativo":
            outro_agente.memoria['celulas_livres'].update(self.memoria['celulas_livres'])
            outro_agente.memoria['bombas'].update(self.memoria['bombas'])
            outro_agente.memoria['tesouros'].update(self.memoria['tesouros'])

    def treinar_modelo(self, dados):
        self.dados_treinamento = dados
        if self.modelo == "Decisao":
            self.modelo_treinado = self.treinar_arvore_decisao(dados)
        elif self.modelo == "KNN":
            self.modelo_treinado = self.treinar_KNN(dados)
        elif self.modelo == "Bayes":
            self.modelo_treinado = self.treinar_Bayes(dados)
        else:
            raise ValueError(f"Modelo {self.modelo} não reconhecido")

    def treinar_arvore_decisao(self, dados):
        self.arvore_decisao = {}
        
        for dado in dados:
            tipo = dado['tipo']
            resultado = dado['resultado']
            
            if tipo not in self.arvore_decisao:
                self.arvore_decisao[tipo] = Counter()
            
            self.arvore_decisao[tipo][resultado] += 1
            
        return self.arvore_decisao
    
    def prever_arvore_decisao(self, tipo):
        if tipo in self.arvore_decisao:
            return self.arvore_decisao[tipo].most_common(1)[0][0]
        return "Desconhecido"

    def treinar_KNN(self, dados):
        self.dados_treinamento = dados
        return "Modelo KNN treinado"
    
    def treinar_Bayes(self, dados):
        self.dados_treinamento = dados
        return "Modelo Bayes treinado"

class Ambiente:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho
        self.matriz = [[random.choice(['L', 'B', 'T']) for _ in range(tamanho)] for _ in range(tamanho)]
        
    def mostrar_ambiente(self):
        for linha in self.matriz:
            print(" ".join(linha))
    
    def verificar_celula(self, x, y):
        return self.matriz[x][y]

    def mover_agente(self, agente, nova_posicao):
        x, y = nova_posicao
        conteudo = self.verificar_celula(x, y)
        if conteudo == 'B':
            agente.estado = 'inativo'
            print(f"Agente {agente.id} destruído por uma bomba em {nova_posicao}")
        elif conteudo == 'T':
            agente.coletar_tesouro()
            print(f"Agente {agente.id} encontrou um tesouro em {nova_posicao}")
        else:
            print(f"Agente {agente.id} moveu-se para {nova_posicao}")
        agente.atualizar_posicao(nova_posicao)
        
# Exemplo de uso
if __name__ == "__main__":
    dados_treino = [
        {'posicao': (0, 0), 'tipo': 'L', 'resultado': 'continuar'},
        {'posicao': (0, 1), 'tipo': 'B', 'resultado': 'destruido'},
        {'posicao': (1, 0), 'tipo': 'T', 'resultado': 'fortalecido'},
        {'posicao': (1, 1), 'tipo': 'L', 'resultado': 'continuar'}
    ]
    
    agente = Agente(id=1, modelo="Decisao", posicao=(0, 0))
    agente.treinar_modelo(dados_treino)
    print("Modelo Treinado:", agente.modelo_treinado)
    
    tipo_teste = 'L'
    previsao = agente.prever_arvore_decisao(tipo_teste)
    print(f"Previsão para tipo '{tipo_teste}': {previsao}")
