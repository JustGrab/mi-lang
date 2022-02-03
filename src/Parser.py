class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentSymb = tokens[0].kind
        self.tokenCounter = 0

        #If list of tokens only contains end-of-text token, file is empty.
        if len(tokens) == 1:
            print("File Empty")
            exit()

    def parse(self):
        self._program()

    def _accept(self, symbol):
        if self.currentSymb == symbol:
            self._nextSymb()
        else:
            print(f"Error! Current symbol is: '{self.currentSymb}'. Expected symbol is: '{symbol}'")
            exit()

    def _expected(self, expectedList):
        if self.currentSymb not in expectedList:
            print("ERROR, Current Symbol is ", self.currentSymb, ", Expecting ", expectedList)
            exit()

    def _nextSymb(self):
        self.tokenCounter = self.tokenCounter + 1
        self.currentSymb = self.tokens[self.tokenCounter].kind

    def _program(self):
        self._accept("program")
        self._accept("ID")
        self._accept(":")
        self._body()
        self._accept("end")

    def _body(self):
        if self.currentSymb in ["bool","int"]:
            self._declarations()
        self._statements()
    
    def _declarations(self):
        self._declaration()
        while self.currentSymb in ["bool", "int"]:
            self._declaration()

    def _declaration(self):
        assert self.currentSymb in ["bool", "int"]
        self._nextSymb()
        self._accept("ID")
        self._accept(";")

    def _statements(self):
        self._statement()
        while self.currentSymb == ";":
            self._nextSymb()
            self._statement()

    def _statement(self):
        if self.currentSymb == "ID":
            self._assignmentStatement()
        elif self.currentSymb == "if":
            self._conditionalStatement()
        elif self.currentSymb == "while":
            self._iterativeStatement()
        elif self.currentSymb == "print":
            self._printStatement()
        else:
            self._expected(["ID", "if", "while", "print"])

    def _assignmentStatement(self):
        assert self.currentSymb == "ID"
        self._accept("ID")
        self._accept(":=")
        self._expression() 

    def _conditionalStatement(self):
        assert self.currentSymb == "if"
        self._accept("if")
        self._expression()
        self._accept("then")
        self._body()
        if self.currentSymb == "else":
            self._nextSymb()
            self._body()
        self._accept("fi")

    def _iterativeStatement(self):
        self._accept("while")
        self._expression()
        self._accept("do")
        self._body()
        self._accept("od")

    def _printStatement(self):
        assert self.currentSymb == "print"
        self._accept("print")
        self._expression()

    def _expression(self):
        self._simpleExpression()
        if self.currentSymb in ["<",  "=<", "=", "!=", ">=", ">"]:
            self._nextSymb()
            self._simpleExpression()

    def _simpleExpression(self):
        self._term()
        while(self.currentSymb in ["+", "-", "or"]):
            self._nextSymb()
            self._term()

    def _term(self):
        self._factor()
        while self.currentSymb in ["*", "/", "and"]:
            self._nextSymb()
            self._factor()
        
    def _factor(self):
        if self.currentSymb in ["-", "not"]:
            self._nextSymb()
        if self.currentSymb in ["true", "false", "NUM"]:
            self._literal()
        elif self.currentSymb == "ID":
            self._nextSymb()
        elif self.currentSymb == "(":
            self._nextSymb()
            self._expression()
            self._accept(")")
        else:
            self._expected(["true", "false", "NUM", "ID", "("])
    
    def _literal(self):
        assert self.currentSymb in ["false", "true", "NUM"]
        if self.currentSymb == "NUM":
            self._nextSymb()
        else:
            self._booleanLiteral()


    def _booleanLiteral(self):
        assert self.currentSymb in ["true", "false"]
        self._nextSymb()
