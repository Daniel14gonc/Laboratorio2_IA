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

    def pamientras(self,node,evidence):
        inference = VariableElimination(self.model)
        return inference.query(variables =[node], evidence=evidence)
    
    '''
    def enumeration(self, X, evidence):
        Q = {}

        for xi in [0, 1]:
            evidence[X] = xi
            Q[xi] = self.enumerate_all(list(self.model.nodes()), evidence)

    def enumerate_all(self, variables, e):
        if not variables:
            return 1.0
        print(variables)
        print(e)
        Y = variables[0]
        # prob(Variable, valor, condiciones)
        print(self.prob(Y, e[Y], e))
        return 0
        
        if Y in e:
            return self.prob(Y, e[Y], e) * self.enumerate_all(rest, e)

        else:
            total = 0
            for y in [0, 1]:
                e[Y] = y
                total += self.prob(Y, y, e) * self.enumerate_all(rest, e)
            del e[Y]
            return total
    
    def prob(self, variable, value, conditions):
        if len(self.cps[variable]) == 1:
            return self.cps[variable][0][value][0]
    '''

        
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
    