import sys
import os
import math
import time
import string
import time

import operator
import numpy as np

start_time = time.time()


data = open("input.txt").read().strip().splitlines()

output = open("/Users/Piyush/Desktop/output.txt", "w+") # Creating output file data
# output = open("output.txt", "w+")

filetext = [] # filetext is a list storing each line in input file

for line in data:
    filetext.append(line)  # appending each line in input file to filetext

grid_size = int(filetext[0]) # grid_size denoting the size of grid
print "grid_size"
print grid_size

cars_num = int(filetext[1]) # cars_num denoting the number of cars
print "cars_num"
print cars_num

obstacles_num = int(filetext[2]) # obstacles_num denoting the number of obstacles
print "obstacles_num"
print obstacles_num

# obstacles_coordinates list denoting the location of obstacles
obstacles_coordinates = (filetext[3:3+int(obstacles_num)]) # Putting all elements from filetext's line 3 till line number of 'obstacles_num' into 'obstacles_coordinates' list

obstacles_coordinates_list = [] # list of tuples - obstacles_coordinates_list
for coordinate in obstacles_coordinates:
    x_coordinate = int(coordinate.split(",", 1)[0])
    y_coordinate = int(coordinate.split(",", 1)[1])
    obstacles_coordinates_list.append((x_coordinate,y_coordinate))

print "Obstacle Coordinates List"
print obstacles_coordinates_list

start_cars = filetext[3+int(obstacles_num):3+int(obstacles_num)+int(cars_num)] # start_cars_list denoting the start location of each car
start_cars_list = [] # list of tuples - start_cars_list
for coordinate in start_cars:
    x_coordinate = int(coordinate.split(",", 1)[0])
    y_coordinate = int(coordinate.split(",", 1)[1])
    start_cars_list.append((x_coordinate,y_coordinate))

print "Start Cars List"
print start_cars_list

terminal_cars = filetext[3+int(obstacles_num)+int(cars_num):3+int(obstacles_num)+int(cars_num)+int(cars_num)] # terminal_cars_list denoting the terminal location of each car
terminal_cars_list = [] # list of tuples - terminal_cars_list
for coordinate in terminal_cars:
    x_coordinate = int(coordinate.split(",", 1)[0])
    y_coordinate = int(coordinate.split(",", 1)[1])
    terminal_cars_list.append((x_coordinate,y_coordinate))

print "terminal_cars_list"
print terminal_cars_list

states_set = set() # States_set
rewards_dict = {} # Rewards_Dictionary
for i in range(grid_size):
    for j in range(grid_size):
        rewards_dict[(i,j)] = -1 # Assigning each element in rewards_dict the value of -1
        states_set.add((i,j)) # list of tuples in states_list

for x,y in obstacles_coordinates_list:
    rewards_dict[(x,y)] = -101 # Assigning obstacle_location in rewards_dict the value of -101

# print "states_set"
# print states_set

# print "Rewards Dictionary"
# print rewards_dict

# Action Function
def actions(state):
    # if state in terminal_location: # terminal_location is the terminal location of the car
    if state in [terminal_current]:
        return [None]
    else:
        return [(0, -1), (0,1), (1,0), (-1,0)]  # north, south, east, west
def turn_left(action):
    if action[0] == -1 and action[1] == 0:
        return (0,-1)
    elif action[0] == 0 and action[1] == -1:
        return (1,0)
    elif action[0] == 1 and action[1] == 0:
        return (0,1)
    elif action[0] == 0 and action[1] == 1:
        return (-1,0)

# go function
def go(state, action):
    state_new = tuple(map(operator.add, state, action)) # Adding two tuples of state and action in it

    if state_new in states_set: # Returning state_new if it exists in state_list
        return state_new
    else:
        return state # If new_state doesn't exist in states_list, then returning the original state

# Transition Function
def transition(state, action):
    if action is None:
        return [(0.0, state)]
    else:
        return [(0.7, go(state, action)),
                (0.1, go(state, turn_left(action))),
                (0.1, go(state, turn_left(turn_left(action)))),
                (0.1, go(state, turn_left(turn_left(turn_left(action)))))]

epsilon = 0.1
gamma = 0.9
def value_iteration():
    utility_dict = dict([(s, 0) for s in states_set])
    while True:
        utility_copy = utility_dict.copy()
        delta = 0
        for s in states_set:
            utility_dict[s] = rewards_dict[s] + gamma * max([sum([p * utility_copy[s1] for (p, s1) in transition(s, a)])
                                        for a in actions(s)])
            delta = max(delta, abs(utility_dict[s] - utility_copy[s]))
        if delta < epsilon * (1-gamma)/gamma:
             return utility_copy


def best_policy(utility_value):
    """Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action. (Equation 17.4)"""
    pi = {}
    for s in states_set:
        maxist = [expected_utility(a, s, utility_value) for a in actions(s)]
        # pi[s] = max(actions(s), lambda a:expected_utility(a, s, utility_copy))
        elem = max(maxist, key = lambda item:item[1])
        pi[s]=elem[0]
    return pi

def expected_utility(a, s, utility_copy):
    "The expected utility of doing a in state s, according to the MDP and U."
    if a is None:
        return None, None
    nextstate = go(s, a)
    return a, utility_copy[nextstate]



output_avgreward = [] # Output avg_reward value to be put in the output

for i in range(len(start_cars_list)):

    terminal_current = terminal_cars_list[i]
    rewards_dict[terminal_current] = 99

    # print "Value Iteration is:"
    utility_value = value_iteration()
    # print "Utility Value:"
    # print utility_value

    policies = best_policy(utility_value)
    # print policies

    total_reward = 0


    for j in range(10):
        pos = start_cars_list[i]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k=0
        reward = 0
        while pos != terminal_cars_list[i]:
            move = policies[pos]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_left(turn_left(move))
                    else:
                        move = turn_left(move)
                else:
                    move = turn_left(turn_left(turn_left(move)))
            pos = go(pos, move)
            reward += rewards_dict[pos]
            k+=1

        total_reward += reward

    avgreward = int(np.floor(total_reward/10))
    print avgreward
    output_avgreward.append(avgreward)

    rewards_dict[terminal_current] = -1

print "Output_avg_reward dictionary"
print output_avgreward

for elem in output_avgreward:
    if elem is output_avgreward[-1]:
        output.write(str(elem))
    else:
        output.write(str(elem) + '\n')

output.close()

print("%s seconds" % (time.time() - start_time)) # Printing execution time in seconds