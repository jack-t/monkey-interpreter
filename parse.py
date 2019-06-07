import lex
from ast import *

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.states = []

	def peek(self):
		if len(self.tokens) >= 1:
			return self.tokens[0]
		else:
			raise Exception("Too few tokens left in the stream")

	def peel(self):
		if len(self.tokens) >= 1:
			ret = self.tokens[0]
			self.tokens = self.tokens[1:]
			return ret
		else:
			raise Exception("Too few tokens left in the stream")

	def expect(self, token):
		tok = self.peel()
		if tok == None or tok.name != token:
			raise Exception("expected '" + token + "'; got " + str(tok))
		else:
			return tok

	def test_next(self, token):
		tok = self.peek()
		return tok.name == token

	def mark(self):
		self.states.append(self.tokens)
	def drop(self):
		self.states.pop()

	def backtrack(self):
		self.tokens = self.states.pop()

	def parse(self):
		stmts = []
		while len(self.tokens) > 0:
			stmts.append(self.stmt())

		return Program(stmts)

	# statements are either let bindings or expr statements. Both end with semicolons
	def stmt(self):
		stmt = None
		if not self.test_next("let"):
			ex = self.expr()
			stmt = ExprStmt(ex)
		else:
			self.expect("let")
			name = self.expect("identifier").payload
			self.expect("=")
			ex = self.expr()
			stmt = LetStmt(name, ex)

		self.expect(";")
		return stmt

	def expr(self):
		expr = None
		if self.test_next("{"):
			expr = self.block()
		elif self.test_next("if"):
			expr = self.if_expr()
		elif self.test_next("fn"):
			expr = self.fn_lit()
		else:
			expr = self.add()

		if self.test_next("("):
			return self.call(expr)
		else:
			return expr

	def fn_lit(self):
		self.expect("fn")
		self.expect("(")		

		params = []
		while not self.test_next(")"):
			params.append(self.expect("identifier").payload)
			if self.test_next(","):
				self.expect(",")


		self.expect(")")

		expr = self.expr()

		return FuncLiteralExpr(params, expr)


	def call(self, func):
		self.expect("(")
		params = []
		while not self.test_next(")"):
			params.append(self.expr())
			if self.test_next(","):
				self.expect(",")
		self.expect(")")

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
		self.expect("{")
		stmts = []

		while not self.test_next("}"):
			self.mark()
			try:
				stmts.append(self.stmt())
				self.drop() # this can't be in a finally block
			except:
				self.backtrack()
				expr = self.expr()
				self.expect("}")
				return Block(stmts, expr) # you're only allowed one expression at the end

		self.expect("}")
		return Block(stmts, None)

	def if_expr(self):
		self.expect("if")
		condition = expr()
		true = expr()
		false = None
		if self.test_next("else"):
			false = expr()
		return ConditionalExpr(condition, true, false)

	def mult(self):
		expr = self.cmp()
		while self.test_next("*") or self.test_next("/"):
			expr = BinaryExpr(expr, self.get_op(self.peel().name), self.cmp())

		return expr

	def add(self):
		expr = self.mult()
		while self.test_next("+") or self.test_next("-"):
			expr = BinaryExpr(expr, self.get_op(self.peel().name), self.mult())

		return expr

	def cmp(self):
		expr = self.assign()
		while self.test_next(">") or self.test_next(">=") or self.test_next("<") or self.test_next(">="):
			expr = BinaryExpr(expr, self.get_op(self.peel().name), self.assign())

		return expr

	def assign(self):
		expr = self.primary()
		while self.test_next("="):
			self.expect("=")
			expr = AssignExpr(expr, self.expr())

		return expr

	def primary(self):
		if self.test_next("integer-literal") or self.test_next("string-literal"):
			return LiteralExpr(self.peel().payload)
		elif self.test_next("identifier"):
			return SymbolReferenceExpr(self.expect("identifier").payload)
		elif self.test_next("("):
			self.expect("(")
			expr = self.expr()
			self.expect(")")
			return expr
		else:
			raise Exception("Not sure what else could go here: " + ", ".join(map(str, self.tokens)))