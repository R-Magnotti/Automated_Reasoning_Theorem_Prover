import sys

dict = {'(((P => Q) & P) & !(Q))': '(((!(P) | Q) & P) & !(Q))'}

def genCNF(prop):
   return dict[prop]

print(genCNF(sys.argv[1]))


