import xml.etree.ElementTree as ET

def XMLtoDict(xml):
    """ decodifica uma msg xml

    Parametros: 
    xml:msg xml a ser descodificada

    """
    msg = {}
    parser = ET.XMLPullParser(['start', 'end']) # nãl bloqueante
    parser.feed(xml)
    for event,elem in parser.read_events():
        if(elem.tag!='data'):
            if (str(elem.text).isnumeric()):
                elem.text = int(elem.text)
            msg[elem.tag]=elem.text
    return msg


def dictToXML(dict):
    """ codifica uma msg em xml

        Parametros:
        dict:msg(dicionario) a ser codificada

    """
    mensagem = ET.Element('data'); # root

    for key, val in dict.items():
        child = ET.Element(key)
        child.text = str(val)
        mensagem.append(child)

    return ET.tostring(mensagem)