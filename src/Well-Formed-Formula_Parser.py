#**********************************************************************************************************************
#CSC 442: Artificial Intelligence
#Code designed to convert well-formed-formula strings into a postfix tree
#Author: Rich Magnotti (netid: rmagnott@ur.rochester.edu)
#**********************************************************************************************************************
from CNF_Converter import toCNF
from Data_Structs import Queue
from Data_Structs import Stack
from Data_Structs import ExpTree
#grammar:
#     sentence ::= letter
#     expression ::= '(' expression ')'
#     expression ::= expression '=>' expression
#     expression ::= expression '<=>' expression
#     expression ::= expression '^' expression
#     expression ::= expression 'v' expression
#     expression ::= '~' expression
#dictates all allowed tokens
allowed_tokens = \
        {
            '=>'   : 'IMP',
            '<=>'  : 'BIC',
            '^'    : 'AND',
            '||'    : 'OR', #python won't recognize the v - 'or' symbol, so we will use the boolean operator 'or'
            '~'    : 'NOT',
            '('    : 'LPAR',
            ')'    : 'RPAR'
        }
def isLetter(lett):
    if lett in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or '~' in lett or 'NOT' in lett:
        return True
    else:
        return False

def isOperator(op):
    if op in precedence_map.keys():
        return True
    else:
        return False

#gives precedence values of valid operators
precedence_map = \
        {
            'IMP'   : 4,
            'BIC'   : 5,
            'AND'   : 2,
            'OR'    : 3,
            'NOT'   : 1
        }

#global variables for tokens/list of
tokenList = []
tokensListPF = []

#create an expression tree to load the logical sentence into
def constructExpTree():
    #conditions of expression tree:
    #-binary
    #-internal nodes are operators
    #-leaf nodes are operands
    s = Stack() #stack as helper to create expTree
    for item in tokensListPF: #iterate through all items in token list
        #if item is an operand add to stack
        if isLetter(item) is True:
            tree = ExpTree(item)
            s.push(tree)
        #this method pushes subtrees onto stack and assembles them as left children of new operators
        elif isOperator(item) is True: #if item is an operator
            tree = ExpTree(item)
            tree.rightChild = s.pop()
            tree.leftChild = s.pop()
            s.push(tree)
    tree = s.pop()

    return tree #should return entire tree as single element in stack

#doesnt work at the moment...
def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        print(eTree.token)
        printTree(eTree.rightChild)

def tokenizer(proposition):
    #add portion here to verify that tokens are valid
    Q = Queue()
    tmpString = ''
    for i in range(len(proposition)):
        #whitespace is the token delimeter
        #CASE: if curr element is a delimeter
        if proposition[i] is ' ':
            while(not Q.isEmpty()):
                tmp = Q.dequeue()
                tmpString = tmpString+tmp
            if tmpString.isalpha() is True: #if str is a char
                tokenList.append(tmpString)
            elif '~' in tmpString: #if negated letter
                tmpString = tmpString.replace('~', 'NOT')
                tokenList.append(tmpString)
            else: #if char is not a string but rather an operator or par
                tokenList.append(allowed_tokens[tmpString])
            tmpString = ''
        #CASE: if we are on last element of list
        elif (i == (len(proposition)-1)):
            Q.enqueue(proposition[i])
            while(not Q.isEmpty()):
                tmp = Q.dequeue()
                tmpString = tmpString+tmp
            if tmpString.isalpha() is True: #if char is a letter
                tokenList.append(tmpString)
            elif '~' in tmpString:
                tmpString = tmpString.replace('~', 'NOT')
                tokenList.append(tmpString)
            else: #if char is not a string but rather an operator or par
                tokenList.append(allowed_tokens[tmpString])
            tmpString = ''
        #CASE: if element is not a delimeter nor the final element
        else:
            Q.enqueue(proposition[i])

#func to make infix notation to postfix
#we start by analyzing input tokens from 1st ot last element in infix order
#at each step we are analyzing a subsequent token in the string
#our goal is to fill a different empty string with the same tokens in POSTFIX order, with the help of a stack
#1) if token is an operand (AKA a letter), append it to the PF string
#2) if token is a left paren, push it onto the stack
#3) if token is a right paren, pop values from stack->PFstring until a left paren is found
#4) if token is an operator (AKA AND, OR, etc...), pop everything from the stack->PFstring that has >= precedence,
#       then push curr item
def makePF():
    inParen = False
    s = Stack()
    for item in tokenList:
        s.printS()
        if isLetter(item) is True: #if operand
            tokensListPF.append(item)
        #important idea here is that the parens are taken into consideration for precedence but never pushed to EXPtree
        elif item is 'LPAR':
            s.push(item)
            inParen = True
        elif item is 'RPAR':
            tmp = s.peek()
            while tmp is not 'LPAR':
                tmp = s.pop()
                tokensListPF.append(tmp)
            inParen = False
        elif isOperator(item) is True: #if operator
            if inParen is True:
                print('we enter parens. Pushing op to stack, ', item)
                s.push(item)
            elif s.isEmpty() is False: #if there's anything on the stack
                tmp = s.peek()
                while precedence_map[item] >= precedence_map[tmp] and s.isEmpty() is False:
                    tmp = s.pop()
                    tokensListPF.append(tmp)
                s.push(item)
            else: #if the stack is empty
                s.push(item)
                s.printS()
        if item == tokenList[-1]: #if on last item of input string, add rest of stack to list
            while s.isEmpty() is False:
                tokensListPF.append(s.pop())

def main():
    logic = input("enter your logical sentence\n")
    print('input infix string, ', logic)
    tokenizer(logic)  # lexical analysis
    makePF()  # convert the tokens now to postfix order
    print('postfix str ', tokensListPF)
    #now create an expression tree from the postfix equation
    eT = constructExpTree()
    printTree(eT)
    toCNF(eT)

main()
