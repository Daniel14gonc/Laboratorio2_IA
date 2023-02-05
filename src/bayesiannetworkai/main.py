from bayesiannetworkai import BayesianNetwork
from pgmpy.models import BayesianNetwork as BN
from pgmpy.factors.discrete.CPD import TabularCPD

net = [('Burglary', 'Alarm'), 
    ('Earthquake', 'Alarm'),
    ('Alarm', 'JohnCalls'), 
    ('Alarm', 'MaryCalls')]

nodos = [
    ('Burglary', [[0.001], [0.999]]),
    ('Earthquake', [[0.002], [0.998]]),
    ('Alarm',[[0.95, 0.94, 0.29, 0.001], [0.05, 0.06, 0.71, 0.999]], ['Burglary', 'Earthquake']),
    ('MaryCalls', [[0.70, 0.01], [0.30, 0.99]],['Alarm']),
    ('JohnCalls', [[0.90, 0.05], [0.10, 0.95]],['Alarm'])
] 
bayesian_network = BayesianNetwork(net, nodos)

bayesian_network.fully_described()
bayesian_network.factors()

# bayesian_network.enumeration('JohnCalls', {'Burglary': 1, 'Earthquake': 0})


print(bayesian_network.compactness_representation())