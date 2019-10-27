#**********************************************************************************************************************
#CSC 442: Artificial Intelligence
#Code designed to convert well-formed-formula strings into a postfix tree
#Author: Rich Magnotti (netid: rmagnott@ur.rochester.edu)
#**********************************************************************************************************************
from CNF_Converter import toCNF
from Data_Structs import Stack
from Data_Structs import ExpTree
import re
#grammar:
#     sentence ::= letter
#     expression ::= '(' expression ')'
#     expression ::= expression '=>' expression
#     expression ::= expression '<=>' expression
#     expression ::= expression '^' expression
#     expression ::= expression 'v' expression
#     expression ::= '!' expression
#dictates all allowed tokens
precedence_map = \
        {
            '=>'   : 5,
            '<=>'  : 6,
            '&'    : 3,
            '|'   : 4, #python won't recognize the v - 'or' symbol, so we will use the boolean operator 'or'
            '!'    : 2,
            '('    : 1,
            '=>*': 5,
            '<=>*': 6,
            '&*': 3,
            '|*': 4,  # python won't recognize the v - 'or' symbol, so we will use the boolean operator 'or'
        }

def flipToken(tree):
    print('current item being flipped ', tree.token, ' with negative status ', tree.isNeg)
    if isLetter(tree.token) is True:
        print('current flip is recognized to be a letter! ')
        if tree.isNeg is None or tree.isNeg is False:
            tree.token = '!' + tree.token
            tree.isNeg = True

        elif tree.isNeg is True:
            tree.token = tree.token.replace('!', '')
            tree.isNeg = False

    else:
        if re.search('[&]', tree.token):
            print('recognized that we have an & to be flipped ')
            tree.token = '|'

        elif re.search('[|]', tree.token):
            tree.token = '&'

def isLetter(lett):
    if (re.search('[a-zA-z]', lett) and re.search('[!]', lett)) or (re.search('[a-zA-z]', lett) and re.search('[*]', lett)) or re.search('[a-zA-z]', lett):
        return True
    else:
        return False

def isOperator(op):
    if op in precedence_map.keys():
        return True
    else:
        return False

def flipListToken(token):
        if re.search('[*]', token):
            token = token.replace('*', '')
        else:
            token =  token + '*'
        return token

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
            #if tree token has negation flag, set its value of neg to true
            if re.search('[*]', item):
                tree.token = tree.token.replace('*', '')
                flipToken(tree)
            s.push(tree)
        #this method pushes subtrees onto stack and assembles them as left children of new operators
        elif isLetter(item) is False: #if item is an operator
            tree = ExpTree(item)
            if re.search('[*]', item):
                tree.token = tree.token.replace('*', '')
                flipToken(tree)
            tree.rightChild = s.pop()
            tree.leftChild = s.pop()
            s.push(tree)
    tree = s.pop()

    return tree #should return entire tree as single element in stack

#doesnt work at the moment...
treeList = []
def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        treeList.append(eTree.token)
        printTree(eTree.rightChild)
    return treeList

#func to make infix notation to postfix
#we start by analyzing input tokens from 1st ot last element in infix order
#at each step we are analyzing a subsequent token in the string
#our goal is to fill a different empty string with the same tokens in POSTFIX order, with the help of a stack
#1) if token is an operand (AKA a letter), append it to the PF string
#2) if token is a left paren, push it onto the stack
#3) if token is a right paren, pop values from stack->PFstring until a left paren is found
#4) if token is an operator (AKA AND, OR, etc...), pop everything from the stack->PFstring that has >= precedence,
#       then push curr item
tokensListPF = []
def tokenizerPF(tokenList):
    s = Stack()
    k = 0
    for item in tokenList:
        #print('current stack ')
        #s.printS()
        if isLetter(item) is True: #if operand
            tokensListPF.append(item)

        #important idea here is that the parens are taken into consideration for precedence but never pushed to EXPtree
        #NOW IN NEGATION AND PARENS
        if tokenList[k] is '(' and tokenList[k - 1] is '!':
            numParenSets = 1 #b/c we've already encountered one paren to get into this elif
            j = k + 1
            while numParenSets > 0:
                if tokenList[j] is '(':
                    s.push(tokenList[j])
                    numParenSets = numParenSets + 1
                elif tokenList[j] is ')':
                    numParenSets = numParenSets - 1
                elif tokenList[j] is '!':
                    tokenList[j] = ' '
                    break
                else:
                    tokenList[j] = flipListToken(tokenList[j])
                j = j + 1
            tokenList[k - 1] = ' '
            s.pop() #get rid of negation on stack

        if item is '(':
            s.push(item)
        elif item is ')':
            tmp = s.pop()
            while tmp is not '(':
                tokensListPF.append(tmp)
                tmp = s.pop()
        elif isOperator(item) is True: #if operator
            while s.isEmpty() is False and precedence_map[s.peek()] >= precedence_map[item]:
                    tmp = s.pop()
                    tokensListPF.append(tmp)
            s.push(item)
        k = k + 1
    while s.isEmpty() is False:
        tokensListPF.append(s.pop())

def main():
    tmp = input("enter your logical sentence\n")
    tokenList = tmp.split(" ")
    tokenizerPF(tokenList)  # convert the tokens now to postfix order
    print('postfix str ', tokensListPF)
    #now create an expression tree from the postfix equation
    eT = constructExpTree()
    toCNF(eT)
    tList = printTree(eT)
    print(tList)

main()
