'''
Module Name : PythonDSA
Created By  : Ankit Chandok
Website     : https://codexstudios.pythonanywhere.com
Contact Us  : codexstudios@gmail.com,codexcodespace@gmail.com
'''
#########################################################################################################################################
class MyError(Exception):
	# Constructor or Initializer
	def __init__(self, value):
		self.value = value
	# __str__ is to print() the value
	def __str__(self):
		return(repr(self.value))
def ERROR(func,x):
    raise func(x)
class Stack(Exception):
    def __init__(self,stack,size=10):
            self.stack = stack
            self.__size = size
            self.__errors = {
                'NI' : 'Not Implemented',
                'OverFlow' : 'Sorry , Stack OverFlow 😊 .',
                'UnderFlow' : 'Sorry , Stack is Empty 😊 .',
                'ChangeSize' : 'Sorry , The Stack will be OverFlow by Doing This So Not Implemented  😊 .'
            }
    def push(self,value,ThrowERROR=False):
        if (self.__size == len(self.stack)):
            if (ThrowERROR):
                ERROR(Stack,self.__errors['OverFlow'])
            else:
                return print(self.__errors['OverFlow'])
        else:
            try:
                self.stack.append(value)
            except:
                if (ThrowERROR):
                    ERROR(Stack,self.__errors['NI'])
                else:
                    print(self.__errors['NI'])
    def pop(self,tell=None,ThrowERROR=False):
        try:
            if tell:
                if (tell.lower()=='return'):
                    return self.stack.pop()
                elif (tell.lower()=='tell'):
                    print(f'The Item Removed From Stack is {self.stack.pop()}')
            else:
                self.stack.pop()
        except:
            if (ThrowERROR):
                ERROR(Stack,self.__errors['UnderFlow'])
            else:
                print(self.__errors['UnderFlow'])
    def peek(self,Return=None,ThrowERROR=False):
        try:
            if (Return==None):
                print(f'The Peek Item in The Stack is {self.stack[-1]}')
                return self.stack[-1]
            elif (Return):
                return self.stack[-1]
            else:
                print(f'The Peek Item in The Stack is {self.stack[-1]}')
        except:
            if (ThrowERROR):
                ERROR(Stack,self.__errors['UnderFlow'])
            else:
                print(self.__errors['UnderFlow'])
    def IsEmpty(self):
        if (self.stack==[]):
            return True
        else:
            return False
    def IsFull(self):
        if (len(self.stack == self.__size)):
            return True
        else:
            False
    def OfSize(self):
        return len(self.stack)
    def MaxSize(self,Return=None):
        if (Return):
            return self.__size
        else:
            print(f'Max Size Allocated to this Stack is {self.__size} 😊 .')
    def SpaceLeft(self,Return=None):
        if (Return):
            return (self.__size - len(self.stack))
        else:
            print(f'The Space Left to Add Items in this Stack is {(self.__size - len(self.stack))} 😊 .')
    def ChangeSize(self,size):
        if (size > len(self.stack)):
            self.__size = size
        else:
            print(self.__errors['ChangeSize'])
    def ClearStack(self):
        self.stack = []

class Queue():
    pass

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.start = None
    def viewList(self):
        if self.start == None:
            print('List is Empty .')
        else:
            temp = self.start
            while temp != None:
                print(temp.data,end=' ')
                temp = temp.next
    def deleteFirst(self):
        if self.start == None:
            print('Linked List is Empty .')
        else:
            self.start = self.start.next
    def insertFirst(self,value):
        FirstNode = value
        self.start = Node(FirstNode,self.start)
    def insertLast(self,value):
        newNode = Node(value)
        if self.start == None:
            self.start = newNode
        else:
            temp = self.start
            while temp.next != None:
                temp = temp.next
            temp.next = newNode
##################################################################################
