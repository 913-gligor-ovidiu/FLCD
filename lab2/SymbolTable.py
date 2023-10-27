from HashTable import HashTable

class SymbolTable:
    def __init__(self, size):
        self.table = HashTable(size)
        self.current = 1

    def insert(self, name):
        self.table.insert(name, self.current)
        self.current += 1

    def get(self, name): # return the position in the symbol table of the identifier/constant
        return self.table.get(name)

    def display(self):
        return self.table.display()
    

