import pgmpy.models
import pgmpy.inference
import networkx as nx
import pylab as plt

class BayesianNetwork(object):

    def __init__(self,array_tuples):
        self.model = pgmpy.models.BayesianModel(array_tuples)

    def set_probabilities(self,nodo,probabilities_values,evidence):
        element = pgmpy.factors.discrete.TabularCPD(nodo, 2, probabilities_values,evidence)
        



    