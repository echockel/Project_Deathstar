#######################################
# yoda_ast.py
# Developed by: Emily Hockel, Prateek Chawla, and Adel Danandeh
#
# Modified code from:
#   Copyright (c) 2011, Jay Conrod.
#   All rights reserved.
#######################################

import lexer

SYS_VAR          = 'SYS_VAR'
INTEGER          = 'INTEGER'
STRING           = 'STRING'
IDENTIFIER       = 'IDENTIFIER'

internalTokens = [
    (r'[ \n\t]+',                                        None),    # Ignore whitespace, newlines, and tabs
    (r'I FIND YOUR LACK OF FAITH DISTURBING[^\n]*',      None),    # Ignore comments
    (r'A LONG TIME AGO IN A GALAXY FAR, FAR AWAY...',    SYS_VAR), # main
    (r'...MAY THE FORCE BE WITH YOU',                    SYS_VAR), # end main
    (r'IVE GOT A BAD FEELING ABOUT THIS',                SYS_VAR), # print statement
    (r'YODA',                                            SYS_VAR), # Assignment
    (r'\(',                                              SYS_VAR), # Used to group expressions
    (r'\)',                                              SYS_VAR),
    (r'\+',                                              SYS_VAR), # Used to combine print expressions
    (r';',                                               SYS_VAR), # Used to separate statements
    (r'VADER',                                           SYS_VAR), # +
    (r'SIDIOUS',                                         SYS_VAR), # - 
    (r'LUKE',                                            SYS_VAR), # *
    (r'LEAH',                                            SYS_VAR), # /
    (r'CHEWBACCA',                                       SYS_VAR), # %
    (r'SITH_ORDER',                                      SYS_VAR), # <=
    (r'SITH',                                            SYS_VAR), # <
    (r'JEDI_ORDER',                                      SYS_VAR), # >=
    (r'JEDI',                                            SYS_VAR), # >
    (r'BB8_ORDER',                                       SYS_VAR), # !=
    (r'ORDER',                                           SYS_VAR), # ==
    (r'R2D2',                                            SYS_VAR), # AND
    (r'BB8',                                             SYS_VAR), # NOT
    (r'C3PO',                                            SYS_VAR), # OR
    (r'LIGHT_SIDE',                                      SYS_VAR), # True
    (r'DARK_SIDE',                                       SYS_VAR), # False
    (r'ITS A TRAP',                                      SYS_VAR), # if
    (r'MOVE ALONG',                                      SYS_VAR), # then
    (r'STAY ON TARGET',                                  SYS_VAR), # else
    (r'THESE ARENT THE DROIDS YOU ARE LOOKING FOR',      SYS_VAR), # end
    (r'DO',                                              SYS_VAR), # while
    (r'OR DO NOT...',                                    SYS_VAR), # do
    (r'THERE IS NO TRY',                                 SYS_VAR), # end
    (r'[0-9]+',                                          INTEGER),
    (r'\"([^\\"\n]|\\[\\"0nt])*\"',                      STRING),
    (r'[A-Za-z][A-Za-z0-9_]*',                           IDENTIFIER),
]

def yoda_lex(input):
    return lexer.lex(input, internalTokens)