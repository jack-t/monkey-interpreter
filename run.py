from ast import *
from value import *
from scope import Scope

def dispatch(scope, ast):
	if isinstance(ast, Program):
		return dispatch_program(scope, ast)
	elif isinstance(ast, ExprStmt):
		return dispatch_expr_stmt(scope, ast)
	elif isinstance(ast, LetStmt):
		return dispatch_let_stmt(scope, ast)
	elif isinstance(ast, FuncLiteralExpr):
		return dispatch_fn_lit(scope, ast)
	elif isinstance(ast, FuncApplicationExpr):
		return dispatch_call(scope, ast)
	elif isinstance(ast, Block):
		return dispatch_block(scope, ast)
	elif isinstance(ast, ConditionalExpr):
		return dispatch_if_expr(scope, ast)
	elif isinstance(ast, BinaryExpr):
		return dispatch_binary_op(scope, ast)
	elif isinstance(ast, AssignExpr):
		return dispatch_assign(scope, ast)
	elif isinstance(ast, LiteralExpr):
		return dispatch_literal(scope, ast)
	elif isinstance(ast, SymbolReferenceExpr):
		return dispatch_symbol(scope, ast)
	else:
		raise Exception("Can't dispatch " + str(ast))

def dispatch_program(scope, ast):
	for stmt in ast.stmts:
		dispatch(scope, stmt)

# stmt dispatches don't return anything; they can't be composed except through blocks
def dispatch_expr_stmt(scope, ast):
	dispatch(scope, ast.expr)

def dispatch_let_stmt(scope, ast):
	scope.bind(ast.binding.identifier, dispatch(scope, ast.expr))

def dispatch_fn_lit(scope, ast):
	return FunctionObject(Scope(scope), ast.param_names, lambda s: dispatch(s,ast.expr) )

def dispatch_call(scope, ast):
	func = dispatch(scope, ast.func)
	print("func: " + str(func))
	args = []
	for arg in ast.arguments:
		args.append(dispatch(scope, arg))
	return func.invoke("apply", *args)

def dispatch_block(scope, ast):
	for stmt in ast.stmts:
		dispatch(scope, stmt)
	if ast.return_expr is not None:
		return dispatch(scope, ast.return_expr)
	else:
		return None

def dispatch_if_expr(scope, ast):
	switch = dispatch(ast.condition)

	if switch.is_equal(BoolObject(True)):
		return dispatch(ast.true)
	elif ast.false is not None:
		return dispatch(ast.false)
	else:
		return None

def dispatch_binary_op(scope, ast):
	lhs = dispatch(scope, ast.lhs)
	rhs = dispatch(scope, ast.rhs)
	return lhs.invoke(ast.op, rhs)

def dispatch_assign(scope, ast):
	return scope.assign(ast.lvalue.identifier, dispatch(ast.rvalue))

def dispatch_literal(scope, ast):
	if isinstance(ast.value, int):
		return IntObject(ast.value)
	elif isinstance(ast.value, str):
		return StringObject(ast.value)

def dispatch_symbol(scope, ast):
	return scope.get(ast.identifier)