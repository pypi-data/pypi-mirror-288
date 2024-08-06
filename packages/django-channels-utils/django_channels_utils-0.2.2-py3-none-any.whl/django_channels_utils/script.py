from abstract_consumer_handler import AbstractConsumerHandler





class MyHandler(AbstractConsumerHandler):
    
    def handle(self):
        print("handle")
        

class MyParentClass(MyHandler):
    pass
        



myHandler = MyParentClass()