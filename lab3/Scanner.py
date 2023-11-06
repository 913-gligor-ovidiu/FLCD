from Pif import Pif
from SymbolTable import SymbolTable
import re

class Scanner:
    
    def __init__(self,programPath, tokensPath):
        self.pif = Pif()
        self.constants = SymbolTable(10)
        self.identifiers = SymbolTable(10)
        self.tokens = self.readTokensFromTokenIn(tokensPath)
        self.program = self.readFile(programPath)

    def readFile(self,file_path):
        """
        Will return the input program as a list of lines
        """
        lines = []
        with open(file_path,"r") as f:
            for line in f.readlines():
                    lines.append(line)
        return lines
        
    def readTokensFromTokenIn(self, tokensPath):
        """
        Will return the tokens from the token.in file as a dictionary
        with the key being the token and the value being the line corresponding to the token in the token.in file
        """
        lineCount = 1
        aux = {}
        with open(tokensPath,"r") as f:
            for line in f.readlines():
                line = line.strip()
                aux[line] = lineCount
                lineCount += 1    
        return aux

    def isIdentifier(self, token):
        regexIdentifier = r"^[a-zA-Z]([a-zA-Z]|[0-9])*$"
        return re.match(regexIdentifier, token)

    def isIntegerConstant(self, token):
        regexInteger = r"^(0|[-]?[1-9][0-9]*)$"
        if re.match(regexInteger, str(token)):
            return True
        return False
        
    def isStringConstant(self,token):
        regexString = "^[a-zA-Z0-9_ ?:*^+=.!]*$"
        if re.match(regexString, token):
                return True
        return False
    
    def isCharConstant(self,token):
        regexChar = r"^[a-zA-Z0-9_ ?:*^+=.!]$"
        if re.match(regexChar, token):
            return True
        return False


    def parse(self):
        lineNumber = 1
        stringFlag = 0 
        charFlag = 0
        for line in self.program:
            if line.strip() == "":
                lineNumber += 1
                continue
            line = line.strip()
            for token in self.tokens:
                if token in line:
                    line = line.replace(token," "+token+" ") #add spaces around tokens            


            line = re.sub(r' +',' ',line) # remove multiple spaces from around tokens and keep only 1
            line = line.strip() # remove spaces from beggining and end of line
            lineTokens = line.split(" ") # split line into tokens
            aux = []
            for i in range(len(lineTokens)): # merge <,>,=,! with = if neccesary
               if lineTokens[i] == "=":
                   if lineTokens[i-1] == "<" or lineTokens[i-1] == ">" or lineTokens[i-1] == "!" or lineTokens[i-1] == "=":
                       aux.pop()
                       aux.append(lineTokens[i-1]+lineTokens[i])
                       continue
                   else :
                       aux.append(lineTokens[i])
               else:
                     aux.append(lineTokens[i])
                       
            lineTokens = aux
            print(lineTokens)
            stringConst = ""
            charConst = ""
            for lineToken in lineTokens:
                #check if string or char const is opened and if it is add the token to the const
                if lineToken in self.tokens and stringFlag == 1 and lineToken != "\"":
                    stringConst += lineToken +" "
                    continue
                if lineToken in self.tokens and charFlag == 1 and lineToken != "\'":
                    charConst += lineToken
                    continue
                if lineToken in self.tokens:
                    self.pif.add(self.tokens[lineToken],0) # add token to pif
                    if lineToken =="\"" and stringFlag == 1: 
                        if self.isStringConstant(stringConst):
                            self.pif.add(2, self.constants.get(stringConst))
                        else:
                            raise Exception(f"Invalid string constant at line {lineNumber} at {lineToken}!")
                        stringFlag = 1 - stringFlag
                        stringConst = ""
                    elif lineToken == "\"" and stringFlag == 0:
                        stringFlag = 1 - stringFlag
                    
                    if lineToken == "\'" and charFlag == 1:
                        if self.isCharConstant(charConst):
                            self.pif.add(2, self.constants.get(charConst))
                        else:
                            raise Exception(f"Invalid char constant at line {lineNumber} at {lineToken}!")
                        charFlag = 1 - charFlag
                        charConst = ""
                    elif lineToken == "\'" and charFlag == 0:
                        charFlag = 1 - charFlag
                
                else:
                    if stringFlag == 1:
                        stringConst += lineToken +" "
                        continue
                    if charFlag == 1:
                        charConst += lineToken
                        continue
                    if self.isIdentifier(lineToken):
                        self.pif.add(1, self.identifiers.get(lineToken))
                    elif self.isIntegerConstant(lineToken):
                        self.pif.add(2, self.constants.get(lineToken))
                    else:
                        raise Exception(f"Invalid token at line {lineNumber} at {lineToken}!")
            lineNumber += 1
        if stringFlag == 1 or charFlag == 1:
            raise Exception(f"String or char const never closed!")      
        return self.pif, self.constants, self.identifiers


progPath = "lab3/p1err.txt"
tokensPath = "lab3/token.in"
scanner = Scanner(progPath, tokensPath)

pif, constants, identifiers = scanner.parse()
print("PIF:")
pif.display()
print("\n\n")

print("Constants:")
constants.display()
print("\n\n")

print("Identifiers:")
identifiers.display()