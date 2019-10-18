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
        print('current node ', tree.token)
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
    if tree.token in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return False
    elif tree.token in opList:
        return True

def flipToken(tree):
    if isOp(tree) is False:
        tree.token = '~' + tree.token
        print('new token ', tree.token)
        return tree.token

    elif isOp(tree) is True:
        if tree.token is 'AND':
            tree.token = 'OR'
            print('new token ', tree.token)
            return tree.token

        elif tree.token is 'OR':
            tree.token = 'AND'
            print('new token ', tree.token)
            return tree.token

def propNeg(tree):
    if tree is not None:
        propNeg(tree.leftChild)
        if tree.leftChild is None:
            tree.token = flipToken(tree)
        else:
            print('propping negs, current tree node = ', tree.leftChild.token)
            tree.leftChild.token = flipToken(tree.leftChild)
            tree.rightChild.token = flipToken(tree.rightChild)

def impElim(tree):
    if tree is not None:
        impElim(tree.leftChild)
        if tree.token is 'IMP':
            propNeg(tree.leftChild) #the negative propagation only affects left children
            tree.token = 'OR'
    return tree

def printTree(eTree):
    #simple inorder DFS traversal to grab values from nodes
    if eTree is not None:
        printTree(eTree.leftChild)
        print(eTree.token)
        printTree(eTree.rightChild)

def toCNF(tree):
    print('----------------------------------------------------------------------------------------------------')
    CNF1 = bicElim(tree)
    print('CNF tree----------')
    printTree(CNF1)

    CNF2 = impElim(CNF1)
    print('CNF tree----------')
    printTree(CNF2)

    #moveNeg(tree)
    #disToCon(tree)
def main():
    pass

main()