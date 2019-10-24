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

S = Stack() #global stack

def bicElim(tree):
    #do DFS to find biconditionals and solve bottom up
    if tree is not None:
        bicElim(tree.leftChild)
        if tree.token is 'BIC':
            tmp1 = tree.leftChild
            tmp2 = tree.rightChild

            tree.token = 'AND' #set current biconditional to an 'and'

            tL = ExpTree('IMP')
            tR = ExpTree('IMP')

            tree.leftChild = tL
            tree.rightChild = tR

            tL.leftChild = tmp1
            tL.rightChild = tmp2

            tR.rightChild = tmp2
            tR.leftChild = tmp1
        bicElim(tree.rightChild)
    return tree

opList = ['IMP', 'BIC', 'OR', 'AND', 'NOT']

def isOp(tree):
    if tree.token in opList:
        return True
    else:
        return False

def flipToken(tree):
    if isOp(tree) is False:
        tree.token = 'NOT' + tree.token
        return tree.token

    elif isOp(tree) is True:
        if tree.token in 'AND':
            tree.token = 'OR'
            return tree.token

        elif tree.token in 'OR':
            tree.token = 'AND'
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
        if tree.token is 'IMP':
            tree = propNeg(tree) #the negative propagation only affects left children
            tree.token = 'OR'
    return tree

def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        print(eTree.token)
        printTree(eTree.rightChild)

def checkDL(tree):
    if isOp(tree.leftChild) is False: #if left child is a letter
        if tree.rightChild.token is not tree.token:
            return True
def checkDR(tree):
    if isOp(tree.rightChild) is False: #if left child is a letter
        if tree.leftChild is not tree.token:
            return True

def distributeL(tree):
    #for left side of distribution
    print('in distrib L tree def, current node ', tree.token, 'its left child ', tree.leftChild.token, 'its right child ', tree.rightChild.token)
    tree.leftChild.leftChild = ExpTree(tree.leftChild)
    tree.leftChild.token = tree.token
    tree.leftChild.rightChild = ExpTree(tree.rightChild.leftChild)

    #for right side of distribution
    tree.rightChild.token = flipToken(tree.rightChild)
    tree.rightChild.leftChild = tree.leftChild

    tree.token = flipToken(tree)

def distributeR(tree):
    print('in distrib R tree def, current node ', tree.token, 'its left child ', tree.leftChild.token,
          'its right child ', tree.rightChild.token)
    #for left side of distribution
    tree.rightChild.rightChild = ExpTree(tree.rightChild)
    tree.rightChild.token = tree.token
    tree.rightChild.leftChild = ExpTree(tree.leftChild.rightChild)

    #for right side of distribution
    tree.leftChild.token = flipToken(tree.leftChild)
    tree.leftChild.rightChild = tree.rightChild

    tree.token = flipToken(tree)

def elimDisj(tree):
    if tree.leftChild is not None or tree.rightChild is not None:
        print('elim disj curr node and left child ', tree.token, tree.leftChild.token)
        elimDisj(tree.leftChild)
        if checkDL(tree) is True:
            distributeL(tree)
        elif checkDR(tree) is True:
            distributeR(tree)
        elimDisj(tree.rightChild)
    return tree

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
    print('passing tree to impelim ', CNF2.token, 'global rootnode ', rootNode.token)

    finCNF = elimDisj(tree)
    print('CNF tree after disj  ----------')
    printTree(finCNF)
def main():
    pass

main()