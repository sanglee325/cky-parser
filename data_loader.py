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

    def applyRule(self, key):
        return self.rule[key]

class sentence:
    def __init__(self):
        self.content = None
    
    def load(self, path):
        try:
            self.content = np.loadtxt(path, dtype='str', delimiter='\t', encoding='utf-8')
            print(self.content)
            return self.content
        except:
            print("[ERROR] loading sentence failed")
        
        return None


