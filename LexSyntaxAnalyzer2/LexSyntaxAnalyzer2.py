#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Code by Tony Imbesi

import re


# In[2]:


# Reads a file to lexically and syntactically analyze it.
def main():
    comp = Compiler()
    comp.read_file("test1.txt")


# In[3]:


class Compiler:
    lex = 0
    def read_file(self, filename):
        file = open(filename, "r")
        input_str = file.read()
        file.close()
        lex = Lexer(input_str)
        parse = Parser(lex.get_tokens())


# In[4]:


class Token:
    def __init__(self, lexeme, code, name):
        self.lexeme = lexeme
        self.code = code
        self.name = name
    def __str__(self):
        return f"{self.lexeme} ({self.name})"
    def __repr__(self):
        return f"<Token lexeme:{self.lexeme} code:{self.code} string:{self.name}>"


# In[5]:


# Identify every lexeme in the code.
class Lexer:
    
    VAR = 0
    NUMBER = 1
    UNKNOWN = 99

    BEGIN = 10
    END = 11

    REAL_LIT = 12
    NAT_LIT = 13
    BOOL_LIT = 14
    CHAR_LIT = 15
    STR_LIT = 35
    IF = 16
    LOOP = 17
    LPAREN = 18
    RPAREN = 19
    LBRACE = 20
    RBRACE = 21
    STMT_END = 22
    ASSIGN = 23
    EQ = 24
    NE = 25
    LT = 26
    GT = 27
    LE = 28
    GE = 29
    PLUS = 30
    MINUS = 31
    MULT = 32
    DIV = 33
    MOD = 34
    EXP = 36
    NEG = 37
    NIL = 38
    AND = 39
    OR = 40
    COMMA = 41
    LINE_COM = 42
    BLOCK_COM = 43
    FUNC = 44
    SPACE = 100

    #     Use regular expressions to identify each token
    tokens = [
      ('REAL_LIT', r'^real', REAL_LIT),  # real
      ('NAT_LIT', r'^nat', NAT_LIT),     # natural
      ('BOOL_LIT', r'^bool', BOOL_LIT),  #bool
      ('CHAR_LIT', r'^\'.+\'', CHAR_LIT), # char
      ('STR_LIT', r'^".*"', CHAR_LIT), # char
      ('IF', r'^choos', IF),  # if
      ('LOOP', r'^loop', LOOP),  # while
      ('LPAREN', r'^\(', LPAREN),  # (
      ('RPAREN', r'^\)', RPAREN),  # )
      ('LBRACE', r'^\{', LBRACE),  # {
      ('RBRACE', r'^\}', RBRACE),  # }
      ('STMT_END', r'^;', STMT_END),  # ;
      ('ASSIGN', r'^\=', ASSIGN),  # =
      ('EQ', r'^==', EQ),  # ==
      ('NE', r'^!==' , NE),  # !=
      ('LT', r'^<<', LT),  # <
      ('GT', r'^>>', GT),  # >
      ('LE', r'^<==', LE),  # <=
      ('GE', r'^>==', GE),  # >=
      ('PLUS', r'^\+', PLUS),  # +
      ('MINUS', r'^-', MINUS),  # -
      ('MULT', r'^\*', MULT),  # *
      ('DIV', r'^\/', DIV),  # /
      ('MOD', r'^\%', MOD),  # %
      ('EXP', r'^\^', EXP),  # ^
      ('AND', r'^::', AND),
      ('OR', r'^\?\?', OR),
      ('NOT', r'^!!', NIL),
      ('COMMA', r'^,', COMMA),

      ('BEGIN', r'^BEGIN', BEGIN),  # BEGIN
      ('END', r'^END', END),  # END
      ('NUMBER', r'^[0-9]+', NUMBER), # Integer
      ('DEC_NUM', r'^[0-9]+.[0-9]+', NUMBER), # Integer
#       ('FUNC', r'^[A-Za-z_]{6,8}', FUNC),  # Variables
      ('VAR', r'^[A-Za-z_]{6,8}', VAR),  # Variables

#       ('LINE_COM', r'^\$\$.*\n', LINE_COM),
#       ('BLOCK_COM', r'^\$\*.*\*\$', BLOCK_COM),
#       ('SPACE', r'\s.+', SPACE),
      ('UNKNOWN', r'.+', UNKNOWN),  # Everything else
    ]
       
    comment_re = r'(^\$\$.*\n)|(^\$\*(.|\n)*\*\$)'

    tokens_list = []
    
    def __init__(self, input_str):
