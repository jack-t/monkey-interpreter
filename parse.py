import lex
from ast import *

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.states = []

	def peek(self, ahead = 1):
		if len(self.tokens) >= ahead:
			return self.tokens[ahead:]
		else:
			raise Exception("Too few tokens left in the stream")

	def peel(self, ahead = 1):
		if len(self.tokens) >= ahead:
			ret = self.tokens[:ahead]
			self.tokens = self.tokens[:ahead]
		else:
			raise Exception("Too few tokens left in the stream")

	def expect(self, token):
		tok = peel()
		if tok.name != token:
			raise Expect("expected '" + token + "'")
		else:
			return tok

	def test_next(self, token):
		tok = peek()
		return tok.name == token

	def mark():
		states.append(tokens)
	def drop():
		states.pop()

	def backtrack():
		tokens = states.pop()

	# statements are either let bindings or expr statements. Both end with semicolons
	def stmt(self):
		stmt = None
		if not test_next("let"):
			expr = expr()
			stmt = ExprStmt(expr)
		else:
			expect("let")
			name = expect("identifier").payload
			expr = expr()
			stmt = LetStmt(name, expr)

		expect(";")
		return stmt

	def expr(self):
		expr = None
		if test_next("{"):
			expr = block()
		elif test_next("if"):
			expr = if_expr()
		else:
			expr = mult()

		if test_next("("):
			return call(expr)
		else:
			return expr

	def call(self, func):
		expect("(")
		params = []
		while not test_next(")"):
			params.append(expr())
		expect(")")

		return FuncApplicationExpr(func, params)

	def get_op(self, op):
		if op == "*": return BinaryOp.MULT
		elif op == "/": return BinaryOp.DIV
		elif op == "+": return BinaryOp.ADD
		elif op == "-": return BinaryOp.SUB
		elif op == ">": return BinaryOp.GREATER
		elif op == ">=": return BinaryOp.GREATER_EQ
		elif op == "<": return BinaryOp.LESS
		elif op == "<=": return BinaryOp.LESS_EQ
		elif op == "==": return BinaryOp.EQUALS
		elif op == "!=": return BinaryOp.NOT_EQUALS
		else:
			raise Exception("No such operation '" + op + "'")

	def block(self):
		expect("{")
		stmts = []

		while not test_next("}"):
			mark()
			try:
				stmts.append(stmt())
				drop() # this can't be in a finally block
			except:
				backtrack()
				expr = expr()
				expect("}")
				return Block(stmts, expr) # you're only allowed one expression at the end

		expect("}")
		return Block(stmts, None)

	def if_expr(self):
		expect("if")
		condition = expr()
		true = expr()
		false = None
		if test_next("else"):
			false = expr()
		return ConditionalExpr(condition, true, false)

	def mult(self):
		expr = add()
		while test_next("*") or test_next("/"):
			expr = BinaryExpr(expr, get_op(p.name), add())

		return expr

	def add(self):
		expr = cmp()
		while test_next("+") or test_next("-"):
			expr = BinaryExpr(expr, get_op(p.name), cmp())

		return expr

	def cmp(self):
		expr = assign()
		while test_next(">") or test_next(">=") or test_next("<") or test_next(">="):
			expr = BinaryExpr(expr, get_op(p.name), assign())

		return expr

	def assign(self):
		expr = primary()
		while test_next("="):
			expr = AssignExpr(expr, expr())

		return expr

	def primary(self):
		if test_next("integer-literal") or test_next("string-literal"):
			return LiteralExpr(peel().payload)
		elif test_next("identifier"):
			return SymbolReferenceExpr(expect("identifier").payload)
		elif test_next("("):
			expr = expr()
			expect(")")
			return expr
		else:
			raise Exception("Not sure what else could go here")