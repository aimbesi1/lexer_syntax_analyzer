#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Code by Tony Imbesi

import re

VAR = 0
NUMBER = 1
UNKNOWN = 99

BEGIN = 10
END = 11

ONEB = 12
TWOB = 13
FOURB = 14
EIGHTB = 15
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

tokens = [
  ('ONEB', r'^sint$', ONEB),  # one byte
  ('TWOB', r'^mint$', TWOB),  # two byte
  ('FOURB', r'^lint$', FOURB),  # four byte
  ('EIGHTB', r'^xlint$', EIGHTB),  # eight byte
  ('IF', r'^choos$', IF),  # if
  ('LOOP', r'^loop$', LOOP),  # while
  ('LPAREN', r'\(', LPAREN),  # (
  ('RPAREN', r'\)', RPAREN),  # )
  ('LBRACE', r'\{', LBRACE),  # {
  ('RBRACE', r'\}', RBRACE),  # }
  ('STMT_END', r';', STMT_END),  # ;
  ('ASSIGN', r'\=', ASSIGN),  # =
  ('EQ', r'==', EQ),  # ==
  ('NE', r'!=' , NE),  # !=
  ('LT', r'<', LT),  # <
  ('GT', r'>', GT),  # >
  ('LE', r'<=', LE),  # <=
  ('GE', r'>=', GE),  # >=
  ('PLUS', r'\+', PLUS),  # +
  ('MINUS', r'-', MINUS),  # -
  ('MULT', r'\*', MULT),  # *
  ('DIV', r'\/', DIV),  # /
  ('MOD', r'\%', MOD),  # %
  
  ('BEGIN', r'BEGIN', BEGIN),  # BEGIN
  ('END', r'END', END),  # END
  ('NUMBER', r'^[0-9]+$', NUMBER), # Integer
  ('VAR', r'^[A-Za-z_]{6,8}$', VAR),  # Variables
  ('UNKNOWN', r'.', UNKNOWN),  # Everything else
]

tokens_list = []
next_index = 0
next_token = 0
lex_error = False


# In[2]:


print(tokens_list)


# In[3]:


i = 0
while i < len(tokens):
    print(tokens[i][1])
    i = i + 1


# In[4]:


def main():
    global tokens_list
    tokens_list = []
    filename = "test4.txt"
    file = open(filename, "r")
    words = file.read().split()
    print("Number of tokens: ")
    print(len(words))
    print(words)
    for word in words:
        lookup(word, tokens_list)
        if lex_error:
            break
    if not(lex_error):
        print("Tokens list: ")
        print(tokens_list)
        
        syntax_analyze()
    file.close()


# In[5]:


# Identify every lexeme in the code.

def lookup(word, tokens_list):
    global lex_error
    # Compare this word to every regular expression in tokens, then add that word's token code
    # to the list of token codes.
    i = 0
    while i < len(tokens):
#         print(tokens[i])
        match = re.fullmatch(tokens[i][1], word)
        if (match and tokens[i][0] == 'UNKNOWN'):
            raise Exception(f"Error: unknown token '{word}'")
            lex_error = True
            break
        elif match:
            print(f"Matched: '{tokens[i][0]}'")
            tokens_list.append(tokens[i][0])
#             print(tokens_list)
            break
        
        i = i + 1


def error(errorMsg):
    print(errorMsg)
    exit(1)


# In[6]:


# Evaluate the program's syntax based on the following rules:

# <PROG> -> BEGIN {<STMT_LIST>} END
# <STMT_LIST> -> `{`{<STMT>}`}`
# <STMT> -> <ASSIGN> | <LOOP> | <IF>
# <ASSIGN> -> <type> <id> = <value> ;
# <value> -> <expression> <bool>
# <IF> -> choos `(`<value>`)` {<STMT_LIST>}
# <LOOP> -> loop `(`<value>`)` {<STMT_LIST>}

# <bool> -> :empty: | ((<|<=|==|!=|>=|>) <expression>)
# <expression> -> <term> {(+|-) <term>}
# <term> -> <factor> {(*|/|%) <factor>}
# <factor> -> <id> | <literal> | `(`<expression>`)`


def syntax_analyze():
    global next_index, next_token
    next_index = 0
    next_token = tokens_list[next_index]
    print(f"start: next_token: '{next_token}'")
#     print(f"next in list: '{tokens_list[next_index]}'")
    begin()
    
def lex():
    global next_index, next_token, tokens_list
    next_index = next_index + 1
    next_token = tokens_list[next_index]
    print(f"lex: next_token: '{next_token}'")
#     print(f"next in list: '{tokens_list[next_index]}'")

def error(token):
    raise Exception(f"Too bad! Error at token '{next_index}' ('{tokens_list[next_index]}')\n Expected token: '{token}'")

    
def begin():
    global next_index, next_token
#     print("<BEGIN>")
#     print(f"next_token: '{next_token}'")
    if next_token == 'BEGIN':
        lex()
#         print("LBRACE")
#         print(f"next_token: '{next_token}'")
        if next_token == 'LBRACE':
            lex()
            stmt_list()
            end()
        else:
            error('LBRACE')
    else:
        error('BEGIN')

def end():
    global next_index, next_token
    if next_token == 'END':
        print("No syntax errors!")
    else:
        error('END')

def stmt_list():
    global next_index, next_token
    print("--STMT_LIST--")
    while next_token != 'RBRACE':
        if next_token == 'IF':
            lex()
            print ('CHOOS: ')
            body()
            print ('Exit CHOOS')
        elif next_token == 'LOOP':
            lex()
            print ('LOOP: ')
            body()
            print ('Exit LOOP')
        else:
            assign()
    lex()
    print("--Exit STMT_LIST--")
            
def body():
    global next_index, next_token
    if next_token == 'LPAREN':
        lex()
        value()
        if next_token == 'RPAREN':
            lex()
            if next_token == 'LBRACE':
                lex()
                stmt_list()
            else:
                error('LBRACE')
        else:
            error('RPAREN')
    else:
        error('LPAREN')
                
def value():
    global next_index, next_token
    expr()
    if (next_token == 'EQ' or next_token == 'NE' or next_token == 'GT' or next_token == 'LT' or next_token == 'GE' or next_token == 'LE'):
        lex()
        expr()

def expr():
    global next_index, next_token
    term()
    while (next_token == 'PLUS' or next_token == 'MINUS'):
        lex()
        term()

def expr_bool():
    global next_index, next_token

def term():
    global next_index, next_token

    factor()
    while (next_token == 'MULT' or next_token == 'DIV' or next_token == 'MOD'):
        lex()
        factor()

def factor():
    global next_index, next_token
    
    if (next_token == 'VAR' or next_token == 'NUMBER'):
        lex()
    else:
        if (next_token == 'LPAREN'):
            lex()
            expr()
            if (next_token == 'RPAREN'):
                lex()
            else:
                error('RPAREN')
        else:
            error('LPAREN')

def assign():
    global next_index, next_token
#     print("Enter <ASSIGN>")
    var_type()
    var_id()
    if next_token ==  'ASSIGN':
        lex()
        value()
        if next_token == 'STMT_END':
            lex()
        else:
            error('STMT_END')
    else:
        error('ASSIGN')
    
    
    

def var_type():
    global next_index, next_token
    if (next_token == 'ONEB' or next_token == 'TWOB' or next_token == 'FOURB' or next_token == 'EIGHTB'): 
        lex()
    else:
        error('VAR_TYPE')
        
def var_id():
    global next_index, next_token
    if next_token == 'VAR':
        lex()
    else:
        error('VAR')


# In[7]:


# Run it
main()


# In[ ]:




