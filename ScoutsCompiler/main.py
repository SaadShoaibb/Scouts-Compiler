import re
import os

literals = [
    'intConst',
    'stringConst', 'floatConst', 'charConst', 'boolConst'
]

lexemeClass = [
    'keyword', 'ID', 'intConst',
    'OP', 'comma', 'stringConst', 'floatConst', 'charConst', 'DT', 'boolConst'
]
# The above constants are used in the code for token types and constant values.

# path=input("Enter the path :")
#path = "(add path here).txt"
#codeobj = open(path, "r")
#source_code = codeobj.read()

source_code="""
#include <iostream>
using namespace std;

int main() {
    int x = 5;
    int y = 5;
    if (x < y) {
        cout << x << "is the greatest";
    }
    if (y > x){
        cout << y << "is the greatest";
    }
    else {
        cout << x <<" , " << y << "are equal";
    }


    return 0;
}
"""
# The above variable 'blank_var' contains a C++ code snippet as a multi-line string.

# Here, the import statement for the 're' module is used for regular expression matching.

# The following code defines constants for various token types and constant values.

# The 'blank_var' variable contains a C++ code snippet that will be analyzed by the lexer and parser.

# The lexer and parser logic will be implemented here.

# Remove single-line comments (//...) and track line numbers


single_line_comments = []
source_code = re.sub(r'//(.*)',
                     lambda m: single_line_comments.append((m.group(1), source_code.count('\n', 0, m.start()))),
                     source_code)

# Remove multi-line comments (/*...*/) and track line numbers
multi_line_comments = []
source_code = re.sub(r'/\*.*?\*/',
                     lambda m: multi_line_comments.append((m.group(0), source_code.count('\n', 0, m.start()))),
                     source_code, flags=re.DOTALL)

print("INPUT FILE:\n", source_code)

# Regular expressions to find different elements in a string
integers = re.findall('^[0-9]+$|[0-9]+', source_code)  # Find all integer numbers
floatn = re.findall(r'[0-9]+\.[0-9]+', source_code)  # Find all floating-point numbers
chars = re.findall(r'\'[^\'\\\.]\'', source_code)  # Find all single characters

# Dictionary mapping tokens to their categories
tokenDict = {
    '=': 'assgOP',
    '&': 'passByRef',
    '<': 'lt',
    '>': 'gt',
    '++': 'increment',
    '--': 'decrement',
    '+': 'plus',
    '-': 'minus',
    '*': 'multiply',
    '/': 'divide',
    '>=': 'gET',
    '<=': 'lET',
    '(': 'L_round_bracket',
    ')': 'R_round_bracket',
    '{': 'L_curly_bracket',
    '}': 'R_curly_bracket',
    '[': 'L_square_bracket',
    ']': 'R_square_bracket',
    ',': 'COMMA',
    '"': 'doubleQuote',
    '\'': 'singleQuote',
    ';': 'terminator',
    '#': 'sharp',
    '&&': 'L_and',
    '!': 'L_Not',
    '||': 'L_OR',
    '<<': 'L_shift',
    '>>': 'R_shift',
    '==': 'eq',
    ':': 'colon'

}

# List of reserved keywords in the programming language
KeyWords = ["if", "else", "while", "do", "for", "cout", "cin", "return", "switch", "case", "break", "function", "enum",
            "using", "namespace", "include", "endl", "default", "return"]

# List of different types of brackets
bracket = ['(', ')', '{', '}', '[', ']']

# List of different data types
datatype = ["int", "float", "char", "string", "bool", "short", "long", "void"]

# List of punctuators
punctuator = [',', ';', ':', ',']

# List of arithmetic operators
artOp = ['-', '+', '*', '/', '%']

# List of logical operators
logOp = ['||', '&&']

# List of single logical operators
slogop = ['!']

# List of assignment operators
asgOp = ['=']

# List of single comparison operators
sinlop = ['<', '>']

# List of relational operators
relOp = ['<=', '>=', '!=', '==', "<<", ">>"]

# List of increment/decrement operators
incr = ['++', '--']

# List of boolean constants
boolConst = ['True', 'False']


class LexStream:
    # initialize a single linked list, for first pass of lexer
    def __init__(self, value, line_numbers, type):
        self.data = {
            "value": value,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type
        }  # Assign data
        self.next = None  # Initialize next as null


class ParseStream:
    #initialize a double linked list, for
    def __init__(self, name, line_numbers, type, scope):
        self.data = {
            "Name": name,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type,
            "Scope": scope
        }  # Assign data
        self.next = None  # Initialize next as null
        self.prev = None  # Initialize prev as null


