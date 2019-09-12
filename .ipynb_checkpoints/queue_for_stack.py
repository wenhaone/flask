
def queue_for_stack():
    stack1 = []
    stack2 = []


class Queue(object):
    def __init__(self):
        self.stack1 = []
        self.stack2 = []
    def enqueue(self,item):
        self.item =item
        self.stack1.append( self.item)

    def qnqueue(self):
        if self.stack2 :
            return self.stack2.pop()
        elif self.stack1:
            while self.stack1:
                self.stack2.append( self.stack1.pop())
            return  self.stack2.pop()
        else:
            return None
    def is_empty(self):
        return  not (self.stack1 or self.stack2)
if __name__=="__main__":
    queue1 = Queue()
    queue1.enqueue(1)
    queue1.enqueue(2)
    queue1.enqueue(3)
    queue1.enqueue(4)
    queue1.enqueue(5)
    print(queue1.qnqueue())
    print(queue1.qnqueue())
    print(queue1.qnqueue())
    print(queue1.qnqueue())
    print(queue1.qnqueue())
 






