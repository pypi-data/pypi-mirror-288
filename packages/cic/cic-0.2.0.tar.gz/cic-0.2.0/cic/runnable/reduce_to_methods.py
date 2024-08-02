import sys
import logging

import ply.lex as lex

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


tokens = (
         'NUMBER',
#         'PLUS',
#         'MINUS',
#         'TIMES',
#         'DIVIDE',
         'LPAREN',
         'RPAREN',
      )

methods = {}
contract = False
method = None
typ = None
function = False
signature = False


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'//.+'
    pass


def t_item(t):
    r';'
    global function, signature, method, typ

    signature = False
    function = False
    method = None
    typ = None


def t_contract(t):
    r'(interface|contract).+\{'
    global contract
    if contract:
        raise SyntaxError('this meagre parser will only handle one interface/contract definition per file')
    contract = True


def t_pragma(t):
    r'pragma.+'
    pass


def t_function(t):
    r'function'
    global function, contract

    if not contract:
        raise SyntaxError('functions must be within inteface/contract definitions')
    function = True


def t_LPAREN(t):
    r'\('
    global function, signature

    if not function:
        return
    signature = True


def t_RPAREN(t):
    r'\)'
    global signature

    signature = None


def t_WORD(t):
    r'([\w\d]+)'
    global method, typ, signature

    if typ and not signature:
        return

    if function and method == None:
        method = t.value
        methods[method] = []
    elif typ == None and signature:
        typ = t.value
        methods[method].append(typ)


def t_COMMA(t):
    r','
    global typ

    typ = None


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t}'

def main():
    # Build the lexer
    lexer = lex.lex()

    # Tokenize
    f = open(sys.argv[1], 'r')
    while True:
        l = f.readline()
        if not l:
            break
        lexer.input(l)
        tok = lexer.token()
        logg.debug('token {}'.format(tok))


    for k in methods.keys():
        print('{}({})'.format(k, ','.join(methods[k])))


if __name__ == '__main__':
    main()
