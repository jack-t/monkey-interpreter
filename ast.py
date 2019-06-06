from typing import NamedTuple, List
from enum import Enum

# unlike exprs, statements don't have value
class Statement:
	pass

class Expr:
	pass

class ExprStatement(Statement):
	expr: Expr

class Block(NamedTuple, Expr):
	expr: Expr
	next_expr: Expr

class LValue(NamedTuple):
	identifier: str

class LetStmt(NamedTuple, Statement):
	bound: LValue
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
	rhs: Expr
	op: BinaryOp

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

class FuncLiteralExpr(Expr):
	param_names: List[str]
	statement: Expr

class LiteralExpr(Expr):
	def __init__(self, value):
		if isinstance(value, int) or isinstance(value, string):
			self.value = value
		else:
			raise Exception("literals can only be ints or strings")

class ConditionalExpr(Expr):
	condition: Expr
	true_stmt: Expr
	false_stmt: Expr

class LoopExpr(Expr):
	condition: Expr
	body: Expr