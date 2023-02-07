from pgmpy.models import BayesianNetwork as BN
from pgmpy.factors.discrete.CPD import TabularCPD
import numpy as np
from pgmpy.inference import VariableElimination




# Clase que representa una red bayesiana y sus operaciones
# recibe como parametros una lista de tuplas que representan las relaciones entre nodos
# y una lista de tuplas que representan los nodos y sus atributos
class BayesianNetwork(object):

    
    # Constructor de la clase
    # recibe como parametros una lista de tuplas que representan las relaciones entre nodos
    # y una lista de tuplas que representan los nodos y sus atributos
    def __init__(self, nodos, nodos_atributes):

        # Se inicializa el modelo de red bayesiana utilizando la lista de relaciones entre nodos
        self.model = BN(nodos)
        self.nodos_atributes = nodos_atributes

        # Se construye el grafo de la red bayesiana
        self.build_graph(nodos)
        self.cps = {}

        # Se calculan las probabilidades de los nodos
        self.set_probabilities()
        # self.factors()
        
    
    # Construir el grafo de la red bayesiana
    def build_graph(self, nodes):
        self.graph = {}
        for node in nodes:
            if node[0] in self.graph:
                if node[1] not in self.graph[node[0]]:
                    self.graph[node[0]].append(node[1])
            else:
                self.graph[node[0]] = [node[1]]

    
    # Metodo que calcula la probabilidad de que un nodo sea cierto dado un conjunto de evidencias
    def set_probabilities(self):
        # Lista de tablas de probabilidad condicional de los nodos
        cpds = []

        for nodo in self.nodos_atributes:
            if len(nodo) == 2:
                element = TabularCPD(nodo[0], 2, nodo[1])
                self.cps[nodo[0]] = [nodo[1]]        
            else:
                temp = []
                for i in range(len(nodo[2])):
                    temp.append(2)
                element = TabularCPD(nodo[0], 2, nodo[1], nodo[2], temp)
                self.cps[nodo[0]] = [nodo[1], nodo[2]]
            cpds.append(element)
        
        # Se agregan las tablas de probabilidad condicional al modelo de red bayesiana
        for element in cpds:
            self.model.add_cpds(element)

    
    # Método de enumeración para la red bayesiana para consultar la probabilidad de un nodo dado un conjunto de evidencias
    def enumeration(self,node,evidence):
        inference = VariableElimination(self.model)
        return inference.query(variables =[node], evidence=evidence)
    
        
    # Método para imprimir los factores de la red bayesiana
    def factors(self):
        factores = self.model.get_cpds()
        for factor in factores:
            print(factor)
    
    
    # Método para saber si la red bayesiana esta completamente descrita o no
    # retorna True si la red bayesiana esta completamente descrita
    def fully_described(self):
        print("Completamente descrita" if self.model.check_model() else "No completamente descrita")

    
    
    # Método para obtener la representación de la red bayesiana en forma compacta
    # retorna una cadena de texto con la representación de la red bayesiana en forma compacta
    # Ejemplo: P(A,B,C) = P(A|B,C)P(B|C)P(C)
    def compactness_representation(self):
        parent_relation = {}
        for node in self.graph:
            if node not in parent_relation:
                parent_relation[node] = {}
            
            for child in self.graph[node]:
                if child in parent_relation:
                    parent_relation[child].add(node)
                else:
                    parent_relation[child] = {node}

        left_side_equation = "P("
        right_side_equation = ""
        for element in parent_relation:
            left_side_equation += element + ','
            right_side_equation += "P(" + element 
            if len(parent_relation[element]) > 0:
                right_side_equation += ' | '
            for parents in parent_relation[element]:
                right_side_equation += parents + ','
            
            if len(parent_relation[element]) > 0:
                right_side_equation = right_side_equation[:-1] + ') '
            else :
                right_side_equation +=  ') '
        left_side_equation = left_side_equation[:-1] + ')'
        return left_side_equation + ' = ' + right_side_equation
    