# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:14:05 2018

@author: gy15hj
"""
import random 

class Agent(): 
    def __init__ (self, environment, agents, random_seed, x, y):
        '''
        initialise agents
       
        environment = spatial environment within which agents are located 
       
        agents = refers to all agents in environment 
       
        random_seed = number assigned as random seed in model - setting the 
        random seed keeps the start point for random number generation at the 
        same point each time the code is run, this can be useful if need to run 
        exact outcome more than once to identify an error 
       
        x = x axis coordinate for agent location within environment 
       
        y= y axis coordinate for agent location within environment
        
        Underscore is used before x and y as part of python convention - on 
        testing it was realised that rather than actually preventing you from 
        modifying values preceded by an underscore it simply provides a warning 
        that thye should not be altered.  
        '''
       
        '''
        Assign coordinates using 'if' and 'else' statements to ensure that
        the code can stil runs even if there are missing X and Y values within 
        the HTML file that has been read in, by generating random cordinates 
        instead.  
        '''
        if (x == None): 
            self._x = random.randint(0,100)
        else:
            self._x = x
        if (y == None): 
            self._y = random.randint(0,100)
        else:
            self._y = y
        self.environment = environment 
        self.store = 0 
        self.agents = agents 
        self.store = 0 
        self.random_seed = 1
        self.store = 0
        
    def getx(self):      
        return self._x 
        
    def setx(self, value):
        self._x = value 
        
    def delx(self):
        del self._x 
    
    def gety(self):
        return self._y 
        
    def sety(self, value):
        self._y = value 
        
    def dely(self):
        del self._y
        
    x = property(getx, setx, delx, "I'm the 'x' property.")       
    y = property(gety, sety, dely, "I'm the 'y' property.")   
    
    def move(self):
        '''
        Moves the agents randomly on the X and Y axis. 
        
        Modulus operator used to create a torus within the environment that 
        ensures agents stay witin the environment. 
        '''
        if random.random() < 0.5:
            self._x = (self._x + 1) % 100 
        else:
            self._x = (self._x - 1) % 100

        if random.random() < 0.5:
            self._y = (self._y + 1) % 100
        else:
            self._y = (self._y - 1) % 100    
            
    def eat(self):
        '''
        Agents 'eat' the environment: assigned amount (10) is removed from the 
        environment and added to agent's store 
        '''
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10         
            
    def share_with_neighbours(self, neighbourhood):
        '''
        Agent shares some of their store with others (total of both agents
        stores divivded between the 2), if within assigned 'neighbourhood' 
        distance (having culaculated the distance using 'distance_between' 
        function) and if the other agent has less in their store than 
        themselves.
        '''
        for agent in self.agents: 
            dist = self.distance_between(agent) 
            if dist <= neighbourhood: 
                #print(str(agent.store) + str(self.store)) #check stores 
                if agent.store < self.store: 
                    sum = self.store + agent.store 
                    ave = sum /2 
                    self.store = ave  
                    agent.store = ave
                    
                    '''
                    Print to check code is doing what it should do.
                    '''
                    #print("sharing " + str(dist) + " " + str(ave)) 
                    
    
    def distance_between(self, agent):
        '''
        Calculates distance between self and another agent.
        '''
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5