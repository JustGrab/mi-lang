import string
import sys
from Parser import Parser

class Token:
    def __init__(self, kind, value, line, pos):
        self.kind = kind
        self.value = value
        self.line = line
        self.pos = pos

    def toString(self):
        return f" LINE: {self.line}, POSITION: {self.pos}, KIND: {self.kind}, VALUE: {self.value}"
    
    def kind(self):
        return self.kind

    def position(self):
        return self.pos

    def value(self):
        return self.value

class Scanner:
    def __init__(self, file):
        self.Tokens = []
        self.file = file
        self.text = self.file.splitlines()
        self.keywords = ["or", "and", "not", "false", "true", "end", "bool", "int","if", "then", "else", "fi", "while", "do", "od", "print", "program"]
        self.allowedSymbols = ["=", "<", "+", "-", "*", "/", "(", ")", ";", ">", "_", ":", "!"]

        self.line = 0
        self.pos = 0
        #If file is empty, then there is nothing to read and end-of-text token is generated.
        if len(self.text) == 0:
            self.currLine = [""]
            self.Tokens.append(Token("end-of-text", None, None, None))
        else:
            self.currLine = self.text[self.line]
            
        self.error = False
        self.end = False
        self.current = ""

    def printLines(self):
        print("size of text = " + str(len(self.text)))
        print("size of line", self.line, "=", len(self.currLine))
        print(self.text)

    # If we are at end of text, end == true and current symbol is cleared
    # Increment line + 1, reset position and set text[line + 1] = to current line.
    def nextLine(self):
        if self.isEOT() == True:
            self.end == True
            self.clearCurrent()
        else:
            self.currLine = self.text[self.line]
            self.clearCurrent()
            self.pos = 0
            self.line += 1
            self.currLine = self.text[self.line]
            if len(self.currLine) == 0:
                self.nextLine()

    def clearCurrent(self):
        self.current = ""
    
    #If not end EOT, end == true, if at end of line goto next line, if not end of line then move current pos + 1 
    def advance(self):
        if self.isEOT() == True:
            self.end = True
        elif self.endOfLine() == True:
            self.nextLine()
        elif self.endOfLine() == False:
            self.pos += 1

    #Gets the next digit as long as it is a digit.
    def getDigit(self):
        if self.endOfLine() == True:
            self.nextLine()
        while self.currLine[self.pos].isdigit() and self.end == False and self.endOfLine() == False:
            self.current += self.currLine[self.pos]
            if self.lookAhead() == False:
                self.pos += 1
                break
            else:
                self.advance()

    def getIden(self):
        while (self.currLine[self.pos].isalpha() or self.currLine[self.pos].isdigit() or self.currLine[self.pos] == "_") and self.end == False and self.endOfLine() == False:
            self.current += self.currLine[self.pos]
            if self.lookAhead() == False or self.currLine[self.pos].isspace():
                self.pos += 1
                break
            else:
                self.advance()
                
    #Gets the next symbol as long as symbol is in allowed symbols
    def getSymbol(self):
        while (self.currLine[self.pos] not in string.ascii_letters and self.currLine[self.pos] not in string.digits and self.currLine[self.pos] not in string.whitespace) and self.end == False and self.endOfLine() == False:
            self.current += self.currLine[self.pos]
            if self.currLine[self.pos] not in self.allowedSymbols:
                    self.lex_error(self.line, self.pos, self.currLine[self.pos])
            if self.lookAhead() == False or self.currLine[self.pos].isspace():
                if (self.currLine[self.pos] == "!"):
                    self.lex_error(self.line, self.pos, self.currLine[self.pos])
                self.pos += 1
                break
            else:
                #If current char is ! and next char is not =, throw lex error
                if ((self.currLine[self.pos] == "!" and self.currLine[self.pos + 1] != "=")) :
                    self.lex_error(self.line, self.pos, self.currLine[self.pos])
                self.skipComment()
                self.advance()

    def skipWhite(self):
        if self.endOfLine() == True:
            self.nextLine()
        while self.currLine[self.pos-1] == string.whitespace and self.endOfLine() == False and self.end == False: 
            if self.lookAhead() == False:
                self.pos += 1
                break
            else:
                self.advance()

    def skipComment(self):
        if self.currLine[self.pos] == "/" and self.currLine[self.pos + 1] == "/" :
            if self.line == len(self.text) - 1:
                self.clearCurrent()
                self.pos = len(self.currLine[self.line]) - 1
                self.end = True
            else: 
                self.nextLine()
                self.pos -=1

    def lex_error(self, errorLine, pos, offendingChar):
        print(f"Error at Line: {errorLine + 1} Position: {pos + 1} Offending Char: {offendingChar} ")
        exit()
        

    def isEOT(self):
        if self.line == len(self.text)-1 and self.pos >= len(self.text[-1]):
            return True
        else:
            return False

    def endOfLine(self):
        if self.pos >= len(self.currLine):
            return True
        else:
            return False

    #Check to see is pos+1 is possible
    def lookAhead(self):
        if self.pos + 1 >= len(self.currLine):
            return False
        else:
            return True

    def next(self):
        self.skipWhite()
        if self.isEOT() == True or self.end == True:
            self.Tokens.append(Token("end-of-text", None, None, None))
        else:
            if self.currLine[self.pos].isalpha() or self.currLine[self.pos] == "_":
                self.getIden()
                if self.current in self.keywords:
                    self.Tokens.append(Token(str(self.current), None, self.line + 1, self.pos - len(self.current) + 1  ))
                elif self.current not in self.keywords:
                    self.Tokens.append(Token("ID", str(self.current), self.line + 1, self.pos - len(self.current) + 1  ))
            elif self.currLine[self.pos] not in string.ascii_letters and self.currLine[self.pos] not in string.digits and self.currLine[self.pos] not in string.whitespace :
                    self.getSymbol()
                    if self.current != "":
                        self.Tokens.append(Token(str(self.current), None, self.line + 1, self.pos - len(self.current) + 1 ))
            elif self.currLine[self.pos].isdigit() == True:
                self.getDigit()
                self.Tokens.append(Token("NUM", str(self.current), self.line + 1, self.pos - len(self.current) + 1))
            else:
                self.advance()
                
        self.clearCurrent()


if __name__ == "__main__":
    file = sys.argv[1]
    file = open(str(file))
    
    scanner = Scanner(file.read())
    #Temporary start token, does not affect list of tokens
    currentToken = Token("START","START","START","START")

    while(currentToken.kind != "end-of-text"):
        scanner.next()
        #if list of tokens in scanner class is not 0, then set current token equal to the last token in the scanner token list
        if len(scanner.Tokens) != 0:
            currentToken = scanner.Tokens[-1]

    file.close()
    tokens = scanner.Tokens
    for i in range(len(tokens)):
        print(tokens[i].toString())

#Begin parsing 
print("\nParsing...")
par = Parser(tokens)
par.parse()
print("Parsing Successful!")