class SymbolTable:


    # Constructor for symbol table
    def __init__(self):
        self.head = None

    def push(self, name, line_numbers, type, scope):
        # Insert a new node at the beginning of the list
        new_node = ParseStream(name, line_numbers, type, scope)
        new_node.next = self.head
        new_node.prev = None

        if self.head is not None:
            self.head.prev = new_node

        self.head = new_node

    def printList(self):
        # Print the data of all nodes in the symbol table
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next

    def FindData(self, name):
        # Find the data associated with a given name in the symbol table
        node = self.head
        while node is not None:
            if node.data['Name'] == name:
                return node.data
            node = node.next
        return False


class LexerProc:
    #helper for lexer class, adds new node at end of lexstream
    def __init__(self):
        self.head = None


    def append(self, value, line_numbers, type):


        new_node = LexStream(value, line_numbers, type)

        if self.head is None:
            self.head = new_node
            return

        last = self.head
        while (last.next):
            last = last.next

        last.next = new_node

    def printList(self):
        temp = self.head
        while (temp):
            print(temp.data),
            temp = temp.next


class Token(object):

    def __init__(self, pos, value, linenumber):
        self.type = tokenDict[value] if (pos == 3 or pos == 4) else lexemeClass[pos]
        self.value = value
        self.line_number = linenumber



