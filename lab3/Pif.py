class Pif:
    def __init__(self):
        self.pif = []
    
    def add(self,token,position):
        self.pif.append((token,position))
    
    def display(self):
        for pair in self.pif:
            print(pair)
