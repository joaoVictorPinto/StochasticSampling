
from simulator import Simulator ,SimulationMethod
from simulator import Node, Graph, LoggingLevel


prior_B = [0.3, 0.7]
prior_E = [0.4, 0.6]
prior_P = [0.5, 0.5]
prior_A = [[[0.3, 0.7], [0.2, 0.8]], [[0.7, 0.3], [0.6, 0.4]]]
prior_J = [[[0.2, 0.8], [0.4, 0.6]], [[0.6, 0.4], [0.7, 0.3]]]
prior_M = [[0.3, 0.7], [0.2, 0.8]]


B = Node('B', prior_B)
E = Node('E', prior_E)
P = Node('P', prior_P)
A = Node('A', prior_A, parents = [B, E])
J = Node('J', prior_J, parents = [P, A])
M = Node('M', prior_M, parents = [A]   )

rede = Graph([B, E, P, A, J, M])

#MC = Simulator( rede, 20000, method = SimulationMethod.LikelyhoodWeighting , level = LoggingLevel.DEBUG )
MC = Simulator( rede, 20000, method = SimulationMethod.LogicalSampling , level = LoggingLevel.INFO )
MC.initialize()
MC.execute()
MC.finalize()



print 'P(B=0) = ',B.freq_norm(0)
print 'P(B=1) = ',B.freq_norm(1)

print 'P(E=0) = ',E.freq_norm(0)
print 'P(E=1) = ',E.freq_norm(1)

print 'P(P=0) = ',P.freq_norm(0)
print 'P(P=1) = ',P.freq_norm(1)

print 'P(A=0) = ',A.freq_norm(0)
print 'P(A=1) = ',A.freq_norm(1)


print 'P(J=0) = ',J.freq_norm(0) 
print 'P(J=1) = ',J.freq_norm(1)

print 'P(M=0) = ',M.freq_norm(0)
print 'P(M=1) = ',M.freq_norm(1)




