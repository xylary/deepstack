'''
Created on 30 Jan 2018

@author: k
'''
from extensive_game import ExtensiveGame, ExtensiveGameNode
from example_strategy import random_strategy, constant_action
from best_response import best_response
import numpy as np
from leduc import Leduc
from binascii import a2b_base64

#Leduc is example of ExtensiveGame which by my understanding has to build from the game root 
#This module is to work on a specific function for Leduc which given any node will calculate the possible actions (children)
#every node contains the history none as action_list

global cards 
cards = ('k','k','q','q','j','j') #I run in to errors if I have multiplicities in my cards, something to do with setminus


class LeducNode(ExtensiveGameNode):
    """
    """
    def __init__(self,action_list,bets,raise_tuple):
        #history of actions as a tuple
        self.action_list=action_list
        # Which player is to play in the node. Use -1 for terminal, 0 for
        # chance, 1 for player 1, 2 for player 2.
        
        self.player = self.current_player() #player 1 plays on even round and player 2 plays on odd rounds

        # A dictionary of children for the node. Keys are the actions in the
        # node, and values are ExtensiveGameNode objects resulting from taking
        # the action in this node.
        self.children = {}#make this a dictionary
        

        # Who can see the actions in this node.
        self.hidden_from = [self.player%2+1]#automatically hidden from other player

      
        # for terminal nodes.
        self.utility = {}
        
        #Dynamic calculation of bets - I am not sure if this needs to be done like this or instead the bets can be appended when children are made?
        self.bets= bets #from class Leduc 
        

        # If the node is a chance node, then store the chance probs. This is a
        # dictionary with keys the actions and probs the probability of choosing
        # this action.
        self.chance_probs = {}
        
        #encoded raise amount, do we need to have this in class data? Since it is uniform, i.e. never changes...
        self.raise_tuple=raise_tuple 
        #amount of money each player has
       
    
    def compute_round(self):#takes action_list and searches for double calls, round = number of double calls
        
        round=0
        
        for i in range(0,len(self.action_list)):
            if self.action_list[i:i+2] ==('c','c'): # if there is a call still
                round = round + 1 #adds a round if there are two calls in a row
            elif self.action_list[i:i+2]==('b','c'):
                round = round +1        
        return round
    
    
    def current_player(self):
        non_chance_action_list = [x for x in enumerate(self.action_list) if x not in cards]
        if len(non_chance_action_list)%2 == 0:
            return 2
        else:
            return 1
    def raise_amount(self):
        return self.raise_tuple[self.compute_round()] #raise_tuple will need to be a tuple which contains the bet amoutn for each round  that contains 
    
    
    
    def fold_child(self):       
        self.children['f'] = LeducNode(action_list=self.action_list +('f',),bets=self.bets,raise_tuple=self.raise_tuple)
    def call_child(self):
        child_bets=self.bets.copy()

        child_bets[self.player]=self.bets[self.player%2+1]
        
        self.children['c']=LeducNode(action_list=self.action_list +('c',),bets=child_bets,raise_tuple=self.raise_tuple)
    def bet_child(self):
        child_bets=self.bets.copy()
        
        child_bets[self.player]=self.bets[(self.player)%2+1]
        child_bets[self.player]=child_bets[self.player]+self.raise_amount()
        
        
        self.children['b']=LeducNode(action_list=self.action_list +('b',),bets=child_bets,raise_tuple=self.raise_tuple)
    

    
    def compute_children(self):# variation on compute bets but with bets that can vary, still no consideration of players money, bets are now b= bet, 2b= 2x bet, ab = all-in
        if len(self.action_list)==0:#assign card to first player
            self.child_bets = {1:1,2:1}#both players pay ante
            for card in cards:
                self.children[card]=LeducNode(action_list=self.action_list + (card,),bets=self.child_bets,raise_tuple=self.raise_tuple)#not sure how to add probability to LeducNode that is child
        elif len(self.action_list)==1:#assign card to 2nd player           
            cards_played= (x for x in self.action_list if x in cards)
            remaining_cards=[x for x in cards if x not in cards_played]
            print cards_played
            print remaining_cards
            for card in remaining_cards:
                self.children[card]=LeducNode(self.action_list +(card,),bets=self.bets,raise_tuple=self.raise_tuple)
        elif self.compute_round()>min(len(self.raise_tuple),len(cards)-2): #is terminal because we have reached end of game
            self.children={}#there are no children as game is finished
        elif self.action_list[-1]== ('f'): #is terminal because the previous player folded
            self.children={}#there are no children as game is finished
        elif self.action_list[-2:]== ('c','c') or self.action_list[-2:]==('b','c'):#is chance node - we can ignore terminal round as this is covered in above
            if self.compute_round()<=len(self.raise_tuple):#this will be the flop
                cards_played= (x for x in self.action_list if x in cards)
                remaining_cards=[x for x in cards if x not in cards_played]
                for card in remaining_cards:
                    self.children[card]=LeducNode(self.action_list +(card,),bets=self.bets,raise_tuple=self.raise_tuple)#provide flop (can actually work for n round with a flop at each round of course if #cards > max_rounds+1
        elif self.action_list[-4:]== ('b','b','b','b'):#have we reached bet limit
            self.fold_child()
            self.call_child()
        else:# not a chance node, betting is allowed so all available option (since you are always allowed to fold and call) NB: this allows for folding when there is no bet but a player can actually do this (it is a stupid move but...)
            self.fold_child()
            self.call_child()
            self.bet_child()
        
        
    @staticmethod
    def print_tree_recursive(node,depth,only_leafs):
        """ Prints out a list of all nodes in the tree rooted at 'node'.
        """
        if depth ==0:
            return
            #print'finished printing'
        else:
            node.compute_children()
            if only_leafs == True: 
                if node.children=={}:
                    print(node.action_list)
        
            else:
                print(node.action_list)
                print(node.bets)
            
            for label,child in node.children.items():
                LeducNode.print_tree_recursive(child,depth-1,only_leafs)
            
            
root=LeducNode(action_list=(),bets={},raise_tuple=(2,4))

print root

#root.print_tree_recursive(root,20)

longroot=LeducNode(action_list=('k','k'),bets={1:1,2:1},raise_tuple=(2,4,6))

longroot.print_tree_recursive(longroot,4,only_leafs=False)


