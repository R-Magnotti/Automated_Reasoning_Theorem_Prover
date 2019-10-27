#**********************************************************************************************************************
#CSC 442: Artificial Intelligence
#Code designed to convert a propositional logic expression tree to a CNF form expression tree
#Author: Rich Magnotti (netid: rmagnott@ur.rochester.edu)
#**********************************************************************************************************************

#this module is designed to take in a propositional logic expression tree and return the same tree in CNF form
#CNF:
#step1: eliminate biconditionals <=>
#step2: eliminate implications =>
#step3: move negations inwards ~
#step4: distribute disjunction over conjunction
from Data_Structs import ExpTree
from Data_Structs import Stack
import copy

S = Stack() #global stack

opList = ['=>', '<=>', '|', '&', '!']

def isOp(tree):
    if tree.token in opList:
        return True
    else:
        return False

def flipToken(tree):
    if isOp(tree) is False:
        if tree.isNeg is None or tree.isNeg is False:
            tree.token = '!' + tree.token
            tree.isNeg = True
        elif tree.isNeg is True:
            tree.token = tree.token.replace('!', '')
            tree.isNeg = False
        return tree.token

    elif isOp(tree) is True:
        if tree.token in '&':
            tree.token = '|'
            return tree.token

        elif tree.token in '|':
            tree.token = '&'
            return tree.token

#b/c we are doing from bottom up, we will never have to worry about negating over =>
def makeNeg(tree):
    if tree is not None:
        makeNeg(tree.leftChild)
        flipToken(tree)
        makeNeg(tree.rightChild)

def bicElim(tree):
    #do DFS to find biconditionals and solve bottom up
    if tree is not None:
        bicElim(tree.leftChild)
        if '<=>' in tree.token:
            tmp1 = copy.deepcopy(tree.leftChild)
            tmp2 = copy.deepcopy(tree.rightChild)

            tree.token = '&' #set current biconditional to an 'and'

            tL = ExpTree('=>')
            tR = ExpTree('=>')

            tree.leftChild = tL
            tree.rightChild = tR

            tL.leftChild = copy.deepcopy(tmp1)
            tL.rightChild = copy.deepcopy(tmp2)

            tR.rightChild = copy.deepcopy(tmp1)
            tR.leftChild = copy.deepcopy(tmp2)
        bicElim(tree.rightChild)
    return tree

def impElim(tree):
    if tree is not None:
        impElim(tree.leftChild)
        if '=>' in tree.token:
            makeNeg(tree.leftChild)
            tree.token = '|'
        impElim(tree.rightChild)

def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        print(eTree.token)
        printTree(eTree.rightChild)

def has2Gens(tree):
    if tree.leftChild.leftChild is not None or tree.leftChild.rightChild is not None:
        return True
    if tree.rightChild.leftChild is not None or tree.rightChild.rightChild is not None:
        return True
    else:
        return False

def fixDisjunction(tree):
    if tree.token is '|' and (tree.leftChild.token is '&' or tree.rightChild.token is '&'):
        # case1: atomic proposition distributed over plural proposition
        if isOp(tree.leftChild) is False or isOp(tree.rightChild) is False:
            # to keep left side always as the one with the atomic proposition
            if tree.rightChild.leftChild is None:
                tmp1 = tree.leftChild
                tmp2 = tree.rightChild
                tree.leftChild = tmp2
                tree.rightChild = tmp1
            # doesn't matter which side is which, b/c will be passed to recursion again
            tmp1 = copy.deepcopy(tree.leftChild)
            tmp2 = copy.deepcopy(tree.rightChild.leftChild)
            tmp3 = copy.deepcopy(tree.rightChild.rightChild)

            tree.token = '&'
            tree.leftChild = ExpTree('|')
            tree.rightChild = ExpTree('|')

            tree.leftChild.leftChild = ExpTree('')
            tree.leftChild.leftChild = copy.deepcopy(tmp1)

            tree.leftChild.rightChild = ExpTree('')
            tree.leftChild.rightChild = copy.deepcopy(tmp2)

            tree.rightChild.leftChild = ExpTree('')
            tree.rightChild.leftChild = copy.deepcopy(tmp1)

            tree.rightChild.rightChild = ExpTree('')
            tree.rightChild.rightChild = copy.deepcopy(tmp3)

        # if proposition is a clause/sentence
        else:
            tmp1 = copy.deepcopy(tree.leftChild)
            tmp2 = copy.deepcopy(tree.rightChild)

            tree.token = '&'
            tree.leftChild = None
            tree.rightChild = None
            tree.leftChild = ExpTree('|')
            tree.rightChild = ExpTree('|')

            tree.leftChild.leftChild = copy.deepcopy(tmp1.leftChild)

            tree.leftChild.rightChild = copy.deepcopy(tmp2)

            tree.rightChild.leftChild = copy.deepcopy(tmp1.rightChild)

            tree.rightChild.rightChild = copy.deepcopy(tmp2)

def topDownDFS(tree):
    if tree.token is '|' and (tree.leftChild.token is '&' or tree.rightChild.token is '&'):
        DFSBottomUp(tree)
    else:
        return

def DFSBottomUp(tree):
    #base case is a node with 2 generations
    if has2Gens(tree) is not True:
        DFSBottomUp(tree.leftChild)
        DFSBottomUp(tree.rightChild)
    else:
        fixDisjunction(tree)
        topDownDFS(tree.leftChild)
        topDownDFS(tree.rightChild)

def toCNF(tree):
    #the following will set rootNode reference pointer to same memory location as 'tree'
    rootNode = tree #set global variable so we know which node is root
    bicElim(rootNode)

    impElim(rootNode)

    if has2Gens(rootNode) is True:
        DFSBottomUp(rootNode)

    print('Final CNF Tree')