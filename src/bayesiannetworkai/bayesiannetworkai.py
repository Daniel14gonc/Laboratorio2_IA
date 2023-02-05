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
        
    def build_graph(self, nodes):
        self.graph = {}
        for node in nodes:
            if node[0] in self.graph:
                if node[1] not in self.graph[node[0]]:
                    self.graph[node[0]].append(node[1])
            else:
                self.graph[node[0]] = [node[1]]

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

    def enumeration(self,node,evidence):
        inference = VariableElimination(self.model)
        return inference.query(variables =[node], evidence=evidence)
    
        
    def factors(self):
        factores = self.model.get_cpds()
        for factor in factores:
            print(factor)
    
    def fully_described(self):
        print("Completamente descrita" if self.model.check_model() else "No completamente descrita")

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
    