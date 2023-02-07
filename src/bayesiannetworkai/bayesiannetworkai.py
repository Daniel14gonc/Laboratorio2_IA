from pgmpy.models import BayesianNetwork as BN
from pgmpy.factors.discrete.CPD import TabularCPD
import numpy as np
from pgmpy.inference import VariableElimination

class BayesianNetwork(object):

    def __init__(self, nodos, nodos_atributes):
        self.model = BN(nodos)
        self.nodos_atributes = nodos_atributes
        self.build_graph(nodos)
        self.cps = {}
        self.set_probabilities()
        # self.factors()
        
    '''
        Metodo para construir el grafo de la red bayesiana, recibe una lista de tuplas
        donde cada tupla representa una arista, la primera posicion de la tupla es el nodo padre
        y la segunda posicion es el nodo hijo.
    '''
    def build_graph(self, nodes):
        self.graph = {}
        for node in nodes:
            if node[0] in self.graph:
                if node[1] not in self.graph[node[0]]:
                    self.graph[node[0]].append(node[1])
            else:
                self.graph[node[0]] = [node[1]]

    '''
        Metodo para establecer las probabilidades de cada nodo, utiliza la lista de tuplas self.nodos_atributes
        donde cada tupla representa un nodo, la primera posicion de la tupla es el nombre del nodo
        y la segunda posicion es un arreglo de numpy con las probabilidades del nodo, si el nodo
        tiene padres, la tercera posicion de la tupla es una lista con los nombres de los padres
        del nodo.
    '''
    def set_probabilities(self):
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
        
        for element in cpds:
            self.model.add_cpds(element)

    '''
        Metodo para obtener la probabilidad de un nodo dado un conjunto de evidencias
        recibe el nombre del nodo y un diccionario con las evidencias, donde la llave es el nombre
        del nodo y el valor es el valor de la evidencia.
        Retorna un arreglo de numpy con las probabilidades del nodo.
    '''
    def enumeration(self,node,evidence):
        inference = VariableElimination(self.model)
        e = inference.query(variables =[node], evidence=evidence)
        return e.values
    
    '''
        Metodo que imprime los factores de la red bayesiana. 
        Devuelve una lista con los factores de la red bayesiana.
    '''
    def factors(self):
        factores_list = []
        factores = self.model.get_cpds()
        for factor in factores:
            factores_list.append(factor)
            print(factor)
        return factores_list
    
    '''
        Metodo que imprime si la red bayesiana esta completamente descrita o no.
        Devuelve True si la red bayesiana esta completamente descrita, False en caso contrario.
    '''
    def fully_described(self):
        print("Completamente descrita" if self.model.check_model() else "No completamente descrita")
        return self.model.check_model()

    '''
        Metodo que imprime la representacion compacta de la red bayesiana.
    '''
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
    