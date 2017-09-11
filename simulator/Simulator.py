#coding: utf-8

# Inferencia 
# Nome: Joao Victor da Fonseca Pinto

__all__ = ['Simulator', 'SimulationMethod']

from Logger import Logger, LoggingLevel, EnumStringification, retrieve_kw, NotSet
from Graph import Node, Graph
import sys

# helper function to display a progress bar
def progressbar(it, prefix="", size=60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "█"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()


# Enumeracao para escolha do metodo de simulacao que sera usado
# na classe Simulator
class SimulationMethod(EnumStringification):
  LogicalSampling = 0
  LikelyhoodWeighting = 1


class Simulator(Logger):

  def __init__( self, graph, max_epoch = 1e5, **kw ):

    Logger.__init__(self, **kw)
    self._level   = retrieve_kw( kw, 'level'   , LoggingLevel.INFO                )
    self._method  = retrieve_kw( kw, 'method'  , SimulationMethod.LogicalSampling )
    self._graph = graph
    self._max_epoch = max_epoch

  def initialize(self):
    self._graph.setLevel(self.getLevel())
    self._graph.initialize()

  def execute(self):
    ### loop over epochs
    for epoch in progressbar( range(int(self._max_epoch)), 'Computing', 100 ):
    #for epoch in range(int(self._max_epoch):
      
      self._logger.debug('Start epoch: %d',epoch)
      if self._method is SimulationMethod.LogicalSampling:
        # Apply the logical sampling method 
        self._logicalSampling()
      elif self._method is SimulationMethod.LikelyhoodWeighting:
        # Apply the likelihood method
    	  self._likelihoodWeighting()
      else:
    	  self._logger.fatal('Metodo invalido...')


  def finalize(self):
    pass


  def _likelihoodWeighting(self):

    def calc_likelyhood(graph):
      likelyhood = 1.0
      for node in graph:
        if not node.evidence() is NotSet:
          likelyhood *= node.likelyhood()
      return likelyhood

    for node in self._graph:
      if node.evidence() is NotSet:
        node.draw()
      else:
        node.update_evidence()
    likelyhood = calc_likelyhood(self._graph)
    for node in self._graph:
      node.update_freq(likelyhood)


  def _logicalSampling(self):
    
    def check_evidence(graph):
    	valid=True
    	for node in graph:
    		if node.evidence() is not NotSet:
    			if node.evidence() != node.state():
    				valid=False; break;
    	return valid 
        
    self._logger.debug('Apply logical sampling method...')
    while True:
      for node in self._graph:
      	node.draw()
      if check_evidence(self._graph):
      	for node in self._graph:
          self._logger.debug('Node %s: Updating frequency...',node.name())
          node.update_freq()
          self._logger.debug('Node %s: freq_norm,  P(0)= %1.4f, P(1) = %1.4f', node.name(),node.freq_norm(0),node.freq_norm(1))
      	break
          
    





