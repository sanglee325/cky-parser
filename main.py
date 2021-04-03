import numpy as np

from data_loader import *

def printCKYtable(table):
    for i in table:
        for j in i:
            j.print_cell()
        print()

def saveCKYtree(f, root, prev=None):
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
    saveCKYtree(f, root.get_left(), root)
    saveCKYtree(f, root.get_right(), root)
    print(')', end='')
    f.write(')')

def saveUsedG(f, root, prev=None):
    if root is None:
        return
    if root.get_left() is None and root.get_right() is None:
        tmpstr = str(root.get_idx()) + ' '
        f.write(tmpstr)
        f.write('(')
        tmpstr = prev.get_pos1() + ' '
        f.write(tmpstr)
        tmpstr = root.get_pos1() + ''
        f.write(tmpstr)
        f.write(')\n')
    else:
        tmpstr = str(root.get_idx()) + ' '
        f.write(tmpstr)
        f.write('(')
        tmpstr = root.get_value() + ' '
        f.write(tmpstr)

        f.write('(')
        if root.get_right() is None:
            tmpstr = str(root.get_left().get_idx())
            f.write(tmpstr)
        else:
            tmpstr = str(root.get_left().get_idx()) + ', '
            f.write(tmpstr)
            tmpstr = str(root.get_right().get_idx())
            f.write(tmpstr)
        f.write(')')
        
        f.write(')\n')
    saveUsedG(f, root.get_left(), root)
    saveUsedG(f, root.get_right(), root)

def printUsedG(root, prev=None):
    if root is None:
        return
    if root.get_left() is None and root.get_right() is None:
        print(root.get_idx(), end=' ')
        print('(', end='')
        print(prev.get_pos1(), end=' ')
        print(root.get_pos1(), end='')
        print(')')
    else:
        print(root.get_idx(), end=' ')
        print('(', end='')
        print(root.get_value(), end=' ')

        print('(', end='')
        if root.get_right() is None:
            print(root.get_left().get_idx(), end='')
        else:
            print(root.get_left().get_idx(), end=', ')
            print(root.get_right().get_idx(), end='')
        print(')', end='')
        
        print(')')
    printUsedG(root.get_left(), root)
    printUsedG(root.get_right(), root)

def printSent(root, prev=None):
    if root is None:
        return
    if root.get_left() is None and root.get_right() is None:
        print(root.get_pos1(), end=' ')
    printSent(root.get_left(), root)
    printSent(root.get_right(), root)


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

    if S.content.size == 1:
        target = []
        target.append(S.content.tolist())
    else: 
        target = S.content
    for idx, (parse) in enumerate(target):
        print("Input:", parse)
        split_sent = parse.split(' ')
        n = len(split_sent)
        pidx = 0

        cky_table = [[cell() for i in range(n+1)] for j in range(n)]

        # fill in diagonal table
        for i in range(n):
            p = production(G, start=i+1, end=i+2, idx=pidx, pos1=split_sent[i], pos2=None)
            pidx += 1
            p.convert_word()            
            for pos in p.get_value():
                convert = production(G, start=i+1, end=i+2, idx=pidx ,pos1=pos, p1=p)
                pidx += 1
                convert.get_result()
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
                                    pos1_s, pos1_e = a.get_range()
                                    pos2_s, pos2_e = b.get_range()
                                    if pos1_e == pos2_s:
                                        p = production(idx=pidx, start=pos1_s, end=pos2_e, pos1=a.get_value(), pos2=b.get_value(), g_data=G, p1=a, p2=b)
                                        p.get_result()
                                        if p.get_value() != None:
                                            cky_table[r][c].add_prod(p)
                                            pidx += 1
                            
        
        #printCKYtable(cky_table)
        
        for r in cky_table:
            for c in r:
                if c.get_prod() != None:
                    for p in c.get_prod():
                        if p.get_value() == 'S':
                            f = open("./output.txt", 'a')
                            saveCKYtree(f, p)
                            print()
                            f.write('\n')
                            f.close()
        f = open("./output.txt", 'a')
        f.write('\n')
        f.close()
        print()

        f = open("./used_grammar.txt", 'a')
        tmpstr = '%s\n'%(parse)
        f.write(tmpstr)
        f.close()

        for r in cky_table:
            for c in r:
                if c.get_prod() != None:
                    for p in c.get_prod():
                        if p.get_value() == 'S':
                            f = open("./used_grammar.txt", 'a')
                            saveUsedG(f, p)
                            #printUsedG(p)
                            f.write('\n')
                            f.close()

