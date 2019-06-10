from typing import NamedTuple, List
from enum import Enum

# unlike exprs, statements don't have value
class Statement:
	pass

class Program(NamedTuple):
	stmts: List[Statement]

class Expr:
	pass

class ExprStmt(NamedTuple, Statement):
	expr: Expr

# both are optional: if you have only an expr, then you execute an expression and return its value; only a statement, execute it and return Void
# if you've got both, then you execute the statements, then the expression
# this is basically how Rust works
class Block(NamedTuple, Expr):
	stmts: List[Statement]
	return_expr: Expr

class LValue(NamedTuple):
	identifier: str

class LetStmt(NamedTuple, Statement):
	binding: LValue
	expr: Expr

class AssignExpr(NamedTuple, Expr):
	lvalue: LValue
	rvalue: Expr

class BinaryOp(Enum):
	MULT = 0
	DIV = 1
	ADD = 2
	SUB = 3
	EQUALS = 4
	NOT_EQUALS = 5
	GREATER = 6
	GREATER_EQ = 7
	LESS = 8
	LESS_EQ = 9
	AND = 10
	OR = 11

class BinaryExpr(NamedTuple, Expr):
	lhs: Expr
	op: BinaryOp
	rhs: Expr

class UnaryOp(Enum):
	NEGATION = 0
	NOT = 1 # boolean, but isn't this just the same as negation?

class UnaryExpr(NamedTuple, Expr):
	expr: Expr
	op: UnaryOp

class SymbolReferenceExpr(NamedTuple, Expr):
	identifier: str	

class FuncApplicationExpr(NamedTuple, Expr):
	func: Expr
	arguments: List[Expr]

class FuncLiteralExpr(NamedTuple, Expr):
	param_names: List[str]
	expr: Expr

class LiteralExpr(Expr):
	def __init__(self, value):
		if isinstance(value, int) or isinstance(value, str):
			self.value = value
		else:
			raise Exception("literals can only be ints or strings")
	def __repr__(self):
		if isinstance(self.value, int):
			return "literal {" + str(self.value) + "}"
		else:
			return "literal {\"" + self.value + "\"}"

class ConditionalExpr(Expr):
	condition: Expr
	true: Expr
	false: Expr

class LoopExpr(Expr):
	condition: Expr
	body: Expr