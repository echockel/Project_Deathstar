#######################################
# yoda_ast.py
# Developed by: Emily Hockel, Prateek Chawla, and Adel Danandeh
#
# Modified code from:
# 	Copyright (c) 2011, Jay Conrod.
# 	All rights reserved.
#######################################

import sys
from equality import *

# Statements
class Statement(Equality):
	pass		

# Arithmetic Expressions
class ArithmExp(Equality):
	pass

# Binary Expressions
class BoolExp(Equality):
	pass

# String Expressions
class StringExp(Equality):
	pass


#######################################
# Statement subclasses
#######################################

# Compound statements
class CompoundStatement(Statement):
	def __init__(self, first, second):
		self.first = first
		self.second = second
		
	def __repr__(self):
		return 'CompoundStatement(%s, %s)' % (self.first, self.second)

	def eval(self, env):
		self.first.eval(env)
		self.second.eval(env)

# Assignment statements
class AssignStatement(Statement):
	def __init__(self, name, exp):
		self.name = name
		self.exp = exp

	def __repr__(self):
		return 'AssignStatement(%s, %s)' % (self.name, self.exp)

	def eval(self, env):
		value = self.exp.eval(env)
		env[self.name] = value

# If statements
class IfStatement(Statement):
	def __init__(self, condition, true_stmt, false_stmt):
		self.condition = condition
		self.true_stmt = true_stmt
		self.false_stmt = false_stmt

	def __repr__(self):
		return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

	def eval(self, env):
		condition_value = self.condition.eval(env)
		if condition_value:
			self.true_stmt.eval(env)
		else:
			if self.false_stmt:
				self.false_stmt.eval(env)

# While statements
class WhileStatement(Statement):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body

	def __repr__(self):
		return 'WhileStatement(%s, %s)' % (self.condition, self.body)

	def eval(self, env):
		condition_value = self.condition.eval(env)
		while condition_value:
			self.body.eval(env)
			condition_value = self.condition.eval(env)

# Print statements
class PrintStatement(Statement):
	def __init__(self, stmt):
		self.stmt = stmt

	def __repr__(self):
		return 'PrintStatement(%s)' % self.stmt

	def eval(self, env):
		stmt_value = self.stmt.eval(env)
		sys.stdout.write('%s' % stmt_value)


#######################################
# Arithmetic expressions subclasses
#######################################

# Binary operations - made of two other ArithmExps
class BinopArithmExp(ArithmExp):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
		
	def __repr__(self):
		return 'BinopArithmExp(%s, %s, %s)' % (self.op, self.left, self.right)

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op == 'VADER':
			value = left_value + right_value
		elif self.op == 'SIDIOUS':
			value = left_value - right_value
		elif self.op == 'LUKE':
			value = left_value * right_value
		elif self.op == 'LEAH':
			value = left_value / right_value
		elif self.op == 'CHEWBACCA':
			value = left_value % right_value
		else:
			raise RuntimeError('unknown operator: ' + self.op)
		return value

# Integer constants
class IntArithmExp(ArithmExp):
	def __init__(self, i):
		self.i = i
		
	def __repr__(self):
		return 'IntArithmExp(%d)' % self.i

	def eval(self, env):
		return self.i

# Variable
class VarArithmExp(ArithmExp):
	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return 'VarArithmExp(%s)' % self.name

	def eval(self, env):
		if self.name in env:
			return env[self.name]
		else:
			return 0 # Variables are initialized to 0

#######################################
# Boolean expressions subclasses
#######################################

# AND expressions - left and right sides are BoolExps
class AndBoolExp(BoolExp):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __repr__(self):
		return 'AndBoolExp(%s, %s)' % (self.left, self.right)

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		return left_value and right_value

# OR expressions - left and right sides are BoolExps
class OrBoolExp(BoolExp):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __repr__(self):
		return 'OrBoolExp(%s, %s)' % (self.left, self.right)

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		return left_value or right_value

# NOT expressions - left and right sides are BoolExps
class NotBoolExp(BoolExp):
	def __init__(self, exp):
		self.exp = exp

	def __repr__(self):
		return 'NotBoolExp(%s)' % self.exp

	def eval(self, env):
		value = self.exp.eval(env)
		return not value

# Relational expressions - left and right sides are ArithmExps
class RelopBoolExp(BoolExp):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

	def __repr__(self):
		return 'RelopBoolExp(%s, %s, %s)' % (self.op, self.left, self.right)

	def eval(self, env):
		left_value = self.left.eval(env)
		right_value = self.right.eval(env)
		if self.op == 'SITH':
			value = left_value < right_value
		elif self.op == 'SITH_ORDER':
			value = left_value <= right_value
		elif self.op == 'JEDI':
			value = left_value > right_value
		elif self.op == 'JEDI_ORDER':
			value = left_value >= right_value
		elif self.op == 'ORDER':
			value = left_value == right_value
		elif self.op == 'BB8_ORDER':
			value = left_value != right_value
		else:
			raise RuntimeError('unknown operator: ' + self.op)
		return value

# True Expression
class TrueBoolExp(BoolExp):
	def __init__(self, t):
		self.t = t

	def __repr__(self):
		return 'TrueBoolExp(%s)' % self.t

	def eval(self, env):
		return True

# False Expression
class FalseBoolExp(BoolExp):
	def __init__(self, 	f):
		self.f = f
			
	def __repr__(self):
		return 'FalseBoolExp(%s)' % self.f

	def eval(self, env):
		return False


#######################################
# String expressions subclasses
#######################################

class ConcatStringExp(	StringExp):
 	def __init__(self, left, right):
  		self.left = left
 		self.right = right

 	def __repr__(self):
 		return 'ConcatStringExp(%s, %s)' % (self.left, self.right)

 	def eval(self, env):
 		left_value = self.left.eval(env)
 		right_value = self.right.eval(env)
 		if isinstance(left_value, int):
 			value = '%d' % left_value
 		else:
 			value = left_value
 		if isinstance(right_value, int):
 			value = value + '%d' % right_value
 		else:
 			value = value + right_value
 		return value

# String
class StringExp(StringExp):
	def __init__(self, s):
		self.s = s
		
	def __repr__(self):
		return 'StringExp(%s)' % self.s

	def eval(self, env):
		return self.s[1:-1].decode('unicode_escape')