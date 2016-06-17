#######################################
# yoda_ast.py
# Developed by: Emily Hockel, Prateek Chawla, and Adel Danandeh
#
# Modified code from:
# 	Copyright (c) 2011, Jay Conrod.
# 	All rights reserved.
#######################################


from yoda_lexer import *
from combinators import *
from yoda_ast import *

def keyword(kw):
	return Reserved(kw, SYS_VAR)

num = Tag(INTEGER) ^ (lambda i: int(i))
string = Tag(STRING)
id = Tag(IDENTIFIER)


# Called by main program
# To begin parsing the program we call parser and pass
# the entire set of tokens for the program and a position of 0
def yoda_parse(tokens):
	ast = parser()(tokens, 0)
	return ast

############################################
# Top level parsers	
############################################
def program():
	return keyword('A LONG TIME AGO IN A GALAXY FAR, FAR AWAY...') + \
			stmt_list() + keyword('...MAY THE FORCE BE WITH YOU') ^ process_group

# This enforces that first and last tokens be our 
# starting and ending stmts in program()
def parser():
	return Phrase(program())



############################################
# Statements
############################################
def stmt_list():
	separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
	return Exp(stmt(), separator)

def stmt():
	return assign_stmt() | \
		   while_stmt()	 | \
		   if_stmt()	 | \
		   print_stmt()

def assign_stmt():
	def process(parsed):
		((name, _), exp) = parsed
		return AssignStatement(name, exp)
	return id + keyword('YODA') + arithm_exp() ^ process

def while_stmt():
	def process(parsed):
		((((_, condition), _), body), _) = parsed
		return WhileStatement(condition, body)
	return keyword('DO') + bool_exp() + \
		   keyword('OR DO NOT...') + Lazy(stmt_list) + \
		   keyword('THERE IS NO TRY') ^ process

def if_stmt():
	def process(parsed):
		(((((_, condition), _), true_stmt), false_parsed), _) = parsed
		if false_parsed:
			(_, false_stmt) = false_parsed
		else:
			false_stmt = None
		return IfStatement(condition, true_stmt, false_stmt)
	return keyword('ITS A TRAP') + bool_exp() + \
		   keyword('MOVE ALONG') + Lazy(stmt_list) + \
		   Opt(keyword('STAY ON TARGET') + Lazy(stmt_list)) + \
		   keyword('THESE ARENT THE DROIDS YOU ARE LOOKING FOR') ^ process

def print_stmt():
	def process(parsed):
		(_, exp) = parsed
		return PrintStatement(exp)
	return keyword('IVE GOT A BAD FEELING ABOUT THIS') + string_exp() ^ process



############################################
# Arithmetic expressions
############################################
def arithm_exp():
	return precedence(arithm_term(),
					  arithm_precedence_levels,
					  process_binop)

def arithm_term():
	return arithm_value() | arithm_group()

def arithm_value():
	return (num ^ (lambda i: IntArithmExp(i))) | \
		   (id ^ (lambda v: VarArithmExp(v)))

def arithm_group():
	return keyword('(') + Lazy(arithm_exp) + keyword(')') ^ process_group


############################################
#Boolean expressions
############################################
def bool_exp():
	return precedence(bool_term(),
					  bool_precedence_levels,
					  process_logic)

def bool_term():
	return bool_not() 	| \
		   bool_relop() | \
		   bool_value() | \
		   bool_group()

def bool_not():
	return keyword('BB8') + Lazy(bool_term) ^ (lambda parsed: NotBoolExp(parsed[1]))

def bool_relop():
	relops = ['SITH', 'SITH_ORDER', 'JEDI', 'JEDI_ORDER', 'ORDER', 'BB8_ORDER']
	return arithm_exp() + any_operator_in_list(relops) + arithm_exp() ^ process_relop

def bool_value():
	return (keyword('LIGHT_SIDE') ^ (lambda t: TrueBoolExp(t))) | \
		   (keyword('DARK_SIDE') ^ (lambda f: FalseBoolExp(f)))

def bool_group():
	return keyword('(') + Lazy(bool_exp) + keyword(')') ^ process_group


############################################
#String expressions
############################################
def string_exp():
	return precedence(string_value(),
					  string_precedence_levels,
					  process_string)

def string_value():
	return (string ^ (lambda s: StringExp(s))) | \
		   (id ^ (lambda v: VarArithmExp(v)))

############################################
# Helper functions
############################################

def process_binop(op):
	return lambda l, r: BinopArithmExp(op, l, r)

def process_logic(op):
	if op == 'R2D2': # AND
		return lambda l, r: AndBoolExp(l, r)
	elif op == 'C3P0': # OR
		return lambda l, r: OrBoolExp(l, r)
	else:
		raise RuntimeError('unknown logic Operator: ' + op)

def process_relop(parsed):
	((left, op), right) = parsed
	return RelopBoolExp(op, left, right)

def process_group(parsed):
	((_, p), _) = parsed
	return p

def process_string(_):
	return lambda l, r: ConcatStringExp(l, r)

def any_operator_in_list(ops):
	op_parsers = [keyword(op) for op in ops]
	parser = reduce(lambda l, r: l | r, op_parsers)
	return parser

def precedence(value_parser, precedence_levels, combine):
	def op_parser(precedence_level):
		return any_operator_in_list(precedence_level) ^ combine
	parser = value_parser * op_parser(precedence_levels[0])
	for precedence_level in precedence_levels[1:]:
		parser = parser * op_parser(precedence_level)
	return parser


############################################
# Operator precedence levels
############################################
arithm_precedence_levels = [
	['LUKE', 'LEAH', 'CHEWBACCA'], # *, /, %
	['VADER', 'SIDIOUS'], # +, -
]

bool_precedence_levels = [
	['R2D2'], # AND
	['C3P0'], # OR
]

string_precedence_levels = [
	['+'],
]