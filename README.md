# Mi-Lang
Mi-Lang is a mini interpreted language that follows an [LL(1)](https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node14.html) grammar. The language includes a lexical analyzer, parser written in python and an interpreter written in emacs lisp. 
The language's EBNF grammar which can be seen in grammar.txt.



# Program Example 
```
// Euclid's algorithm for the greatest common divisor.
program GCD:
   int a;  int b;
   a := 15;
   b := 20;
   print a;  print b;
   while a != b do
      if a < b then b := b - a
      else a := a - b
      fi
   od;
   print a
end
```
More examples can be found in /examples.

# Lexaical Analysis
Breaks down the provided inputted file into tokens. Tokens consists of their name, token type, line number, and position number. If there is an unrecognized symbol in file, a lexical error will be thrown and analysis will end. These tokens will then be used in the parser.

# Parser
The parser is a top down parser that works at the highest level of the parse tree and then works it way down. This parser was chosen for this language because it follows LL(1) grammar. The parser currently does not generate abtract syntax trees, though some are provided in /ast.

# Interpreter
The interpreter is an [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) interpreter written in emacs lisp that parses through the ASTs and outputs a working program written in Mi-Lang.
