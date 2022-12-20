import sys
import argparse
import middleware

class Consumer:
    def __init__(self, datatype):
        self.type = datatype
        self.queue = middleware.JSONQueue(f"/{self.type}")
        # self.queue = middleware.PickleQueue("/")
        
    @classmethod
    def datatypes(self):
        return ["temp", "msg", "weather"]    

    def run(self, length=10):
        i = 15
        
        while True:
            
            # if i == 0: # deixa de subscrever o topico
            #     self.queue.leaveTopic()
            #     print("já saiu!")

            if i == 10: # pede a lista de tópicos
                self.queue.getTopicsList()

            topic, data = self.queue.pull()
            if topic == None: # para receber a lista de topicos
                print("\nLista de tópicos presentes no broker: ")
                print(data) 
                print()
                
            else:
                print(topic, data)
            i -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="type of producer: [temp, msg, weather]", default="temp")
    args = parser.parse_args()

    if args.type not in Consumer.datatypes():
        print("Error: not a valid producer type")
        sys.exit(1)

    p = Consumer(args.type)
    
    p.run()