#         print(self.tokens[0][1])
#         words = input_str.split()
#         print(words)
#         for word in words:
#             lex_error = self.lookup(word)
#             if lex_error:
#                 break
        lex_error = self.lookup(input_str)
        if lex_error:
            return
        if not (lex_error):
            print("Complete! Tokens list: ")
            print(self.tokens_list)
            
    def lookup(self, inp):
        while (len(inp) > 0):
            print("Remaining input: ")
            print(inp)
            # Compare this word to every regular expression in tokens, then add that word and its token code
            # to the list of token codes.
       
            # 1) Consume whitespace and comments
            inp = inp.strip()
            comment_match = re.match(self.comment_re, inp)
            if (comment_match):
                print("Comment: " + comment_match.group())
                inp = inp[matchpos.start() + len(comment_match.group()):]
                continue
            # Continue when there are no more comments to skip
            i = 0
            while i < len(self.tokens):
                print(self.tokens[i][1])
           # 2) Find the match at the start of the string
                matchpos = re.search(self.tokens[i][1], inp)
                if (matchpos and self.tokens[i][0] == 'UNKNOWN'):
                    raise Exception(f"Error: unknown token '{inp}'")
                    return True
           # 3) Consume the matched portion of the string
                elif matchpos:
                    print(f"Matched: '{self.tokens[i][0]}'")
                    self.tokens_list.append(Token(matchpos.group(), self.tokens[i][2], self.tokens[i][0]))
                    inp = inp[matchpos.start() + len(matchpos.group()):]
           # Start over and find the next token to match
                    break


                i = i + 1
            
        return False
    
    def get_tokens(self):
        return self.tokens_list


def error(errorMsg):
    print(errorMsg)
    exit(1)


# In[6]:


