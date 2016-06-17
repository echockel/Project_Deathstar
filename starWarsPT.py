#! /usr/bin/env python
import sys
from yoda_parser import *
from yoda_lexer import *

"""
Client Interface for the Star Wars Interpreter
    Reads command line arguments, checks file existence, extension, opens file
    and begins parsing in yoda_lexer.py. Functions as the entrance point for the interpreter.

Supported Keywords:
    A LONG TIME AGO IN A GALAXY FAR, FAR AWAY...    main
    ...MAY THE FORCE BE WITH YOU                    end main
    IVE GOT A BAD FEELING ABOUT THIS                print statement
    I FIND YOUR LACK OF FAITH DISTURBING            Comments
    YODA                                            Assignment
    VADER                                           +
    SIDIOUS                                         - 
    LUKE                                            *
    LEAH                                            /
    CHEWBACCA                                       %
    SITH_ORDER                                      <=
    SITH                                            <
    JEDI_ORDER                                      >=
    JEDI                                            >
    BB8_ORDER                                       !=
    ORDER                                           ==
    R2D2                                            AND
    BB8                                             NOT
    C3PO                                            OR
    LIGHT_SIDE                                      True
    DARK_SIDE                                       False
    ITS A TRAP                                      if
    MOVE ALONG                                      then
    STAY ON TARGET                                  else
    THESE ARENT THE DROIDS YOU ARE LOOKING FOR      end
    DO                                              while
    OR DO NOT...                                    do
    THERE IS NO TRY                                 end

How to Use:
    python starWarsPT.py [FILE].yoda

Team: Prateek Chawla, Emily Hockel, Adel Danandeh
"""

class starWarsInterpreter():

    def __init__ (self):
        self.__commandLineArgs()
        self.__fileOut = self.__openFile()
        tokens = yoda_lex(self.__fileOut.read())
        parse_result = yoda_parse(tokens)
        if not parse_result:
            sys.stderr.write('Parse error!\n')
            sys.exit(1)
        ast = parse_result.value
        env = {}
        ast.eval(env)
        self.__fileOut.close()

    def __commandLineArgs(self):
        """
        Confirms length of command line arguments
        """
        if len(sys.argv) <= 1 or len(sys.argv) > 2:
            raise Exception('Please enter exactly one .yoda file error!\n')

    def __openFile(self):
        """
        Open file if possible. 
        """
        file = None 
        #os.path.isfile(file)
        try: 
            file = open(sys.argv[1], 'r')
        except IOError: 
            raise Exception('File not found\n')

        return file

    def __checkExtension(self, file):
        """
        Checks that file extension is supported.
        """
        if not sys.argv[1].endswith('.yoda'):
            raise Exception('Please enter exactly one .yoda file error!\n')

starWars = starWarsInterpreter()