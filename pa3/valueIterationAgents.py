# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #run value iteration for the given number of iterations
        for i in range(iterations):
          #get the currentvalues from the counter
          currentvalues = util.Counter()
          # calculate values for each state
          for state in self.mdp.getStates():
            #initialized to none to handle the case when the state has no actions
            currentvalue = None
            # calculate values for each action from a state
            for action in self.mdp.getPossibleActions(state):
              qvalue = self.computeQValueFromValues(state,action)
              if qvalue > currentvalue or currentvalue==None :
                currentvalue = qvalue
            # if the state has no actions then don't give any positive or negative reward
            if currentvalue == None:
              currentvalue = 0
            currentvalues[state] = currentvalue
          self.values = currentvalues



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qvalue = 0
        # calculate q-value for the chance node, iterate over all transition states from the chance node
        for next_state, prob in self.mdp.getTransitionStatesAndProbs(state,action):
            qvalue= qvalue + prob * (self.mdp.getReward(state, action, next_state) + (self.discount * self.values[next_state]))

        return qvalue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        value = None
        bestaction = None
        # in terminal state return action none
        if len(self.mdp.getPossibleActions(state)) == 0:
            return None
        # iterate over all possible actions to find the best action
        for action in self.mdp.getPossibleActions(state):
            qvalue = self.computeQValueFromValues(state, action)
            # find the max currentvalue and return the action for the max value as the best action
            if qvalue > value or value == None:
                value = qvalue
                bestaction = action

        return bestaction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
