# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 14:11:45 2018

@author: gy15hj

__version__ 0.1.0 

This model runs from a GUI. On running this code a window will appear. Within
this window the model will run on selection of 'Model' > 'Run Model' within 
the menu bar. 

On running the model, a number of agents (set as 10 as default) will move 
around the environment which will change colour to represent the agents 
'eating'/removing the environment. The agents retain whatever they remove from 
the environment in their store, and can share their store with nearby agents if
their store is low. 

"""
##############################################################################
############################## IMPORTING MODULES #############################
##############################################################################

import matplotlib #plotting library  
matplotlib.use('TkAgg') #change the backend to render as associated with TkInter

import random #library of random number generators 
import operator  
import matplotlib #plotting library  
import time #provides time-related functions (time code to test efficiency)
import agentframework #needed to access the file containing the Agent class 
import csv #file reading and writing 
import matplotlib.animation
import matplotlib.backends.backend_tkagg
import tkinter #GUI package 
import requests
import bs4 #library for pulling data out of HTML file 

##############################################################################

##############################################################################
############################# CREATING ENVIRONMENT ###########################
##############################################################################

'''
Create 'environment' list. Read in .txt file containing environment data to 
generate the environment in which the agents will be located. 
'''
environment = [] #create a new list in which to append rows from rowlist

f = open('in.txt') 
reader = csv.reader(f)
for row in reader:	
    rowlist = [] #create new list in which to input rows from csv reader 
    environment.append(rowlist)			
    for value in row:	
        rowlist.append(int(value))
f.close() 

'''
#Plot environment to check csv read in has worked correctly.
    
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show() #plot environment
'''

###############################################################################

'''
Lines from earlier version of code. 

#Def allows us to define our own function that can be called later.  

def distance_between(agents_row_a, agents_row_b): 
  return (((agents_row_a._x - agents_row_b._x)**2) + ((agents_row_a._y - agents_row_b._y)**2))**0.5

#Random seed now moved into agent framework. 
  
random_seed = 1 #defining the random seed 
random.seed(random_seed) #setting the random seed to that which has been defined above

'''

##############################################################################
############################ ASSIGN VARIABLES ################################
##############################################################################

num_of_agents = 2 #set the number of agents 
num_of_iterations = 100 #set the number of iterations 
neighbourhood = 20 #neighbourhood variable to determine distances when sharing
random_seed = 1 #define random seed 

##############################################################################

##############################################################################
############################## CREATE LISTS ##################################
##############################################################################

agents = [] #create agent list to which to append agents once generated 

##############################################################################

##############################################################################
########################### READ IN HTML FILE  ###############################
##############################################################################

'''
Opens connection to file via internet and reads in file, the sources x and y 
coordinates from file to set up agents.
'''
 
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

'''
Test that file has been read correctly. 

It is important to be able to check this as model is now dependent on 
successfully being able to read in this file from the internet - 
relies on School of Geography Server working etc.

print(td_ys) 
print(td_xs) 
'''

##############################################################################

##############################################################################
############################# CREATE AGENTS ##################################
##############################################################################

#ax.set_autoscale_on(False)
for i in range(num_of_agents):
    random_seed += 1
    #print ("random seed", random_seed) #print to check that random seed is changing 
    #x and y coordinates needed to initiliase agents taken from html file 
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    agents.append(agentframework.Agent(environment, agents, random_seed, x, y))

#loop creates agents located at coordinates taken from html file
#runs until num_of_agents has been satisfied 
        
##############################################################################
  
'''
#Early code exploration.

#Task 1: Measuring distances between agents and timing various methods of doing 
#this to find most efficient method:

#Clock used to time code to check for efficiency 
#start tells clock at what point in the code to start timing 

start = time.clock() 

#Attempt 1: Calculates distances between agents and appends them to 'distances' 
#list - this version is inefficient as it calculates the distance between an 
#agent and itself and repeats calculations between agents

distances =[]

for agents_row_a in agents:
    for agents_row_b in agents: 
            distance = distance_between(agents_row_a, agents_row_b)
            distances.append(distance)           
 

#Attempt 2: Intial attempt at shrinking the code so as to prevent unecessary/
#repeat distance calculations. This version appeared correct initially but 
#on testing it (printing the elements of the code), it is not actually doing 
#what is required. The line '(agents_row_a > agents_row_b)' is actually just 
#comparing the ys (the first row of the first agent and the first row of the 
#second agent) and then only calculates the distance between agents if the y of
#the first agent is bigger than the y of the second agent
            
for agents_row_a in agents:
    for agents_row_b in agents: 
        if (agents_row_a > agents_row_b): 
            print("agents_row_a > agents_row_b")
            print("agents_row_a ", agents_row_a)
            print("agents_row_b ", agents_row_b)
            
            distance = distance_between(agents_row_a, agents_row_b)
            distances.append(distance) 
        else:
            print("agents_row_a <= agents_row_b")
            print("agents_row_a ", agents_row_a)
            print("agents_row_b ", agents_row_b)

#Attempt 3: The if statement prevents distance being calculated between an 
#agent and itself or an agents to which it has already been compared 
#for example 1 does not need to compared to 1, nore does 1 need to be compared 
#to 2 if 2 has already been compared to 1. This code is therefore less 
#computationally expensive as it avoids unecessary/repeat calculations           

for i in range(num_of_agents):
    for j in range(num_of_agents):
        if (i > j):
            distance = distance_between(agents[i], agents[j])
            distances.append(distance)

#Attempt 4: Negates the need for the if statement by limiting the second loop 
#to fall within the range of i. Having utilised the timer we can see that this 
#is a more effcient way of calculating the distance between the agents. 
            
for i in range(0, num_of_agents):
    for j in range(0, i):
        distance = distance_between(agents[i], agents[j])
        distances.append(distance)     
        
#Task 2: Finding minimum and maximum distances:

#Attempt 1: having appended all the calculated distances to 'distances', the 
#the maximum value within the list is assigned to 'high' and the minimum value
#assigned to 'low'.These two new 'high' and 'low' variables can then be printed. 

high = max(distances) #assigns the highest value within 'distances' to 'high'
low = min(distances) #assigns the lowest value within 'distances' to 'low'

print (high, low) #prints high and low value 

#Attempt 2: This method combines the two tasks by calculating the distances 
#between agents by calling the distance_between function defined above and 
#appending each calculated distance to 'distances' list. Each time the loop runs it will 
#reasign the distance value to max_dist if higher than the previous assigned 
#value. Printng 'max_dist' will therefore give you the maximum value. 

max_dist = 0; #set max_dist value at 0 

for i in range(0, num_of_agents):
    for j in range(0, i):
        distance = distance_between(agents[i], agents[j])
        distances.append(distance) 
        if (distance > max_dist):
            max_dist = distance 

print("maximum distance", max_dist)     

#End tells clock at what point in code to stope timing.
       
end = time.clock() #tells the clock at what point to stop timing 

#Print the time is took to get from the start to end point.     

print("time = " + str(end - start))     
'''

'''
#Testing agent framework connection - create and print an agent. 

a = agentframework.Agent(environment, agents)  
print(a._y, a._x)
a.move()
print(a._y, a._x)

'''

##############################################################################
############################# PLOT & ANIMATE #################################
##############################################################################

fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#ax.set_autoscale_on(False)

carry_on = True	

def update(frame_number):
    
    fig.clear()
    
    '''
    Set axis to remain at 0,99 before plotting the environemt so it doesn't 
    resize to scale to agents as they move each time.
    '''
    
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.ylim(99, 0)  
    matplotlib.pyplot.imshow(environment)
    
    global carry_on  

    '''
    The shuffle function within the random library will randomise the order in 
    which the agents are processed each time the loop runs to prevent model
    artifacts. 
    
    The loop calls the move, eat and share_with_neighbours functions from 
    the agent framework.  
    '''
    random.shuffle(agents) 
    for i in range(num_of_agents):        
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
     
    '''
    Plot agents and display as red. 
    '''
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y,color='red') 

 
def gen_function(b = [0]):
    a = 0
    global carry_on 
    while (a < 10) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1

##############################################################################
###################### SET UP GUI & ANIMATE MODEL ############################
##############################################################################
        
def run(): 
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=100, repeat=False)
    #animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=10)
    canvas.show() 

root = tkinter.Tk() 
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1) 
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 

 
tkinter.mainloop()

##############################################################################