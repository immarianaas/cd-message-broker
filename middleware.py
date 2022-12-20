from enum import IntEnum
import socket
import json
import pickle
import xml.etree.ElementTree as ET
from utils import XMLtoDict
from utils import dictToXML


class SerializationType(IntEnum): # enum com os tipos de serialização
    JSON=1
    XML=2
    PICKLE=3


class MiddlewareType(IntEnum):# enum para endentificar o tipo de entidades
    CONSUMER = 1
    PRODUCER = 2

class Queue:
    HOST = 'localhost'
    PORT = 8000
    
    def __del__(self):
        """Destruição da Queue"""

        print('closing socket')
        self.socket.close() # termina a ligação

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        """Construtor

            Parametros:
            topic: topico associado à Queue
            type: tipo de entidade que contém a Queue

        """
        self.topic = topic
        self.type = type
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# regista a socket 
        self.socket.connect((self.HOST, self.PORT))# tenta ligar-se


    def push(self, value): # publicação
        """ Sends data to broker. """

        header = '{:05d}'.format(len(value)) #cabeçalho com o tmanho da msg
        self.socket.sendall(header.encode()+value) # envia o cabeçalho e a mensagem


    def pull(self): 
        """ recebe dados do broker"""

        tamanhoMsg = self.socket.recv(5)  # recebe o tamanho da msg

        tamanhoMsg = int(tamanhoMsg.decode('utf-8')) # descodifica o cabeçalho

        dataSerial = self.socket.recv(tamanhoMsg)  # recebe a msg 

        tamanhoDataSerial=len(dataSerial) # garantir que a msg é lida toda até ao fim
        while(tamanhoDataSerial<tamanhoMsg):
            dataSerial=dataSerial+self.socket.recv(tamanhoMsg-tamanhoDataSerial)
            tamanhoDataSerial=len(dataSerial)

        return dataSerial


    def getJoinTopicMsg(self):
        """retorna uma msg para informar o broker que quer participar no processo """
        return {'OP': 'join', 'TOPIC': self.topic, 'TYPE': int(self.type)}


    def getPublishMsg(self, value):
        """ retorna uma msg de publicação """
        return {'OP': 'publish', 'VALUE': value}

    
    def getTopicsListMsg(self):
        """retorna msg de pedido da lista de tópicos """
        return {'OP': 'topics_request'}
    
    
    def getLeaveMsg(self):
        """ retorna msg de cancelamento de subscrição de determinado topico """
        return {'OP' : 'leave_topic'}


        


class JSONQueue(Queue):
    serial = SerializationType.JSON

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        super().__init__(topic, type)
        ser = '{:1d}'.format(int(self.serial)) # enviar o tipo de serializacao
        self.socket.sendall(ser.encode('utf-8'))
        mensagem = super().getJoinTopicMsg() # pede mensagem de join
        mensagem = json.dumps(mensagem) # converte a msg para JSON
        msgReady = mensagem.encode('utf-8')
        super().push(msgReady) # envia a msg para o broker
    
    def push(self, value):
        msg = super().getPublishMsg(value)
        msgReady = json.dumps(msg) 
        msgReady = msgReady.encode('utf-8')
        super().push(msgReady)

    def pull(self):
        dataSerial = super().pull() # recebe dados do broker
        data = dataSerial.decode('utf-8')
        data = json.loads(data) # descodifca a mensagem

        if 'LIST' in data: # se receber a lista de topicos
            return None, data['LIST']

        return data['TOPIC'], data['VALUE']

    def getTopicsList(self):
        mensagem = super().getTopicsListMsg()
        msgJSON = json.dumps(mensagem)
        msgReady = msgJSON.encode('utf-8')
        super().push(msgReady)
    
    def leaveTopic(self):
        mensagem = super().getLeaveMsg()
        msgJSON = json.dumps(mensagem)
        msgReady = msgJSON.encode('utf-8')
        super().push(msgReady)

# -----------------------------------------------------------------------------

class XMLQueue(Queue):
    serial = SerializationType.XML

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        super().__init__(topic, type)
        ser = '{:1d}'.format(int(self.serial)) # enviar o tipo de serializacao
        self.socket.sendall(ser.encode('utf-8'))
        mensagem = super().getJoinTopicMsg()
        mensagemXML = dictToXML(mensagem) # codifica a msg para XML
        super().push(mensagemXML) # envia a msg para o broker


    def push(self, value):

        msg = super().getPublishMsg(value)
        msgReady = dictToXML(msg)
        super().push(msgReady)

    def pull(self):
        dataSerial = super().pull()
        data = XMLtoDict(dataSerial) # descodifica
        if 'LIST' in data: # recebe a lista de topicos
            return None, data['LIST']
        return data['TOPIC'], data['VALUE']

    def getTopicsList(self):
        mensagem = super().getTopicsListMsg()
        msgReady = dictToXML(mensagem)
        super().push(msgReady) # cria o header e envia     

    def leaveTopic(self):
        mensagem = super().getLeaveMsg()
        msgReady = dictToXML(mensagem)
        super().push(msgReady)

# -----------------------------------------------------------------------------

class PickleQueue(Queue):
    serial = SerializationType.PICKLE

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        super().__init__(topic, type)
        ser = '{:1d}'.format(int(self.serial)) # enviar o tipo de serializacao
        self.socket.sendall(ser.encode('utf-8'))
        mensagem = super().getJoinTopicMsg()
        msgReady = pickle.dumps(mensagem)
        super().push(msgReady)

    def push(self, value):
        msg = super().getPublishMsg(value)
        msgReady = pickle.dumps(msg) 
        super().push(msgReady)

    
    def pull(self):
        dataSerial = super().pull()
        data = pickle.loads(dataSerial)
        if 'LIST' in data:
            return None, data['LIST']
        return data['TOPIC'], data['VALUE']
        

    def getTopicsList(self):
        mensagem = super().getTopicsListMsg()
        msgReady = pickle.dumps(mensagem)
        super().push(msgReady)      

    def leaveTopic(self):
        mensagem = super().getLeaveMsg()
        msgReady = pickle.dumps(mensagem)
        super().push(msgReady)



