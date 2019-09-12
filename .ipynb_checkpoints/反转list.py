
"""写程序把一个单向链表顺序倒过来（尽可能写出更多的实现方法，标出所写方法
的空间和时间复杂度）"""

class Node(object):
    def __init__(self,item):
        self.item = item
        self.next = None
#第一种方法：
def loopList(node):
    while node.next != None:
        node.next.next = node
        node=node.next
#利用三个指针逐个反转
def f1(head):
    p = head
    q = head.next

