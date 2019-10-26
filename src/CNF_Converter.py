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

def bicElim(tree):
    #do DFS to find biconditionals and solve bottom up
    if tree is not None:
        bicElim(tree.leftChild)
        if tree.token is '<=>':
            tmp1 = tree.leftChild
            tmp2 = tree.rightChild

            tree.token = 'AND' #set current biconditional to an 'and'

            tL = ExpTree('=>')
            tR = ExpTree('=>')

            tree.leftChild = tL
            tree.rightChild = tR

            tL.leftChild = tmp1
            tL.rightChild = tmp2

            tR.rightChild = tmp2
            tR.leftChild = tmp1
        bicElim(tree.rightChild)
    return tree

opList = ['=>', '<=>', '|', '&', '~']

def isOp(tree):
    if tree.token in opList:
        return True
    else:
        return False

def flipToken(tree):
    if isOp(tree) is False:
        tree.token = '~' + tree.token
        return tree.token

    elif isOp(tree) is True:
        if tree.token in '&':
            tree.token = '|'
            return tree.token

        elif tree.token in '|':
            tree.token = '&'
            return tree.token

def propNeg(tree):
    #essentially DeMorgan's law
    if tree is not None:
        propNeg(tree.leftChild)
        if tree is not rootNode:
            if tree.leftChild: #if not bottom node
                tree.leftChild.token = flipToken(tree.leftChild)
                tree.rightChild.token = flipToken(tree.rightChild)
        else:
            tree.leftChild.token = flipToken(tree.leftChild)
    return tree

def impElim(tree):
    if tree.leftChild is not None:
        impElim(tree.leftChild)
        if tree.token is '=>':
            tree = propNeg(tree) #the negative propagation only affects left children
            tree.token = '|'
    return tree

def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        print(eTree.token)
        printTree(eTree.rightChild)

def distribCD(tree):
    print('current item ', tree.token)
    if tree.leftChild.leftChild is not None and tree.rightChild.rightChild is not None:
        
        distribCD(tree.leftChild)
        #stuff
        distribCD(tree)
        distribCD(tree.rightChild)
        #stuff

    else:
        if tree.token is '|' and (tree.leftChild.token is '&' or tree.rightChild.token is '&'):
        #case1: atomic proposition distributed over plural proposition
            if isOp(tree.leftChild) is False or isOp(tree.rightChild) is False:
                #to keep left side always as the one with the atomic proposition
                if tree.rightChild.leftChild is False:
                    tmp1 = tree.leftChild
                    tmp2 = tree.rightChild
                    tree.leftChild = tmp2
                    tree.rightChild = tmp1
                #doesn't matter which side is which, b/c will be passed to recursion again
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

                distribCD(tree)

            #if proposition is a clause/sentence
            else:
                tmp1 = copy.deepcopy(tree.leftChild)
                tmp2 = copy.deepcopy(tree.rightChild)

                tree.token = '&'
                tree.leftChild = ExpTree('|')
                tree.rightChild = ExpTree('|')

                tree.leftChild.leftChild = ExpTree('')
                tree.leftChild.leftChild = copy.deepcopy(tmp1.leftChild)

                tree.leftChild.rightChild = ExpTree('')
                tree.leftChild.rightChild = copy.deepcopy(tmp2)

                tree.rightChild.leftChild = ExpTree('')
                tree.rightChild.leftChild = copy.deepcopy(tmp1.rightChild)

                tree.rightChild.rightChild = ExpTree('')
                tree.rightChild.rightChild = copy.deepcopy(tmp2)

                distribCD(tree)

global rootNode
def toCNF(tree):
    #the following will set rootNode reference pointer to same memory location as 'tree'
    global rootNode
    rootNode = tree #set global variable so we know which node is root
    print('----------------------------------------------------------------------------------------------------')
    CNF1 = bicElim(tree)
    print('CNF tree after bicon ----------')
    printTree(CNF1)

    CNF2 = impElim(CNF1)
    print('CNF tree after imp   ----------')
    printTree(CNF2)

    distribCD(tree)
    print('CNF tree after disj  ----------')
    printTree(tree)
def main():
    pass

main()