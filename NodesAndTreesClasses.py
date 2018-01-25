'''
Created on 19 Jan 2018

@author: k
'''


    
class Tree:   
    def _init_(self,data,children=[]):
        self.data=data
        self.children=children
   
    def _str_(self):
        return(str(self.data))
    def add_data(self,extrainfo):
        self.data.append(extrainfo)
    def add_child(self,obj):
        self.children.append(obj)
    def givechildren(self):#function for outputting descendents of tree as list and linking them
        pass
    


    

def depth_children(n,tree):
        if n=0:
            return tree#returns current tree if depth =0
        if n=1:
             return tree.children#returns children when count gets to 1
        else:
            children=[]#list of children at ith level
            for c in tree.children:
                children.append(depth_children(n-1,c)) #makes children a list of ith descendents
            return children#I don't think this is in the right place

def buildtree(roottree,depth):
    
    for i = (0,depth):#builds down at each level
        for d in depth_children(i,roottree):#enumerates the ith descendents as a list
            d.givechildren
    
    
class Treeattempt: #my first attempt at tree -  - the advantage may be that we have explicit edges.
    def __init__(self,rootnode,depth):
       
        self.nodes(0)=rootnode
        if  i (1,depth):
            for currentnode in nodes(i-1):
                
                for child in currentmode.givechildren:
                    self.nodes(i)=self.nodes(i).append(child)
                    self.edges=self.edges,append((currentnode,child)
        
    def writenode(self, node):
        self.nodes=self.nodes.append((node))
    
    def writeedge(self,node1,node2):
        self.edges= self.edges.append([node1,node2])

class nodeold():#I think that we don't need nodes in this idea of tree - as trees hold place and direct descendents and then tree is also collections of trees defined recursively
  
    def __init__(self, params):
        
        Constructor
        '''        self.data= "no data yet"
        
    def givechildren(node):
        pass