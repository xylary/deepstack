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

class LeducNode(ExtensiveGameNode):
    """
    """
    def __init__(self,action_list,bets,raise_tuple,players_current_money):
        # Which player is to play in the node. Use -1 for terminal, 0 for
        # chance, 1 for player 1, 2 for player 2.
        
        self.player = current_player(action_list) #player 1 plays on even round and player 2 plays on odd rounds

        # A dictionary of children for the node. Keys are the actions in the
        # node, and values are ExtensiveGameNode objects resulting from taking
        # the action in this node.
        self.children = compute_children(action_list)
        

        # Who can see the actions in this node.
        self.hidden_from = [self.player%2+1]#automatically hidden from other player

        # Utility of the node to each player (as a dictionary). Only relevant
        # for terminal nodes.
        self.utility = {}
        
        #Dynamic calculation of bets - I am not sure if this needs to be done like this or instead the bets can be appended when children are made?
        self.bets= bets #from class Leduc 
        

        # If the node is a chance node, then store the chance probs. This is a
        # dictionary with keys the actions and probs the probability of choosing
        # this action.
        self.chance_probs = {}
        
        #encoded raise amount, do we need to have this in class data? Since it is uniform, i.e. never changes...
        self.raise_tuple=raise_tuple wit
        #amount of money each player has
        self.players_current_money=players_current_money
    
    def compute_round(self,action_list):#takes action_list and searches for double calls, round = number of double calls
        if not c in list(action_list):
            round=0
        else:
            for i in range(0,len(action_list)):
                if c in list(action_list[i:]):# if there is a call still
                   j =  list(action_list[i:]).index(c)
                   if list(action_list[j+1:]).index(c) = j+1:#searched for two calls in a row which signifies end of round
                       round = round + 1 #adds a round if there are two calls in a row
                       i = i+2
                    else:
                        i = i+1
                
                else:
                    i = len(action_list)#stop searching
        return round
    
    
    def current_player(self,action_list):
        
        if len(non_chance_action_list)%2 = 0:
            return 2
        else:
            return 1
    def raise_amount(self,action_list):
        return self.raise_tuple[compute_round(action_list)] #raise_uple will need to be a tuple which contains the bet amoutn for each round  that contains 
    
    
    
    def fold_child(self):       
        self.children.append(LeducNode(action_list +(f)))
    def call_child(self): 
        child_bets=bets(copy)
        child_current_players_money= current_players_money(copy)
        child_bets[self.player]=bets[self.player%2+1]
        child_current_players_money[self.player]=currentplayers_money[self.player]-bets[self.player%2+1+bets[self.player]
        
        self.children.append(LeducNode(action_list +(c),bets=child_bets,current_players_money)=child_current_players_money))
    def bet_child(self):
        child_bets=bets(copy)
        child_current_players_money= current_players_money(copy)
        child_bets[self.player]=bets[self.player]+raise_amount(action_list)
        child_current_players_money[self.player]=currentplayers_money[self.player]-raise_amount
        
        self.children.append(LeducNode(action_list +(c),bets=child_bets,current_players_money)=child_current_players_money))
    def twobet_child(self):
        child_bets=bets(copy)
        child_current_players_money= current_players_money(copy)
        child_bets[self.player]=bets[self.player]+2raise_amount(action_list)
        child_current_players_money[self.player]=currentplayers_money[self.player]-2raise_amount
        
        self.children.append(LeducNode(action_list +(c),bets=child_bets,current_players_money)=child_current_players_money))

    def allinchild(self):
        child_bets=bets(copy)
        child_current_players_money= current_players_money(copy)
        child_bets[self.player]=bets[self.player]+current_players_money[self.player]
        child_current_players_money[self.player]=0
        
        self.children.append(LeducNode(action_list +(c),bets=child_bets,current_players_money)=child_current_players))
        
    def compute_children_varied_bets(self,action_list):# variation on compute bets but with bets that can vary, still no consideration of players money, bets are now b= bet, 2b= 2x bet, ab = all-in
        if len(action_list)=0:#assign card to first player
            child_bets = {1:1,2:1}#both players pay ante
            for card in cards:
                
                self.children.append(LeducNode(action_list +(card),bets=child_bets))#not sure how to add probability to LeducNode that is child
        elif len(action_list)=1#assign card to 2nd player           
            cards_played= [x for i,x in enumerate(action_list) if i in cards]
            remaining_cards=[x for x in cards for x not in cards_played]
            for card in remaining_cards:
                self.children.append(LeducNode(action_list +(card)))
        elif compute_round>max_rounds #is terminal because we have reached end of game
            self.children={}#there are no children as game is finished
        elif action_list[len(action_list)]= [f] #is terminal because the previous player folded
            self.children={}#there are no children as game is finished
        elif action_list[len(action_list)-1:len(action_list)]= (c,c):#is chance node - we can ignore terminal round as this is covered in above
            if compute_round(action_history)=1:#this will be the flob
                cards_played= [x for i,x in enumerate(action_list) if i in cards]
                remaining_cards=[x for x in cards for x not in cards_played]
                for card in remaining_cards:
                    self.children.append(LeducNode(action_list +(card)))#provide flop (can actually work for n round with a flop at each round of course if #cards > max_rounds+1
        elif action_list[len(action_list)-4:len(action_list)]= (b,b,b,b):#have we reached bet limit
            fold_child()
        elif action_list[len(action_list)]= (2b) or action_list[len(action_list)-1]=(2b):#can't bet less than previous but'
            fold_child()
            call_child()
            bet_child()
            twobet_child()
            allin_child)()
        elif action_list[len(action_list)]= (ab)
            fold_child()
            call_child()
         
          
                               
        else:# not a chance node, betting is allowed so all available option (since you are always allowed to fold and call) NB: this allows for folding when there is no bet but a player can actually do this (it is a stupid move but...)
            fold_child()
            call_child()
            bet_child()
            twobet_child()
            allin_child)()
    