# Trabalho de CPE 726 - Topicos Especiais em Inferencia em Grafos
# Author: Joao Victor da Fonseca Pinto


__all__ = ['Node','Graph']

from simulator import Logger, LoggingLevel, EnumStringification, retrieve_kw, NotSet
import random as rng


class Node(Logger):

  _prng = rng

  def __init__(self, name, cpt, **kw):

    Logger.__init__(self, **kw)
    self._parents  = retrieve_kw( kw, 'parents', NotSet            )
    self._description = retrieve_kw( kw, 'description'  , str()    )
    self._name     = name
    self._cpt      = cpt
    self._evidence = NotSet
    self._state    = NotSet

    if self._parents is NotSet:
      self._nstate   = len(cpt)
    else:
      from copy import copy
      prior = copy(cpt[0])
      for i in range(1,len(self._parents)): prior=prior[0]
      self._nstate=len(prior)

    self._logger.info('Node %s was created.',self._name)

  def initialize(self):
    self._logger.info('Initializing Node %s with %d states.',self._name,self._nstate)
    self._draw = 0
    self._frequency_states = [ 0 for _ in range(self._nstate)] 

  def finalize(self):
    self._logger.info('Prior probabilities (normalized) for the node %s',self.name())
    for state in range(self._nstate):
      print ('P(%s=%d) = %1.4f') % (self._name,state,self.freq_norm(state))

  def execute(self):
    pass

  def add_parent(self, node):
    self._parents.append(node)  

  def name(self):
    return self._name

  def set_state(self, state):
    self._state = state

  def state(self):
    return self._state

  def set_evidence( self, evidence ):
    self._evidence = evidence

  def evidence(self):
    return self._evidence

  # retorna a frequencia normalizada do estado do no. No caso discreto binario, state pode 
  # set 0 (False) ou 1 (True) considerando o exemplo do terremoto do livro do korb.
  def freq_norm(self, state):
    return (self._frequency_states[state]/float(self._draw))
  
  # Atualize os valores da freq no estado atual
  def update_freq(self, inc=1):
  	self._draw+=inc; self._frequency_states[self.state()]+=inc
 
  # retorna a prob a priore considerando o estado dos pais.
  def prior(self):
    from copy import copy
    prior = copy(self._cpt) # make the CPT copy for safety
    if not self._parents is NotSet:
      for idx, parent in enumerate(self._parents):
        prior = prior[parent.state()]
    return prior

  # Faz um novo sorteio considerando a tabela discreta das probabilidades
  def draw(self):
    state = 0; low = 0;
    prior_prob = self.prior()
    upp = prior_prob[0]
    rng = self._prng.random()
    while True:
      if (rng > low) and (rng <= upp):
        break
      else:
        state+=1; low=upp; upp=upp+prior_prob[state]
    self._state = state
 
  

class Graph(Logger):

  def __init__(self, nodes, **kw):
    Logger.__init__(self, **kw)
    self._nodes = nodes

  def __add__(self,node):
    self._nodes.append(node)

  def __getitem__(self, node):
    return self._nodes[node]

  def initialize(self):
    for node in self._nodes:
      node.setLevel(self.getLevel())
      node.initialize()

  def execute(self):
    for node in self._nodes:
      node.execute()

  def finalize(self):
    for node in self._nodes:
      node.finalize()










