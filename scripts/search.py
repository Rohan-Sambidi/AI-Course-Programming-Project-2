#!/usr/bin/env python3
# encoding: utf-8

__copyright__ = "Copyright 2021, AAIR Lab, ASU"
__authors__ = ["Naman Shah", "Rushang Karia"]
__credits__ = ["Siddharth Srivastava"]
__license__ = "MIT"
__version__ = "1.0"
__maintainers__ = [ "Naman Shah"]
__contact__ = "aair.lab@asu.edu"
__docformat__ = 'reStructuredText'

import problem 
import rospy
from std_msgs.msg import String
import argparse
from evaluate import compute_g
from evaluate import compute_h
from node import Node
import os
from priority_queue import PriorityQueue
import subprocess
import time
from utils import initialize_ros
from utils import cleanup_ros

SUBMIT_FILENAME = "hw1_results.csv"
SUBMIT_SEARCH_TIME_LIMIT = 300

class SearchTimeOutError(Exception):

    pass

def is_invalid(state):
    """
        Parameters
        ===========
            state: State
                The state to be checked.
                
        Returns
        ========
            bool
                True if the state is invalid, False otherwise.
    """
    
    return state.x == -1 or state.y == -1

def build_solution(best_path, current_node):
    """
        Builds the solution from the best path recorded.
        
        Parameters
        ===========
            
            best_path: dict
                A map of state -> node representing the best path.
            current_node: Node
                The current node from which the path is to be recorded.
                
        Returns
        ========
            list
                A list of the actions that will lead from the initial state to
                the state represented by the current_node.
    """
    
    action_list = []
    
    # Iterate all the way until the parent.
    # The initial node's parent pointer will be None so we only check till we
    # reach the initial state.
    while current_node.get_parent() is not None:
    
        current_state = current_node.get_state()
        action_list.append(current_node.get_action())
        
        # Consult the map to get the next for the next state (in reverse order).
        current_node = best_path[current_state]
        
    # Since we went bottom-up, to ensure actions are executable, we need to 
    # reverse the action_list.
    #
    # Python's list.reverse() reverses in-place.
    action_list.reverse()
    
    return action_list

def search(init_state, goal_state, helper, algorithm, time_limit=float("inf")):
    """
        Performs a search using the specified algorithm.
        
        Parameters
        ===========
            algorithm: str
                The algorithm to be used for searching.
            time_limit: int
                The time limit in seconds to run this method for.
                
        Returns
        ========
            tuple(list, int)
                A tuple of the action_list and the total number of nodes
                expanded.
    """
    
    # Initialize the g_score map, we use this map to keep a track of the
    # shortest path to a state that we have observed.
    #
    # This map stores data of the form state -> int.
    g_score = {}
    g_score[init_state] = 0

    # Initialize a map to store the best path to a state.
    #
    # This map stores data of the form state -> Node.
    best_path = {}
    best_path[init_state] = None
    
    # Initialize the init node of the search tree and compute its f_score.
    init_node = Node(init_state, None, 0, None, 0)
    f_score = compute_g(algorithm, init_node, goal_state) \
        + compute_h(algorithm, init_node, goal_state)
    
    # Initialize the fringe as a priority queue.
    priority_queue = PriorityQueue()
    priority_queue.push(f_score, init_node)
    
    action_list = None
    total_nodes_expanded = 0
    time_limit = time.time() + time_limit

    while not priority_queue.is_empty() and time.time() < time_limit:
    
        # Pop the node with the smallest f_score from the fringe.
        current_node = priority_queue.pop()
        current_state = current_node.get_state()
        
        # If the current state is a goal state, we are done and need to
        # reconstruct the best path to the goal.
        if helper.is_goal_state(current_state, goal_state):
        
            action_list = build_solution(best_path, current_node)
            break

        # Expand the node.
        total_nodes_expanded += 1
        action_state_dict = helper.get_successor(current_state)
        
        for action, state in action_state_dict.items():

            # The successor function actually stores items in the
            # action -> (next_state, cost) format.
            next_state, action_cost = state
            
            # Only process valid states.
            if is_invalid(next_state):
            
                continue
            
            next_node = Node(next_state,
                current_node,
                current_node.get_depth() + 1,
                action,
                action_cost)
                
            g_value = compute_g(algorithm, next_node, goal_state)
            
            # If a cheaper path is found to the next_state, then we can
            # add the next_state to the fringe.
            if g_value < g_score.get(next_state, float("inf")):
            
                # Remember the cheaper path to the next_state from the
                # current_state/current_node.
                #
                # We need the node since we want to remember the action as well.
                best_path[next_state] = current_node
            
                # Remember the cheaper path cost.
                g_score[next_state] = g_value
                
                # Compute the f-value and add to the fringe (unless it is
                # already there).
                f_score = g_value + compute_h(algorithm, next_node, goal_state)
                if not priority_queue.contains(next_state):
                
                    priority_queue.push(f_score, next_node)

    if time.time() >= time_limit:
    
        raise SearchTimeOutError("Search timed out after %u secs." % (time_limit))

    return action_list, total_nodes_expanded
