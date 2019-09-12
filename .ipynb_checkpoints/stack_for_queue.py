
class Stack(object):
    def __init__(self):
        self.queue1 = []
        self.queue2 = []
    def enstack(self,item):
        self.queue1.append(item)

    def qnstack(self):
        #弹出时，把队列1中元素取出到只剩一个为止，放到队里2中
        #队列1和2交换为止
        #弹出队列2中的元素
        if len(self.queue1) == 0:
            return None
        while len(self.queue1)!=1:
            self.queue2.append(self.queue1.pop(0))
        self.queue1,self.queue2= self.queue2,self.queue1
        return self.queue2.pop(0)

if __name__ == "__main__":
    stack = Stack()
    stack.enstack(1)
    stack.enstack(2)
    stack.enstack(3)
    print(stack.qnstack())
    stack.enstack(7)
    stack.enstack(4)
    stack.enstack(5)
    print(stack.qnstack())
    print(stack.qnstack())
    print(stack.qnstack())
    print(stack.qnstack())
    print(stack.qnstack())


