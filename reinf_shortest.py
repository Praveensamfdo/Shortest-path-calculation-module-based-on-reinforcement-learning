#########################################################################
#                                                                       #
#   Shortest path routing module using Q-learning algorithm             #
#                                                                       #
#   Author  -   Praveen Fernando                                        #
#               Graduate Research Assistant                             #
#               Department of Electrical and Computer Engineering       #
#               University of Akron                                     #
#               330-319-0215 / psf8@zips.uakron.edu                     #
#                                                                       #
#########################################################################

"""

Functions implemented:

    1)add_node(a)
    2)remove_node(a)
    3)add_edge(a , b)
    4)remove_edge(a , b)
    5)shortest_path(a , b)
    6)print_graph()

"""
import numpy as np
import random
import time


class QlearnShortest():
    def __init__(self):
        self.nodes = {}  # key -> a certain node | value -> it's neighbours
        self.alpha = 0.7
        self.gamma = 1
        self.infinity = 1000
        self.episodes = 20

        self.decay_rate = 0.005  # Exponential decay rate for exploration prob

    def add_node(self, node):  # add a node to the graph
        if node not in self.nodes:
            self.nodes[node] = {}

        else:
            print("\nnode %s already added to the graph\n" % (node))

    def remove_node(self, node):
        try:
            del self.nodes[node]

        except:  # remove a node from the graph
            print("\nnode %s is not in the graph\n" % (node))

    def add_edge(self, edge_1, edge_2, weight):  # add an edge to the graph
        if edge_1 in self.nodes and edge_2 in self.nodes:
            if edge_2 not in self.nodes[edge_1] and edge_1 not in self.nodes[edge_2]:

                self.nodes[edge_1][edge_2] = weight
                self.nodes[edge_2][edge_1] = weight

            else:
                print("\nedge already added to the graph\n")

        else:
            print("\nthere are no sufficient nodes for the provided edge\n")

    def remove_edge(self, edge_1, edge_2):  # adding an edge
        if edge_1 in self.nodes and edge_2 in self.nodes:
            if edge_1 in self.nodes[edge_2] and edge_2 in self.nodes[edge_1]:
                self.nodes[edge_1].remove(edge_2)
                self.nodes[edge_2].remove(edge_1)

            else:
                print("\nthere is no link between %s and %s\n" % (edge_1, edge_2))

        else:
            print("\nyou are trying to remove an invalid edge\n")

    def print_graph(self):
        print(self.nodes)

    def calc_r_q(self, node_dict):  # based on the graph, initialize the reward and Q matrix
        num_states = len(node_dict)
        R = np.ones((num_states, num_states)) * self.infinity  # reward matrix shows the costs of the network.
        Q = np.ones((num_states, num_states)) * self.infinity  # Q matrix initialization
        action_array = []

        for key in node_dict:
            action_array.append(key)

        count = 0

        for state in node_dict:  # loop for calculating the R matrix
            for i in range(num_states):
                if action_array[i] in node_dict[state]:
                    R[count][i] = node_dict[state][action_array[i]]
                    Q[count][i] = 100

            count += 1

        return R, Q

    def calcshortest(self, start, goal):
        start_time = time.time()
        state_array = []

        for key in self.nodes:
            state_array.append(key)

        R, Q = self.calc_r_q(self.nodes)

        end_state = state_array.index(goal)
        counter = 0

        for episode in range(self.episodes):
            """
            In each episode, the agent will travel from start state to goal state and gain experience
            """
            current_state = state_array.index(start)
            self.epsilon = np.exp(-self.decay_rate * (counter))

            while True:
                current_state_row = Q[current_state,]
                available_actions = np.where(current_state_row != self.infinity)[0]

                if len(available_actions) == 1:
                    next_state = available_actions[0]


                else:  # epsilon-greedy
                    if random.random() < self.epsilon:  # randomly choose between available actions
                        next_state = random.choice(available_actions)

                    else:
                        next_state = random.choice(np.where(Q[current_state,] == min(Q[current_state,]))[0])  # randomly choose between the lowest cost actions

                Q[current_state, next_state] = Q[current_state, next_state] + self.alpha * (R[current_state, next_state] + self.gamma * min(Q[next_state,]) - Q[current_state, next_state])
                current_state = next_state

                counter += 1

                if next_state == end_state:
                    break

        steps = [state_array.index(start)]
        next_step = np.where(Q[state_array.index(start),] == np.min(Q[state_array.index(start),]))[0][0]
        steps.append(next_step)

        while next_step != end_state:
            next_step = np.where(Q[next_step,] == np.min(Q[next_step,]))[0][0]
            steps.append(next_step)

        converted_steps = []
        for j in steps:
            converted_steps.append(state_array[j])

        end_time = time.time()
        conv_time = round(((end_time - start_time) * 1000), 3)

        return converted_steps, np.round(Q), conv_time, R

