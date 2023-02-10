from bayesiannetworkai import BayesianNetwork
from pgmpy.models import BayesianNetwork as BN
from pgmpy.factors.discrete.CPD import TabularCPD
import numpy as np

net = [('Burglary', 'Alarm'), 
    ('Earthquake', 'Alarm'),
    ('Alarm', 'JohnCalls'), 
    ('Alarm', 'MaryCalls')]

nodos = [
    ('Burglary', np.array([[0.001], [0.999]])),
    ('Earthquake', np.array([[0.002], [0.998]])),
    ('Alarm',np.array([[0.95, 0.94, 0.29, 0.001], [0.05, 0.06, 0.71, 0.999]]), ['Burglary', 'Earthquake']),
    ('MaryCalls', np.array([[0.70, 0.01], [0.30, 0.99]]),['Alarm']),
    ('JohnCalls', np.array([[0.90, 0.05], [0.10, 0.95]]),['Alarm'])
] 
bayesian_network = BayesianNetwork(net, nodos)

# bayesian_network.fully_described()
# bayesian_network.factors()

# bayesian_network.enumerate_all()
print(bayesian_network.enumeration('Burglary', {'JohnCalls': 0, 'MaryCalls': 0}))

#print(bayesian_network.compactness_representation())
#print(bayesian_network.prueba)


# print(bayesian_network.compactness_representation())