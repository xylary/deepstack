'''
Created on 25 Jan 2018

@author: k
'''
class leductree(Tree):
    def _init_(self,data,children=None):
        self.data=data
        self.children=children
   
    def _str_(self):
        return(str(self.data))
    def add_data(self,extrainfo):
        self.data.append(extrainfo)
    def add_child(self,obj):
        self.children.append(obj)#will I have problems appending to none? 
    def givechildren(self):#function for outputting descendents of tree as children and appending them
        self.children=[]
        for c in options:
            self.add_child(leductree(self.data.append(c))
