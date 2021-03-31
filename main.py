import numpy as np

from data_loader import grammar, sentence

def printCKY(table):
    for i in table:
        print(i)

if __name__=='__main__':
    # load grammar
    G = grammar()
    G.load('./data/grammar.txt')

    # load sentence
    S = sentence()
    S.load('./data/input.txt')

    for idx, (parse) in enumerate(S.content):
        print("Input:", parse)
        split_sent = parse.split(' ')
        #print(split_sent)
        n = len(split_sent)

        cky_table = [[[] for i in range(n+1)] for j in range(n)]

        for i in range(n):
            cky_table[i][i+1] = G.applyRule(split_sent[i])

        
        printCKY(cky_table)