class Parser:
    level = 0
    next_index = 0
    next_token = 0
    tokens_list = []
    spaces = ""
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list
        self.syntax_analyze()
        

    # Evaluate the program's syntax based on the following rules:

    # <PROG> -> BEGIN <STMT> END
    # <BLOCK> `{`{<STMT>}`}`
    # <STMT> -> <ASSIGN> | <LOOP> | <IF> | <BLOCK>
    # <ASSIGN> -> <type> <id> = <value> ;
    # <IF> -> choos <body>
    # <LOOP> -> loop <body>
    # <body> -> `(`<value>`)` <STMT>

    # <value> -> <not> <expression> <bool> <bool_p>
    # <bool> -> <boolcomp> <expression> | :empty:
    # <bool_p> -> <boolop> <value> | :empty:
    # <boolop> -> :: | ??
    # <boolcomp> -> < | <== | == | !== | >=== | >  
    # <not> -> !! | :empty:
    # <expression> -> <term> <exp_p>
    # <exp_p> -> (+|-) <term> <exp_p> | :empty:
    # <term> -> <factor> <term_p>
    # <term_p> -> (*|/|%) <factor> <term_p> | :empty:
    # <factor> -> <num_op> <fact_p>
    # <fact_p> -> ^ <num_op> <fact_p> | :empty:
    # <num_op> -> <id> | <literal> | <paren>
    # <paren> -> `(`<value>`)`
    # 
    # <id> -> <var_id>[<function>]
    # <function> -> `(`<params>`)`
    # <params> -> `(`<value> {, <value>}`)`

    def child(s):
        s.level = s.level + 1
        s.indent()
        print(s.spaces + f"Tree level: {s.level}")
        
    def parent(s):
        s.level = s.level - 1
        s.indent()
        msg = s.level
        if s.level == 0:
            msg = "ROOT"
        print(s.spaces + f"Tree level: {msg}")
    
    def indent(s):
        i = 0
        s.spaces = ""
        while i < s.level:
            s.spaces = s.spaces + "   "
            i = i + 1

    def syntax_analyze(self):
        self.level = 0
        self.next_index = 0
        self.next_token = self.tokens_list[self.next_index].name
        print("Tree level: ROOT")
        print(self.spaces + f"Enter <PROG>")
        self.begin()
        self.stmt()
        self.end()
        print(self.spaces + f"Exit <PROG>")
        print("No syntax errors!")

    # Consume the next token
    def lex(s):
        print(s.spaces + f"Consumed token:'{s.next_token}'")
        
        if s.next_index < len(s.tokens_list) - 1:
            s.next_index = s.next_index + 1
            s.next_token = s.tokens_list[s.next_index].name
        
    #     print(f"next in list: '{tokens_list[next_index]}'")

    def error(s, token):
        raise Exception(f"Too bad! Error at token '{s.next_index}' ('{s.tokens_list[s.next_index]}')\n Expected token: '{token}'")


    def begin(s):
        s.child()
        print(s.spaces + f"Enter BEGIN")
        if s.next_token == 'BEGIN':
            s.lex()
        else:
            s.error('BEGIN')
        print(s.spaces + f"Exit BEGIN")
        s.parent()

    def end(s):
        s.child()
        print(s.spaces + f"Enter END")
        if s.next_token == 'END':
            s.lex()
        else:
            s.error('END')
        print(s.spaces + f"Exit END")
        s.parent()

    def stmt(s):
        s.child()
        print(s.spaces + f"Enter <STMT>")
        if s.next_token == 'LBRACE':
            s.lex()
            s.stmt_list()
        elif s.next_token == 'IF':
            s.lex()
            s.child()
            print (s.spaces + f"Enter <IF>")
            s.body()
            print (s.spaces + f"Exit <IF>")
            s.parent()
        elif s.next_token == 'LOOP':
            s.lex()
            s.child()
            print (s.spaces + f"Enter <LOOP>")
            s.body()
            print (s.spaces + f"Exit <LOOP>")
            s.parent()
        else:
            s.assign()
        print(s.spaces + f"Exit <STMT>")
        s.parent()
            
    def stmt_list(s):
        s.child()
        print(s.spaces + f"Enter <BLOCK>")
        while s.next_token != 'RBRACE':
            s.stmt()
        # Consume the closing }
        s.lex()
        print(s.spaces + f"Exit <BLOCK>")
        s.parent()

    def body(s):
        if s.next_token == 'LPAREN':
            s.lex()
            s.value()
            if s.next_token == 'RPAREN':
                s.lex()
                stmt()
            else:
                s.error('RPAREN')
        else:
            s.error('LPAREN')

    def value(s):
        s.child()
        print(s.spaces + f"Enter <value>")
        # Consume not operator
        if (s.next_token == 'NOT'):
            s.lex()
        s.expr()
        s.expr_bool()
        s.bool_op()
        print(s.spaces + f"Exit <value>")
        s.parent()

    def expr(s):
        s.child()
        print(s.spaces + f"Enter <expr>")
        s.term()
        while (s.next_token == 'PLUS' or s.next_token == 'MINUS'):
            s.lex()
            s.term()
        print(s.spaces + f"Exit <expr>")
        s.parent()

    def expr_bool(s):
        s.child()
        print(s.spaces + f"Enter <bool>")
        if (s.next_token == 'EQ' or s.next_token == 'NE' or s.next_token == 'GT' or s.next_token == 'LT' or s.next_token == 'GE' or s.next_token == 'LE'):
            s.lex()
            s.expr()
        print(s.spaces + f"Exit <bool>")
        s.parent()

    def bool_op(s):
        s.child()
        print(s.spaces + f"Enter <boolop>")
        while (s.next_token == 'AND' or s.next_token == 'OR'):
            s.lex()
            s.value()
        print(s.spaces + f"Exit <boolop>")
        s.parent()
        
    def term(s):
        s.child()
        print(s.spaces + f"Enter <term>")
        s.factor()
        while (s.next_token == 'MULT' or s.next_token == 'DIV' or s.next_token == 'MOD'):
            s.lex()
            s.factor()
        print(s.spaces + f"Exit <term>")
        s.parent()

    def factor(s):
        s.child()
        print(s.spaces + f"Enter <fact>")
        s.num_op()
        while (s.next_token == 'EXP'):
            s.lex()
            s.num_op()
        print(s.spaces + f"Exit <fact>")
        s.parent()
    
    def num_op(s):
        s.child()
        print(s.spaces + f"Enter <num_op>")
        # Consume negation operator
        if (s.next_token == 'MINUS'):
            s.lex()
        if not(s.var_id(False) or s.number(False)):
            s.paren()
        print(s.spaces + f"Exit <num_op>")
        s.parent()
    
    def paren(s):
        s.child()
        print(s.spaces + f"Enter <paren>")
        if (s.next_token == 'LPAREN'):
            s.lex()
            s.value()
            if (s.next_token == 'RPAREN'):
                s.lex()
            else:
                s.error('RPAREN')
        else:
            s.error('LPAREN')
        print(s.spaces + f"Exit <paren>")
        s.parent()
        
    def number(s, required):
        s.child()
        print(s.spaces + f"Enter <NUMBER>")
        if s.next_token == 'NUMBER' or s.next_token == 'DEC_NUM':
            s.lex()
        elif required:
            s.error('NUMBER')
        print(s.spaces + f"Exit <NUMBER>")
        s.parent()
        return True
    
    
              
    def assign(s):
        s.child()
        print(s.spaces + f"Enter <ASSIGN>")
        s.var_type()
        s.var_id(True)
        s.assign_sym()
        s.value()
        s.stmt_end()
        print(s.spaces + f"Exit <ASSIGN>")
        s.parent()

    def assign_sym(s):
        s.child()
        print(s.spaces + f"Enter <ASSIGN_SYM>")
        if s.next_token == 'ASSIGN':
            s.lex()
        else:
            s.error('ASSIGN_SYM')
        print(s.spaces + f"Exit <ASSIGN_SYM>")
        s.parent()
        
    def stmt_end(s):
        s.child()
        print(s.spaces + f"Enter <STMT_END>")
        if s.next_token == 'STMT_END':
            s.lex()
        else:
            s.error('STMT_END')
        print(s.spaces + f"Exit <STMT_END>")
        s.parent()
            
    def var_type(s):
        s.child()
        print(s.spaces + f"Enter <type>")
        if (s.next_token == 'REAL_LIT' or s.next_token == 'NAT_LIT' or s.next_token == 'BOOL_LIT' or s.next_token == 'CHAR_LIT' or s.next_token == 'STR_LIT'): 
            s.lex()
        else:
            s.error('VAR_TYPE')
        print(s.spaces + f"Exit <type>")
        s.parent()
        return True

    def var_id(s, required):
        s.child()
        print(s.spaces + f"Enter <id>")
        if s.next_token == 'VAR':
            s.lex()
            s.function()
        # Throw an exception if this token must be a var_id
        elif required:
            s.error('VAR')
        print(s.spaces + f"Exit <id>")
        s.parent()
    
    def function(s):
        s.child()
        print(s.spaces + f"Enter <function>")
        if s.next_token == 'LPAREN':
            s.lex()
            s.params()
            if s.next_token == 'RPAREN':
                s.lex()
            else:
                s.error('RPAREN')
        print(s.spaces + f"Exit <function>")
        s.parent()
                
    def params(s):
        s.child()
        print(s.spaces + f"Enter <params>")
        done = False
        while not done:
            s.value()
            if s.next_token == 'COMMA':
                s.lex()
            else:
                done = True
        print(s.spaces + f"Exit <params>")
        s.parent()


# In[7]:


# Run it
main()

