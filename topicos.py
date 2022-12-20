class topic:
    def __init__(self, name):
        """Construtor

        Parametros:
        name: nome do tópico
        
        """
        self._name = name
        self._topicosFilho = [] # lista dos topicos filhos
        self._subscritos = set() # set de subscritores (sockets) do tópico
        self._lastMsg = None # ultima msg publicada no tópico
        self._pai = None # topico pai do tópico

    def addFilho(self, topico):
        """ adiciona um novo tópico à lista dos tópicos filho

            Parametros:
            topico: topico (filho) a ser adicionado

        """
        self._topicosFilho.append(topico)
        for sub in self._subscritos:
            topico.addSubs(sub) # filhos herdam subscritores dos pais
        


    def addSubs(self, conn):
        """ adiciona um consumer a lista de subscritores do topico

            Parametros:
            conn: socket que representa o consumer (subscritor)

        """
        self._subscritos.add(conn) 
        for t in self._topicosFilho:
            t.addSubs(conn) # filhos herdam subscritores dos pais


    def getSubs(self):
        """ retorna o set de subscritores do tópico """
        return self._subscritos

    def getName(self):
        """ retorna o nome do tópico """
        return self._name

    def getPai(self):
        """ retorna o topico pai do topico """
        return self._pai

    def setLastMsg(self, value):
        """ guarda/define a ultima msg publicada no tópico

            Parametros:
            value: valor da msg

        """
        self._lastMsg = value    



    def getAllLastMsgs(self):
        """ retorna uma lista da ultmima msg publicada no topico, incluindo nos filhos """
        if not self._lastMsg == None:
            list = [self._lastMsg]
        else:
            list = []
        for t in self._topicosFilho:
            list = list + t.getAllLastMsgs()
        return list


    def getLastMsg(self):
        """ retorna a ultima msg publicada no topico """
        return self._lastMsg  #devolve None se n exisitr 


    def getTopic(self, name): 
        """ devolve um tópico (ou None se este não exisitir)

            Parametros:
            name: nome do tópico que queremos receber

        """
        if self._name == name: # caso encontre
            return self

        for t in self._topicosFilho:# se não procura nos tópicos filho

            resp = t.getTopic(name)
            if not resp is None:
                return resp
        return None # se não tiver sido encontrado (não existe)



        
    def insertTree(self, nome, temp=""): # string
        """ insere um tópico na estrutura(arvore)

            Parametros:
            nome: nome do tópico a ser inserido

        """
        if self._name == nome:
            return self
        
        l_nome = nome.split("/") # separar o nome do topico por "/"
        l_temp = temp.split("/") # separar o nome do topico temporario (pais dos pais/etc) por "/"

        if ( not len(nome) == len(temp) ):
            temp += "/" + l_nome[len(l_temp)] # adicionar o nome de um filho ao topico temporario

        for filho in self._topicosFilho:
            if filho.getName() == temp:
                return filho.insertTree(nome, temp) # inserir na arvore esse filho se o pai for este topico
            
        # se não houver nenhum filho == temp
        t = topic(temp)
        self.addFilho( t ) # adicionar a este tópico

        if (not len(nome) == len(temp)):
            l_temp = temp.split("/")
            temp += "/" + l_nome[len(l_temp)] # adicionar o nome de um filho ao topico temporario
            return t.insertTree(nome, temp)
        else:
            return t # retorna esse tópico

    def setPai(self, pai):
        """define o tópico pai

            Parametros:
            pai: topico pai

        """
        self._pai = pai
        self._subscritos.update( pai.getSubs())


    def deleteFromTree(self, c):
        """ remove um subscritor da lista de subscritores de um topico

            Parametros:
            c: subscritor a ser removido

        """
        if c in self._subscritos:
            self._subscritos.remove(c)
        for t in self._topicosFilho: # como os filhos herdam os subscritores dos pais
            t.deleteFromTree(c)

    def __str__(self):
        return"Tópico: " + self._name

    def imprimir(self):
        """ imprime todos os topicos contidos na estrutura"""
        print(self)
        for t in self._topicosFilho:
            t.imprimir()


    def getList(self):
        """ devolve a toda a descendencia de um topico incluindo o prorio """
        list = [self._name]
        for t in self._topicosFilho:
            list = list + t.getList()
        return list
