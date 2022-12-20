import selectors
import socket
import json
import pickle
import xml.etree.ElementTree as ET
from topicos import topic
from utils import XMLtoDict
from utils import dictToXML



HOST = ''                 
PORT = 8000

sel = selectors.DefaultSelector()

serializacoes = {} # dicionario com a informação do tipo de serialização de cada entidade
produtores = {} # dicionario com sockets de produtores e os topicos em que publicam
root = topic("/") # inicialização do tópico "/" 


def deserialize(conn, mensagem):
    """ descodifica a mensagem

        Parametros:
        mensagem: mensagem a ser descodificada
        conn: socket que enviou a mensagem
    """
    serial = serializacoes[conn] #tipo de serialização associada à socket

    if serial == 1: # JSON
        msg = mensagem.decode('utf-8')
        msg = json.loads(msg)
    elif serial == 3: # Pickle
        msg = pickle.loads(mensagem)
    else: # XML
        msg = XMLtoDict(mensagem)
    return msg



def serialize(conn, mensagem):
    """ codifica a mensagem

        Parametros:
        mensagem: mensagem a ser enviada
        conn: socket que envia a mensagem

    """
    serial = serializacoes[conn] # tipo de serialização associada à socket
    if serial == 1: # JSON
        msg = json.dumps(mensagem)
        msg = msg.encode('utf-8')
    elif serial == 3: # Pickle
        msg = pickle.dumps(mensagem)
    elif serial == 2: # XML
        msg = dictToXML(mensagem)

    return msg




def dumpsAndSend(conn, data):
    """ cria o cabeçalho para as mensagens e envia-as

        Parametros:
        conn: socket que envia a mensagem
        data: dados a ser enviados

    """
    dataSerial = serialize(conn, data)  # codifica  
    header = '{:05d}'.format(len(dataSerial)) # cria o cabeçalho
    conn.sendall(header.encode('utf-8')) # envia o cabeçalho
    conn.sendall(dataSerial) # envia a msg



def accept(sock, mask):
    """ aceita novas ligações

        Parametros:
        sock: socket do broker que recebe as ligações
        mask: mascara

    """
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)

    conn.setblocking(False) # impedir que bloqueie
    sel.register(conn, selectors.EVENT_READ,read) # registar a socket no selector



def publish(topic, value): # função para enviar publicações aos consumers
    """ envia publicações aos consumers

        Parametros:
        topic: topico onde é publicado
        value: valor da publicação

    """
    usersToSend = topic.getSubs() # consumers que devem receber a mensagem

    msg={'TOPIC':topic.getName(), 'VALUE': value}

    for c in usersToSend:
        dumpsAndSend(c, msg)

    topic.setLastMsg(msg) # guardar o ultima mensagem do tópico enviada


def closeSocket(conn):
    """ fecha a ligação e remove os dados associados

        Parametros:
        conn: socket do broker associada a uma determinada entidade

    """
    print('closing', conn) 
    del serializacoes[conn] # remove a informação do tipo de serialização
    if conn in produtores: 
        del produtores[conn] # remove a informação sobre em que tópico publicava 
    else:
        root.deleteFromTree(conn) # remove das listas de subscritores de um topico (e filhos)
    sel.unregister(conn)
    conn.close()


def read(conn, mask):
    """ lê eventos ocorridos

        Parametros:
        conn: socket associada a entidade que realizou o evento
        mask: mascara da socket

    """
    if conn not in serializacoes: # caso ainda não esteja registado
        serial = conn.recv(1) # tipo de serialização
        if serial:
            serial = int(serial)
            serializacoes[conn] = serial # associa o tipo de serialização ao socket
            return
        else:  # se não receber a informação sobre a serialização termina a socket
            closeSocket(conn)
            return

    tamanhoMsg = conn.recv(5) # recebe o cabeçalho
    if tamanhoMsg:
        tamanhoMsg = int(tamanhoMsg.decode('utf-8'))

        dataSerial = conn.recv(tamanhoMsg)

        if not dataSerial: # em caso de se desconectar
            closeSocket(conn)   
            return
        tamanhoDataSerial=len(dataSerial) 
        while(tamanhoDataSerial<tamanhoMsg): # garantir que a mensagem é lida toda até ao fim
            dataSerial=dataSerial+conn.recv(tamanhoMsg-tamanhoDataSerial)
            tamanhoDataSerial=len(dataSerial)

        data = deserialize(conn, dataSerial) # descodificar mensagem
        print("mensagem recebida: ", data)
        if data['OP'] == 'join': # registar
            t = root.getTopic(data['TOPIC']) # devolve o topico definido em data['TOPIC'] (se não existir devolve None)

            if data['TYPE'] == 1: # se for um consumer
                if not t is None: # se o tópico já existir
                    t.addSubs(conn) # adiciona o conusmer à lista de subscritores daquele topico (e à dos tópicos filhos)

                else: #se o topico ainda não tiver sido criado
                    t = root.insertTree(data['TOPIC']) # insere o topico na estrutura
                    t.addSubs(conn)# adiciona o consumer

                lastTopicMsgs = t.getAllLastMsgs() # retorna uma lista com a ultima mensagem publicada no topico, assim como a dos topios filho
                
                for msg in lastTopicMsgs:
                    dumpsAndSend(conn, msg) # envia essas ultimas mensagens

            else: # se for um producer

                if t is None: # se o tópico ainda não existir na árvore
                    t = root.insertTree(data['TOPIC']) # cria o tópico e insere na árvore

                produtores[conn] = t # adicona a socket do producer ao tópico correspondente


        elif data['OP'] == 'publish': # publicar
            if conn in produtores: #em principio é sempre verdade
                publish(produtores[conn], data['VALUE']) # publica


        elif data['OP'] == 'topics_request': # pedir a lista de topicos
            l = root.getList() # retorna a lista de todos os tópicos
            l = '\n'.join(l) # transforma a lista numa string com cada tópico separado por /n

            msg = {'OP' : 'topics_list', 'LIST' : l} # cria mensagem
            dumpsAndSend(conn, msg) # envia

        elif data['OP'] == 'leave_topic': # deixar de subscrever num topico
            root.deleteFromTree(conn) # retira a socket da lista de subscritores do topico e dos seus filhos

    else: # quando se desconectar
        closeSocket(conn)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # associa o endereço e a porta ao socket
    s.listen(100) # cria 1 fila de espera apenas para 1 ligação, enquanto um socket estiver a correr a outra fica na lista as outras são rejeitadas
    s.setblocking(False)
    sel.register(s,selectors.EVENT_READ,accept)

    while True: 
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

