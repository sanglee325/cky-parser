import numpy as np

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

class grammar:
    def __init__(self):
        self.rule = Dictlist()
        self.data = None
        
    def load(self, path):
        try:
            self.data = np.loadtxt(path, dtype='str', delimiter=' -> ', encoding='utf-8')
            for a, b in self.data:
                self.rule[b] = a
            #self.printRule()
            return self.rule
        except:
            print("[ERROR] loading grammar failed")
        
        return None

    def printRule(self):
        for r in self.rule:
            for p in self.rule[r]:
                print(p, '->', r)

    def getRule(self, key):
        try: 
            val = self.rule[key]
            return val
        except:
            return None

class sentence:
    def __init__(self):
        self.content = None
    
    def load(self, path):
        try:
            self.content = np.loadtxt(path, dtype='str', delimiter='\t', encoding='utf-8')
            return self.content
        except:
            print("[ERROR] loading sentence failed")
        
        return None

class production:
    def __init__(self, g_data, pos1=None, pos2=None, p1=None, p2=None):
        self.result = []
        self.pos1 = pos1
        self.pos2 = pos2
        self.p1 = p1
        self.p2 = p2
        self.node_stack = []
        self.g_data = g_data

    def get_result(self):
        if self.check_overlap() is False:
            self.result = None
            return
        
        if self.pos1 == None:
            self.result = None
        else:
            if self.pos2 == None:
                tmp = self.g_data.getRule(self.pos1)
            elif self.pos1 != None and self.pos2 != None:
                #print(self.pos1, self.pos2)
                tmp = self.g_data.getRule(self.pos1+" "+self.pos2)
            
            if tmp == None:
                self.result = tmp
            else:
                self.result = tmp[0]
            
        #print('production: ', self.result)
        return self.result
    
    def convert_word(self):
        if self.pos2 == None:
           self.result = self.g_data.getRule(self.pos1)
        return self.result
    
    def check_overlap(self):
        if self.p1 is not None and len(self.p1.get_stack()) == 0:
            self.node_stack.append(self.p1)
        if self.p2 is not None and len(self.p2.get_stack()) == 0:
            self.node_stack.append(self.p2)
        
        for i in self.p1.get_stack():
            if i in self.p2.get_stack():
                return False
        
        if self.p1 is not None:
            self.node_stack += self.p1.get_stack()
        if self.p2 is not None:
            self.node_stack += self.p2.get_stack()

        return True


    def get_value(self):
        return self.result

    def get_left(self):
        return self.p1
    
    def get_right(self):
        return self.p2

    def get_pos1(self):
        return self.pos1
    
    def get_stack(self):
        return self.node_stack

class cell:
    def __init__(self):
        self.productions = None
        self.element = 0
    
    def add_prod(self, production):
        if production != None:
            if self.productions == None:
                self.productions = []
            self.productions.append(production)

    
    def print_cell(self):
        if self.productions == None:
            print("None", end=' ')
        else:
            print('[', end='')
            for p in self.productions:
                print(p.get_value(), end=' ')
            print(']', end=' ')

    def get_prod(self):
        return self.productions

