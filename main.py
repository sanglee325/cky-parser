import numpy as np

from data_loader import *

def printCKYtable(table):
    for i in table:
        for j in i:
            j.print_cell()
        print()

def printCKYtree(f, root, prev=None):
    if root is None:
        return
    print('(', end='')
    f.write('(')
    if root.get_left() is None and root.get_right() is None:
        print(prev.get_pos1(), end=' ')
        tmpstr = prev.get_pos1()+ ' '
        f.write(tmpstr)
        print(root.get_pos1(), end='')
        tmpstr = root.get_pos1() + ''
        f.write(tmpstr)
    else:
        print(root.get_value(), end=' ')
        tmpstr = root.get_value()+ ' '
        f.write(tmpstr)
    printCKYtree(f, root.get_left(), root)
    printCKYtree(f, root.get_right(), root)
    print(')', end='')
    f.write(')')

def printSent(root, prev=None):
    if root is None:
        return
    #print('[', end='')
    if root.get_left() is None and root.get_right() is None:
        print(root.get_pos1(), end=' ')
        #print(prev.get_pos1(), end=' ')
    printSent(root.get_left(), root)
    printSent(root.get_right(), root)
    #print(']', end='')


if __name__=='__main__':
    # load grammar
    G = grammar()
    G.load('./data/grammar.txt')

    # load sentence
    S = sentence()
    S.load('./data/input.txt')

    f = open("./output.txt", 'w')
    f.close()
    f = open("./used_grammar.txt", 'w')
    f.close()

    for idx, (parse) in enumerate(S.content):
        print("Input:", parse)
        split_sent = parse.split(' ')
        #print(split_sent)
        n = len(split_sent)

        cky_table = [[cell() for i in range(n+1)] for j in range(n)]

        # fill in diagonal table
        for i in range(n):
            p = production(G, start=i+1, end=i+2, pos1=split_sent[i], pos2=None)
            p.convert_word()            
            for pos in p.get_value():
                convert = production(G, start=i+1, end=i+2, pos1=pos, p1=p)
                convert.get_result()
                #convert = production(G, pos1=pos, pos2=None).get_result()
                if convert.get_value() != None:
                    cky_table[i][i+1].add_prod(convert)
        
        # run cky parsing algorithm
        for i in range(1, n):
            for j in range(i, 0, -1):
                c = i+1
                r = j-1
                for k in range(1, c-r):
                    for l in range(1, c-r):
                        t1 = cky_table[r][c-k]
                        t2 = cky_table[r+l][c]
                        
                        if t1.productions != None and t2.productions != None:
                            for a in t1.productions:
                                for b in t2.productions:
                                    #print(a.get_value(), b.get_value())
                                    pos1_s, pos1_e = a.get_range()
                                    pos2_s, pos2_e = b.get_range()
                                    if pos1_e == pos2_s:
                                        p = production(start=pos1_s, end=pos2_e, pos1=a.get_value(), pos2=b.get_value(), g_data=G, p1=a, p2=b)
                                        p.get_result()
                                        #p = production(pos1=a, pos2=b, g_data=G).get_result()
                                        if p.get_value() != None:
                                            #print(a.get_value(), b.get_value())
                                            cky_table[r][c].add_prod(p)
                                            #print(split_sent[r:c], p.get_value())
                            
        
        #printCKYtable(cky_table)
        
        for r in cky_table:
            for c in r:
                if c.get_prod() != None:
                    for p in c.get_prod():
                        if p.get_value() == 'S':
                            f = open("./output.txt", 'a')
                            #printSent(p)
                            printCKYtree(f, p)
                            print()
                            f.write('\n')
                            f.close()
        f = open("./output.txt", 'a')
        print()
        f.write('\n')
        f.close()