class Lexer(object):

    def __init__(self):
        self.tokens = []
        self.count = 1
        self.temp = ''
        self.sym = SymbolTable()

    def is_blank(self, index):
        return (source_code[index] == ' ')

    def is_Escape(self, index):
        return (source_code[index] == '\t' or source_code[index] == '\n' or source_code[index] == '\r')

    def line_break(self, index):
        return (source_code[index] == '\n' or source_code[index] == '\t' or source_code[index] == '\b' or source_code[
            index] == ' ')

    def skip_blank(self, index, stringflag):
        while index < len(source_code) and self.is_blank(index):
            index += 1
        return index

    def print_log(self, style, value):
        print(style, value)

    def analyze_code(self, code):
        words = re.findall(r'\b\w+\b', code)  # Find all words in the code

        for word in words:
            value_type = self.get_value_type(word)
            self.sym.push(word, self.count, value_type, word)

    def get_value_type(self, value):
        # Check if the value is a keyword
        if value in KeyWords:
            return "keyword"

        # Check if the value is a bracket
        if value in bracket:
            return "bracket"

        # Check if the value is a data type
        if value in datatype:
            return "dataType"

        # Check if the value is a punctuator
        if value in punctuator:
            return "punctuator"

        # Check if the value is an arithmetic operator
        if value in artOp:
            return "artithmeticOp"

        # Check if the value is a logical operator
        if value in logOp:
            return "logicalOp"

        # Check if the value is a single logical operator
        if value in slogop:
            return "singlelogicalOp"

        # Check if the value is an assignment operator
        if value in asgOp:
            return "assignmentOp"

        # Check if the value is a single comparison operator
        if value in sinlop:
            return "singleComparisonOp"

        # Check if the value is a relational operator
        if value in relOp:
            return "relationalOp"

        # Check if the value is an increment/decrement operator
        if value in incr:
            return "incrementOp"

        # Check if the value is a boolean constant
        if value in boolConst:
            return "booleanConst"

        # If none of the above conditions match, return "UNKNOWN"
        return ""

    def checkforiden(self, scope):
        # Check if the temporary string represents an identifier and add it as a token
        if self.temp != '':
            i = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', self.temp)

            if self.temp in i:
                self.tokens.append(Token(1, self.temp, self.count))  # Add token to the list

                # Check if the identifier has an explicit value assigned in the code
                pattern = r'\b' + self.temp + r'\s*=\s*(.*?)(;|$)'
                matches = re.findall(pattern, source_code)
                if matches:
                    value = matches[0]

                    self.sym.push(self.temp, self.count, self.get_value_type(value), scope)
                else:
                    self.sym.push(self.temp, self.count, "NOT DEFINED", "NOT DEFINED")

                self.temp = ''  # Reset temporary string

    def is_keyword(self, value):
        # Check if the given value is a keyword
        for item in KeyWords:
            if value in item:
                return True
        return False

    def main(self):
        i = 0
        scope = 0
        strf = False

        while i < len(source_code):
            if (source_code[i] == ' '):
                self.checkforiden(scope)
                i = i + 1
                continue
            if source_code[i] == '\n':
                self.checkforiden(scope)
                self.count = self.count + 1
                i = i + 1
                continue
            if source_code[i] == '#':
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
                i = i + 1
                continue
            # Check for logical operators
            elif source_code[i:i + 2] in logOp:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i:i + 2], self.count))
                i = i + 1
            # Check for relational operators
            elif source_code[i:i + 2] in relOp:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i:i + 2], self.count))
                i = i + 1
            # Check for increment operators
            elif source_code[i:i + 2] in incr:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i:i + 2], self.count))
                i = i + 1
            elif source_code[i] in bracket:
                if source_code[i] == "{":
                    scope+=1
                elif source_code[i] == "}":
                    scope-=1
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            elif source_code[i] in punctuator:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            elif source_code[i] in sinlop:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            elif source_code[i] in asgOp:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            elif source_code[i] in slogop:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            elif source_code[i] in artOp:
                self.checkforiden(scope)
                self.tokens.append(Token(3, source_code[i], self.count))
            else:
                self.temp = self.temp + source_code[i]

                if (source_code[i] == '"'):
                    # Check for string literals
                    if (self.temp == '"'):
                        self.temp = ''
                        i = i + 1
                        strf = True
                        while i < len(source_code) and source_code[i] != '"':
                            if (source_code[i:i + 2] == "\\t"):
                                self.temp = self.temp + '\t'
                                i = i + 2
                            elif (source_code[i:i + 2] == "\\n"):
                                self.temp = self.temp + '\n'
                                i = i + 2
                            else:
                                self.temp = self.temp + source_code[i]
                                i = i + 1
                            if (i == len(source_code) or i > len(source_code)):
                                print(
                                    f"... ERROR: UNABLE TO RUN FILE {os.path.abspath('sample.cpp')}  \n STRING QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {self.temp} ")
                                exit()
                        if (len(self.temp) > 0):
                            self.tokens.append(Token(5, self.temp, self.count))
                            strf = False
                            self.temp = ''
                        i = i + 1
                        continue

                if (self.temp in integers):
                    if (source_code[i + 1] != '.' and source_code[i + 1] not in re.findall('[0-9]', source_code)):
                        j = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', source_code[i + 1])
                        if (source_code[i + 1] not in j):
                            self.tokens.append(Token(2, self.temp, self.count))
                            integers.pop(integers.index(self.temp))
                            self.temp = ''

                # Check if the temporary value is a keyword
                elif (self.temp in KeyWords):
                    self.tokens.append(Token(0, self.temp, self.count))
                    self.temp = ''

                # Check if the temporary value is a data type
                elif (self.temp in datatype):
                    self.tokens.append(Token(8, self.temp, self.count))
                    self.temp = ''

                # Check if the temporary value is a boolean constant
                elif (self.temp in boolConst):
                    self.tokens.append(Token(9, self.temp, self.count))
                    self.temp = ''

                # Check if the temporary value is a float number
                elif (self.temp in floatn):
                    self.tokens.append(Token(6, self.temp, self.count))
                    self.temp = ''

                if (source_code[i] == '\''):
                    self.temp = ''
                    i = i + 1
                    if (source_code[i] == '\''):
                        self.temp = ''
                        i = i + 1
                        continue
                    elif (source_code[i:i + 2] == '\\n' or source_code[i:i + 2] == '\\t' or ord(source_code[i])):
                        if (source_code[i:i + 2] == '\\n' or source_code[i:i + 2 == '\\t']):
                            if (source_code[i + 2] == '\''):
                                self.tokens.append(Token(7, source_code[i:i + 2], self.count))
                                self.temp = ''
                                i = i + 2
                                i = i + 1
                                continue
                            else:
                                print(
                                    f"... ERROR: UNABLE TO RUN FILE  {os.path.abspath('sample.cpp')}  \n CHARACTER QUOTES NOT CLOSED IN LINE NUMBER: {self.count}  {source_code[i]} ")
                                exit()
                        else:
                            if (source_code[i + 1] == '\''):
                                self.tokens.append(Token(7, source_code[i], self.count))
                                self.temp = ''
                                i = i + 1
                    else:
                        print(
                            f"... ERROR: UNABLE TO RUN FILE  {os.path.abspath('sample.cpp')}  \n CHARACTER DECLARATION NOT VALID IN LINE NUMBER: {self.count} {source_code[i]} ")
                        exit()
            i = i + 1
            continue


