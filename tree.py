
from utils import strToList

class node:
    def __init__(self,value,parent=None,camada=1,lastTopic=None):
        self.__value=value
        self.__children=set()
        self.__parent=parent
        self.__camada=camada
        self.__sockets=set()
        self.__lastTopic=lastTopic

    @property
    def value(self):
        return self.__value

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def camada(self):
        return self.__camada

    @property
    def sockets(self):
        return self.__sockets

    @property
    def lastTopic(self):
        return self.__lastTopic
    

    def isChild(self,value):
        for child in self.children:
            if child.value==value:
                return True
        
        return False

    def getChild(self,value):
        for child in self.children:
            if(child.value==value):
                return child

    def addLastTopic(self,msg):
        self.__lastTopic=msg

    def constructValue(self,topic):

        if self.value=="/":
            return self.value+ topic
        else:
            return self.value+"/"+topic


    def getNode(self,value):# depth-first
        # print(self.value)
        if(self.value==value):
            return self
        if( self.children):
            
            for c in self.children:
                
                x=c.getNode(value)
                if x:
                    return x
    
    def getNodev2(self,camada,value):
        
        if(camada==self.camada+1):
            for no in self.children:
                if value==no.value:
                    return no
            return
        else:
            for child in self.children:
                node=child.getNodev2(camada,value)
                if node:
                    return node
        

    def addSocket(self,conn):
        self.sockets.add(conn)

    def removeSocket(self,conn):
        self.sockets.remove(conn)

    def insert(self,value,parent,camada): # /temp/1
        n=node(value,parent,camada)
        self.children.add(n)
        return n

    def addNode(self,topic):
        # print(topic)

        if len(topic)==0:
            print(self)
            return self
        

        if (not self.children):
            childvalue=self.constructValue(topic[0])
            # print(childvalue)
            # print(type(topic[0]))
            child=self.insert(childvalue,self,self.camada+1)
            
            return child.addNode(topic[1:len(topic)])
            
        else: 
            # print(topic[0])
            childvalue=self.constructValue(topic[0])
            if self.isChild(childvalue):
                child=self.getChild(childvalue)
                return child.addNode(topic[1:len(topic)])
        
            else:
                # childvalue=str(self.value()) + str(topic[0])
                
                child=self.insert(childvalue,self,self.camada+1)
                
                return child.addNode(topic[1:len(topic)])



    def transverse(self):
        print(self.value)
        if not self.children:
            return

        for child in self.children:
            child.transverse()
            




    def RemoveNode(self,node):
        self.children.remove(node)

            

    def __str__(self):
        return self.value

    def getChildren(self,set):

        if not self.children: 

            return set

        for child in self.children:
            
            set.add(child) 
            child.getChildren(set)

        return set
    
    def getParent(self,parentSet):
        
        if self.camada==1:
            
            return parentSet

        parentSet.add(self.parent)

        return self.parent.getParent(parentSet)
    
        



