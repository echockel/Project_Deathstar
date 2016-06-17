#######################################
# Modified code from:
# 	Copyright (c) 2011, Jay Conrod.
# 	All rights reserved.
#######################################

# Every parser will return a Result object on success
# or None on failure
# value is part of AST
# position is index of next token in the stream
class Result:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)

# Parser
class Parser:
	def __add__(self, other):
		return Concat(self, other)

	def __mul__(self, other):
		return Exp(self, other)

	def __or__(self, other):
		return Alternate(self, other)

	def __xor__(self, function):
		return Process(self, function)

		
# Tag - matches any token with a particular tag
class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


# Reserved - used to parse reserved words and operators
# accepts tokens with specific value and tag
class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
           tokens[pos][0] == self.value and \
           tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


# Concat - takes two parsers as input
# Applies left parser followed by right
# If both are successful, result will be pair of results
# If either is unsuccessful, None is returned
class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None


# Exp - Takes two parsers as input
# Parses a list of expressions with separator between
# each pair of expressions - First parser is used to 
# match elements of list - Second parser is used to 
# match separators (operators)
class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result 


# Alternate - takes two parsers as input
# First applies left parser - if successful return result
# If not, apply right parser and return its result
class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result


# Opt - takes one parser as input
# First applies parser - if successful return result as usual
# If it fails, successful result is returned with value of None
#   and result position is same as input position
class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return Result(None, pos)


# Rep - takes one parser as input
# Applies parser repeatedly until it fails
# If it fails on first application it will not consume any tokens
class Rep(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)


# Process - takes one parser and a function as input
# Applies parser and if successful the result value is
# passed into the function and that result is returned instead
class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result

# Lazy - takes a zero-argument function as input which
#        returns a parser
# Will not call function until it is applied
class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


# Phrase - takes one parser as input
# Applies parser and returns result normally.
# Will fail if parser did not consume all remaining tokens
class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None