from Grammar import Grammar
import copy

class LL1:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__first = {}
        self.__follow = {}
    
    def concatenation_of_length_one(self, list1, list2):
        if '&' in list1:
            return list1 + list2
        return list1 

    def compute_first(self):
        for terminal in self.__grammar.getTerminals():
            self.__first[terminal] = [terminal] # initialize first of terminals with the terminal itself
        
        for lhs in self.__grammar.getProductions().keys():
            if lhs not in self.__first.keys():
                self.__first[lhs] = [] # initialize first of nonterminals with empty list
            for elem in self.__grammar.getProductions()[lhs]:
                if elem in self.__grammar.getTerminals():
                    self.__first[lhs].append(elem) # if rhs is terminal, add it to first of lhs
                elif elem[0] in self.__grammar.getTerminals():
                    self.__first[lhs].append(elem[0]) # if rhs starts with terminal, add it to first of lhs

        done = False
        while not done:
            previous = copy.deepcopy(self.__first)
            for lhs in self.__grammar.getProductions().keys():
                for production  in self.__grammar.getProductions()[lhs]:
                    res = []
                    for elem in production:
                        if len(res) == 0:
                            res += previous[elem]
                        else:
                            res = self.concatenation_of_length_one(res, previous[elem])     
                    self.__first[lhs] += res
                self.__first[lhs] = list(set(self.__first[lhs]))
            if previous == self.__first:
                done = True

    def print_first(self):
        for key in self.__first.keys():
            print(f"First({key}) = {self.__first[key]}")   
    

    def generate_follow(self):
        for nonterminal in self.__grammar.getNonterminals():
            if nonterminal != self.__grammar.getStartSymbol():
                self.__follow[nonterminal] = []
        self.__follow[self.__grammar.getStartSymbol()] = ['&']
        
        done = False
        while not done:
            previous = copy.deepcopy(self.__follow)
            for nonterminal in self.__grammar.getNonterminals():
                productionsForTerminal = self.__grammar.getProductionThatContains(nonterminal)
                if productionsForTerminal == {}: # if nonterminal is not in any production
                    continue
                for lhs in productionsForTerminal.keys():
                    productions = productionsForTerminal[lhs]
                    for production in productions:
                        if nonterminal == production[-1]:
                            self.__follow[nonterminal] += previous[lhs]
                        else:
                            index = production.index(nonterminal)
                            res = []
                            for i in range(index + 1, len(production)):
                                if len(res) == 0:
                                    res += self.__first[production[i]]
                                else:
                                    res = self.concatenation_of_length_one(res, self.__first[production[i]])
                            if '&' in res:
                                res.remove('&')
                                self.__follow[nonterminal] += res
                                self.__follow[nonterminal] += previous[lhs]
                            else:
                                self.__follow[nonterminal] += res
                    self.__follow[nonterminal] = list(set(self.__follow[nonterminal]))   
                        
            if previous == self.__follow:
                done = True
                
    
    def print_follow(self):
        for key in self.__grammar.getNonterminals():
            print(f"Follow({key}) = {self.__follow[key]}")

def main():
    grammar = Grammar()
    grammar.readFromFile("lab5-6-7/files/g1.txt")
    grammar.print_nonterminals()
    grammar.print_terminals()
    grammar.print_productions()
    grammar.print_production('S')
    grammar.checkCFG()
    ll1 = LL1(grammar)
    ll1.compute_first()
    ll1.print_first()
    ll1.generate_follow()
    ll1.print_follow()

main()