class parser:
    def __init__(self, tok):
        self.tok = tok.head
        self.lookahead = None

    def nextToken(self):
        if (self.lookahead == None):
            return self.tok
        else:
            self.tok = self.tok.next
            return self.tok

    def includestmt(self):
        data = self.lookahead.data['value']
        if (data == '#'):
            self.match("#")  # Match the "#" token
            self.match("include")  # Match the "include" token
            self.match("<")  # Match the "<" token
            self.matchID(self.lookahead.data['TYPE'])  # Match an identifier token
            self.match('>')  # Match the ">" token
        else:
            print("ERROR IN INCLUDE STMT")

    def includelist_(self):
        data = self.lookahead.data['value']
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        elif (data in ['$', "using"]):
            return
        else:
            print("ERROR IN INCLUDE LIST _")

    def includelist(self):
        data = self.lookahead.data['value']
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        else:
            print("ERROR IN INCLUDE LIST")

    def namespace(self):
        data = self.lookahead.data['value']
        if (data == 'using'):
            self.match('using')  # Match the "using" token
            self.match('namespace')  # Match the "namespace" token
            self.matchID(self.lookahead.data["TYPE"])  # Match an identifier token
            self.match(';')  # Match the ";" token
        else:
            print("ERROR IN NAMESPACE")

    def start(self):
        data = self.lookahead.data['value']
        if (data == '#'):
            self.includelist()
            self.namespace()
            self.program()
        elif (data == "$"):
            return
        else:
            print("ERROR IN START")

    def vardeclist_(self):
        data = self.lookahead.data['value']
        if (data == ','):
            self.match(',')  # Match the "," token
            self.vardecinit()
            self.vardeclist_()
        elif (data == ';'):
            return
        else:
            print("ERROR IN VARRAIBLE dec list _")

    def vardecid(self):
        data = self.lookahead.data['value']
        if (self.lookahead.data["TYPE"] == "ID"):
            self.matchID(self.lookahead.data["TYPE"])  # Match an identifier token
            self.vardecid_()
        else:
            print("ERROR IN VARDEC ID")

    def vardecid_(self):
        data = self.lookahead.data['value']
        if (data == '['):
            self.match('[')  # Match the "[" token
            if (self.lookahead.data['TYPE'] == 'intConst'):
                self.lookahead = self.nextToken()
                self.match(']')  # Match the "]" token
            else:
                print("ERROR: NOT A CONTS")
        elif (data == ',' or data == ';' or data == '='):
            return
        else:
            print("EROR")

    def relop(self):
        data = self.lookahead.data['value']
        if (data == '<='):
            self.match('<=')  # Match the "<=" token
        elif (data == '<'):
            self.match('<')  # Match the "<" token
        elif (data == '>'):
            self.match('>')  # Match the ">" token
        elif (data == '>='):
            self.match('>=')  # Match the ">=" token
        elif (data == '=='):
            self.match('==')  # Match the "==" token
        elif (data == '!='):
            self.match('!=')  # Match the "!=" token
        else:
            print("ERROR IN RELOP !")

    def expression(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        data_next = self.lookahead.next
        if (self.lookahead.data["TYPE"] == "ID" and data_next.data["value"] == "++"):
            self.matchID(self.lookahead.data["TYPE"])  # Match an identifier token
            self.match("++")  # Match the "++" token
        elif (self.lookahead.data["TYPE"] == "ID" and data_next.data["value"] == "--"):
            self.matchID(self.lookahead.data["TYPE"])  # Match an identifier token
            self.match("--")  # Match the "--" token
        elif (self.lookahead.data["TYPE"] == "ID" and data_next.data["value"] == "="):
            self.matchID(self.lookahead.data["TYPE"])  # Match an identifier token
            self.match("=")  # Match the "=" token
            self.expression()
        elif (data == '!' or self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data[
            'TYPE'] in CONST):
            self.simpleExp()
        else:
            print("ERROR IN EPRESSION")

    def arglist_(self):
        data = self.lookahead.data['value']
        if (data == ','):
            self.match(',')  # Match the "," token
            self.expression()  # Call the expression method
            self.arglist_()  # Recursively call arglist_ to process the remaining arguments
        elif (data == ')'):
            return  # Return if the next token is ")"
        else:
            print("ERROR IN ARG LIST _")

    def arglist(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data[
            'TYPE'] in CONST):
            self.expression()  # Call the expression method
            self.arglist_()  # Call arglist_ to process the remaining arguments
        else:
            print("ERROR IN ARG LIST")

    def args(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data[
            'TYPE'] in CONST):
            self.arglist()  # Call the arglist method to process the arguments
        elif (data == ')'):
            return  # Return if the next token is ")"
        else:
            print("ERROR IN ARGS")

    def constants(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] in CONST):
            self.lookahead = self.nextToken()  # Move to the next token
        else:
            print("ERROR IN CONSTANTS")

    def factor_(self):
        data = self.lookahead.data['value']

        if (data == '('):
            self.match('(')  # Match the "(" token
            self.args()  # Call the args method to process the arguments
            self.match(')')  # Match the ")" token
        elif (
                data == '*' or data == '/' or data == '%' or data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data == "||" or data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN FACTOR _ " + data)

    def factor(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] == 'ID'):
            self.matchID(self.lookahead.data['TYPE'])  # Match an identifier token
            self.factor_()  # Call factor_ to process the remaining factor
        elif (data == '('):
            self.match('(')  # Match the "(" token
            self.expression()  # Call the expression method
            self.match(')')  # Match the ")" token
        elif (self.lookahead.data['TYPE'] in CONST):
            self.constants()  # Call the constants method
        else:
            print("ERROR IN FACTOR")

    def unaryExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.factor()  # Call the factor method
        else:
            print("ERROR IN UNARY EXP")

    def mulOp(self):
        data = self.lookahead.data['value']
        if (data == '*'):
            self.match('*')  # Match the "*" token
        elif (data == '/'):
            self.match('/')  # Match the "/" token
        elif (data == '%'):
            self.match('%')  # Match the "%" token
        else:
            print("ERROR WITH MULOP")

    def mulExp_(self):
        data = self.lookahead.data['value']

        if (data == '*' or data == '/' or data == '%'):
            self.mulOp()  # Call the mulOp method to handle the multiplication operator
            self.unaryExp()  # Call the unaryExp method to handle the next factor
            self.mulExp_()  # Recursively call mulExp_ to process the remaining multiplication expressions
        elif (
                data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data == "||" or data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN MUL EXP _")

    def sumOP(self):
        data = self.lookahead.data['value']
        if (data == '+'):
            self.match('+')  # Match the "+" token
        elif (data == '-'):
            self.match('-')  # Match the "-" token
        else:
            print("ERROR IN SUM OP")

    def sumExp_(self):
        data = self.lookahead.data['value']
        if (data == '+' or data == '-'):
            self.sumOP()  # Call the sumOP method to handle the addition/subtraction operator
            self.mulExp()  # Call the mulExp method to handle the next term
            self.sumExp_()  # Recursively call sumExp_ to process the remaining sum expressions
        elif (
                data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data == "||" or data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN SUM EXP_")

    def mulExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.unaryExp()  # Call the unaryExp method to handle the first factor
            self.mulExp_()  # Call mulExp_ to process the remaining multiplication expressions
        else:
            print("ERROR IN SUM EXP_")

    # i have to add comments heree

    def sumExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.mulExp()  # Call the mulExp method to handle the first term
            self.sumExp_()  # Call sumExp_ to process the remaining sum expressions
        else:
            print("ERROR IN SUM EXP")

    def relExp_(self):
        data = self.lookahead.data['value']
        if (data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!='):
            self.relop()  # Call the relop method to handle the relational operator
            self.sumExp()  # Call the sumExp method to handle the next term
            self.relExp_()  # Recursively call relExp_ to process the remaining relational expressions
        elif (data == '||' or data == '&&' or data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN REL EXP")

    def relExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.sumExp()  # Call the sumExp method to handle the first term
            self.relExp_()  # Call relExp_ to process the remaining relational expressions
        else:
            print("ERROR IN REL EXP")

    def unaryRelExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (data == '!'):
            self.match('!')  # Match the "!" token
            self.unaryRelExp()  # Recursively call unaryRelExp to handle the negation operator
        elif (self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.relExp()  # Call the relExp method to handle the relational expression
        else:
            print("ERROR IN UNARY REL EXP")

    def andExp_(self):
        data = self.lookahead.data['value']
        if (data == '&&'):
            self.match("&&")  # Match the "&&" token
            self.unaryRelExp()  # Call the unaryRelExp method to handle the next relational expression
            self.andExp_()  # Recursively call andExp_ to process the remaining AND expressions
        elif (data == '||' or data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN AND EXP _")

    def andExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data[
            'TYPE'] in CONST):
            self.unaryRelExp()  # Call the unaryRelExp method to handle the first relational expression
            self.andExp_()  # Call andExp_ to process the remaining AND expressions
        else:
            print("ERROR IN AND EXP")

    def SimpleExp_(self):
        data = self.lookahead.data['value']
        if (data == '||'):
            self.match('||')  # Match the "||" token
            self.andExp()  # Call the andExp method to handle the next AND expression
            self.SimpleExp_()  # Recursively call SimpleExp_ to process the remaining OR expressions
        elif (data == ',' or data == ';' or data == ')' or data == "<<"):
            return  # Return if the next token is one of the specified tokens
        else:
            print("ERROR IN SIMPLE EXP _")

    def simpleExp(self):
        data = self.lookahead.data['value']
        CONST = [
            'intConst',
            'stringConst',
            'floatConst',
            'charConst',
            'boolConst'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'ID' or data == '(' or self.lookahead.data[
            'TYPE'] in CONST):
            self.andExp()  # Call the andExp method to handle the first AND expression
            self.SimpleExp_()  # Call SimpleExp_ to process the remaining OR expressions
        else:
            print("ERROR IN SIMPLE EXP")

    def vardecinit_(self):
        data = self.lookahead.data['value']
        if (data == '='):
            self.match('=')  # Match the "=" token
            self.simpleExp()  # Call the simpleExp method to handle the initialization expression
        elif (data == ',' or data == ';'):
            return  # Return if the next token is a comma or semicolon
        else:
            print("ERROR IN VARDECINIT_")

    def vardecinit(self):
        data = self.lookahead.data['value']
        if (self.lookahead.data["TYPE"] == "ID"):
            self.vardecid()  # Call the vardecid method to handle the variable declaration
            self.vardecinit_()  # Call vardecinit_ to handle the initialization (if present)
        else:
            print("ERROR IN VARIABLE INIT")

    def vardeclist(self):
        data = self.lookahead.data['value']
        if (self.lookahead.data["TYPE"] == "ID"):
            self.vardecinit()  # Call the vardecinit method to handle the variable declaration and initialization
            self.vardeclist_()  # Call vardeclist_ to process the remaining variable declarations
        else:
            print("ERROR IN VARIABLE DECLIST")

    def variable(self):
        data = self.lookahead.data['value']
        if (self.lookahead.data["TYPE"] == "ID"):
            self.vardeclist()  # Call the vardeclist method to handle the first variable declaration
            self.match(';')  # Match the semicolon token
        else:
            print("ERROR IN VARIABLE ONLY")

    def declaration__(self):
        data = self.lookahead.data['value']
        data_next = self.lookahead.next
        if (self.lookahead.data['TYPE'] == "ID" and data_next.data['value'] == '('):
            self.function()  # Call the function method to handle function declaration
        elif (self.lookahead.data['TYPE'] == "ID"):
            self.variable()  # Call the variable method to handle variable declaration
        else:
            print("ERROR IN DECLARATION__")

    def declaration(self):
        data = self.lookahead.data['value']
        if (data in datatype):
            self.typeid()  # Call the typeid method to handle the data type identifier
            self.declaration__()  # Call declaration__ to process the remaining declaration tokens
        else:
            print("ERROR: IN declaration FUNCTION")

    def declaration_(self):
        data = self.lookahead.data['value']
        if (data in datatype):
            self.declaration()  # Call the declaration method to handle the declaration
            self.declaration_()  # Recursively call declaration_ to process the remaining declarations
        elif (data == '$'):
            return  # Return if the next token is the end marker
        else:
            print("ERROR: IN declaration_ FUNCTION")

    def declist(self):
        # Get the current value
        data = self.lookahead.data['value']

        if (data in datatype):
            self.declaration()
            self.declaration_()
        else:
            # Print error message if the data is not in datatype
            print("ERROR: IN declist FUNCTION")

    def program(self):
        # Get the current value
        data = self.lookahead.data['value']

        if (data in datatype):
            self.declist()
        elif (data == '$'):
            # Return if data is '$'
            return
        else:
            # Print error message for unknown value in program function
            print("ERROR: IN PROGRAM FUNCTION")

    def function(self):
        # Get the current value
        data = self.lookahead.data['value']

        if (self.lookahead.data['TYPE'] == 'ID'):
            self.matchID(self.lookahead.data['TYPE'])
            self.match('(')
            self.paramas()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif (data == '$'):
            # Return if data is '$'
            return
        else:
            # Print error message for unknown value in function syntax
            print("ERROR IN FUNCTION SYNTAX TOKEN: ", self.lookahead.data)
            exit()

    def stmtlist(self):
        # Get the current value
        data = self.lookahead.data['value']

        CONST = [
            'intConst',
            'stringConst', 'floatConst', 'charConst', 'boolConst'
        ]
        if (data in ['!', '(', 'if', 'cout', 'cin', 'while', 'for', 'switch', 'return', 'break', '//',
                     '*/'] or data in datatype or
                self.lookahead.data["TYPE"] in ["ID", CONST]):
            self.statment()
            self.stmtlist_()
        else:
            # Print error message for unknown value in stmtlist
            print("ERROR IN STMTLIST")

    def iteration(self):
        # Get the current value
        data = self.lookahead.data['value']

        if (data == 'for'):
            self.match('for')
            self.match('(')
            self.vardecinit()
            self.match(';')
            self.simpleExp()
            self.match(';')
            self.expression()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif (data == "while"):
            self.match("while")
            self.match("(")
            self.simpleExp()
            self.match(")")
            self.match("{")
            self.stmtlist()
            self.match("}")
        else:
            # Print error message for unknown value in iteration
            print('ERROR IN ITERETION')

    def switch(self):
        # Get the current value
        data = self.lookahead.data["value"]

        if (data == "switch"):
            self.match("switch")
            self.match("(")
            self.simpleExp()
            self.match(")")
            self.match("{")
            self.caselist()
            self.default()
            self.match("}")
        else:
            # Print error message for unknown value in switch
            print("Error in SWITCH")

    def caselist(self):
        data = self.lookahead.data["value"]
        if (data == "case"):
            self.onecase()
            self.caselist()
        elif (data == "default" or data == "}"):
            return
        else:
            print("ERROR IN CASELIST")

    def onecase(self):
        data = self.lookahead.data["value"]
        if (data == "case"):
            self.match("case")
            if (self.lookahead.data["TYPE"] in literals):
                self.lookahead = self.nextToken()
                self.match(":")
                self.stmtlist()
            else:
                print("ERROR IN CONSTANTS IN SWITCH CASE")
        else:
            print("ERROR IN ONE CASE")

    def default(self):
        data = self.lookahead.data["value"]
        if (data == "default"):
            self.match("default")
            self.match(":")
            self.stmtlist()
        elif (data == "}"):
            return
        else:
            print("ERROR IN DEFAULT")

    def selection(self):
        data = self.lookahead.data["value"]
        if (data == "if"):
            self.match("if")
            self.match("(")
            self.simpleExp()
            self.match(")")
            self.match("{")
            self.stmtlist()
            self.match("}")
            self.selection_()
        else:
            print("ERROR IN SELECTION: " + data)

    def selection_(self):
        data = self.lookahead.data["value"]
        if (data == ";"):
            self.match(";")
        elif (data == "else"):
            self.match("else")
            self.match("{")
            self.stmtlist()
            self.match("}")
        else:
            print("ERROR IN IF CONDITION: TOKEN " + data)
            exit()

    def statment(self):
        data = self.lookahead.data['value'];
        if (data in ['for', 'while']):
            self.iteration()
        elif (data in ['return']):
            self.returnstmt()
        elif (data in ['if']):
            self.selection()
        elif (data in ['switch']):
            self.switch()
        elif (data in ['break']):
            self.match("break")
            self.match(";")
        elif (data == "continue"):
            self.match("continue")
            self.match(";")
        elif (data in ["cin", "cout"]):
            self.input_output()
        elif (data in datatype):
            self.declaration()
        elif (data in ['!', '('] or self.lookahead.data["TYPE"] in ["ID", literals]):
            self.expression()
            self.match(";")
        else:
            print("ERROR IN STATEMENT")

    def printlist(self):
        data = self.lookahead.data["value"]
        if (data == "<<"):
            self.single()
            self.printlist_()
        else:
            print("ERROR IN PRINTLIST :")

    def single(self):
        data = self.lookahead.data["value"]
        if (data == "<<"):
            self.match("<<")
            self.expression()
        else:
            print("ERROR IN SINGLE: ")

    def printlist_(self):
        data = self.lookahead.data["value"]
        data_next = self.lookahead.next
        if (data == "<<" and data_next.data["value"] not in ["endl"]):
            self.single()
            self.printlist_()
        elif (data == "<<" or data == ";"):
            return
        else:
            print("ERROR IN PRINTLIST_")

    def endstmt(self):
        data = self.lookahead.data["value"]
        if (data == "<<"):
            self.match("<<")
            self.match("endl")
            self.match(";")
        elif (data == ";"):
            self.match(";")
        else:
            print("ERROR IN ENDSTMT")

    def input_output(self):
        data = self.lookahead.data["value"]
        if (data == "cout"):
            self.match("cout")
            self.printlist()
            self.endstmt()
        elif (data == "cin"):
            self.match("cin")
            self.inputlist()
            self.match(";")
        else:
            print("ERROR IN INPUT_OUTPUT TOKEN: " + self.lookahead.data)

    def inputlist(self):
        data = self.lookahead.data["value"]
        if (data == ">>"):
            self.singleinput()
            self.inputlist_()
        else:
            print("ERROR IN INPUTLIST")

    def inputlist_(self):
        data = self.lookahead.data["value"]
        if (data == ">>"):
            self.singleinput()
            self.inputlist_()
        elif (data == ";"):
            return;
        else:
            print("ERROR IN INPUTLIST_")

    def singleinput(self):
        data = self.lookahead.data["value"]
        if (data == ">>"):
            self.match(">>")
            self.matchID(self.lookahead.data["TYPE"])
        else:
            print("ERROR IN SINGLEINPUT:")

    def stmtlist_(self):
        data = self.lookahead.data['value'];

        if (data in ['!', '(', 'cout', 'cin', 'if', 'while', 'for', 'switch', 'return', 'break'] or data in datatype or
                self.lookahead.data["TYPE"] in ["ID", literals]):
            self.statment()
            self.stmtlist_()
        elif (data in ['}'] or data == "default"):
            return
        else:
            print("ERROR IN STMTLIST_" + data)

    def returnstmt(self):
        data = self.lookahead.data['value'];
        if (data == 'return'):
            self.match('return')
            self.expression()
            self.match(';')
        elif (data == '}'):
            return
        else:
            print("ERROR IN STATEMENT: ", self.lookahead.data)
            exit()

    def data(self):
        value = self.lookahead.data['TYPE'];
        data = self.lookahead.data['value'];
        conslist = ['intConst', 'stringConst', 'floatConst', 'charConst', 'boolConst']
        if (value in conslist):
            self.lookahead = self.nextToken()

        elif (data == ';'):
            return
        else:
            print("ERROR IN RETURN DATA: ", self.lookahead.data)
            exit()

    def paramas(self):
        data = self.lookahead.data['value'];
        if (data in datatype):
            self.paralist()
        elif (data == ')'):
            return
        else:
            print("ERROR WITH PARAMETERS: ", self.lookahead.data)
            exit()

    def paralist(self):
        data = self.lookahead.data['value'];
        if (data in datatype):
            self.parameter()
            self.paralist_()
        else:
            print("ERROR WITH PARALIST: ", self.lookahead.data)
            exit()

    def paralist_(self):
        data = self.lookahead.data['value'];
        if (data == ','):
            self.match(',')
            self.parameter()
            self.paralist_()
        elif (data == ')'):
            return
        else:
            print("ERROR WITH PARALIST_: ", self.lookahead.data)
            exit()

    def parameter(self):
        data = self.lookahead.data['value'];
        if (data in datatype):
            self.vartypeid()
            self.paraid()
        else:
            print("ERROR WITH PARAMETERS: ", self.lookahead.data)
            exit()

    def paraid(self):
        type = self.lookahead.data['TYPE'];
        if (type == 'ID'):
            self.matchID(type)
            self.paraid_()
        else:
            print("ERROR IN PARAMETERS ID: ", self.lookahead.data)
            exit()

    def paraid_(self):
        data = self.lookahead.data['value'];
        if (data == '['):
            self.match('[')
            self.match(']')
        elif (data == ')' or data == ','):
            return
        else:
            print("ERROR IN PARAMETERS ID: ", self.lookahead.data)
            exit()

    def match(self, t):
        if (self.lookahead.data['value'] == t):
            self.lookahead = self.nextToken()

        else:
            print("ERROR WITH SYNATX NEAR TOKKEN: ", self.lookahead.data['value'], " IN LINE NUMBER: ",
                  self.lookahead.data['LINE_NUMBERS'])
            exit()

    def matchID(self, type):

        if (type == 'ID'):
            self.lookahead = self.nextToken()
        else:
            print("ERROR IN TOKEN: ", self.lookahead.data)
            print("EXPECTED TO BE ID ...")
            exit()

    def typeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if (data == 'int'):
            self.match('int')
        elif (data == 'float'):
            self.match('float')
        elif (data == 'string'):
            self.match('string')
        elif (data == 'char'):
            self.match('char')
        elif (data == 'bool'):
            self.match('bool')
        elif (data == 'void'):
            self.match('void')
        else:
            print("ERROR WITH TYPE IN TOKEN: ", self.lookahead.data)
            exit()

    def vartypeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if (data == 'int'):
            self.match('int')
        elif (data == 'float'):
            self.match('float')
        elif (data == 'string'):
            self.match('string')
        elif (data == 'char'):
            self.match('char')
        elif (data == 'bool'):
            self.match('bool')
        else:
            print("ERROR WITH TYPE IN TOKEN: ", self.lookahead.data)
            exit()


def lexer():
    lexer = Lexer()
    lexer.main()
    tok = LexerProc()
    for token in lexer.tokens:
        tok.append(token.value, token.line_number, token.type)
    tok.append('$', token.line_number + 1, "EOF")
    tok.printList()
    print("\nSYMBOL TABLE: \n")
    lexer.sym.printList()
    print("\n")
    check = parser(tok)
    check.lookahead = check.nextToken()
    check.start()

    if check.lookahead.data['value'] == '$':
        print("SYNTAX IS CORRECT... ")



if __name__ == '__main__':
    lexer()

