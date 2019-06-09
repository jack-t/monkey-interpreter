from ast import *

class Object:
	def to_string(self):
		return StringObject("[Object]")

	def translate_operation_name(self, op):
		if op == BinaryOp.ADD: return "add"
		elif op == BinaryOp.SUB: return "subtract"
		elif op == BinaryOp.MULT: return "multiply"
		elif op == BinaryOp.DIV: return "divide"
		elif op == BinaryOp.EQUALS: return "is_equal"
		elif op == BinaryOp.NOT_EQUALS: return "is_not_equal"
		elif op == BinaryOp.GREATER: return "is_greater"
		elif op == BinaryOp.GREATER_EQ: return "is_greater_or_equal"
		elif op == BinaryOp.LESS: return "is_less"
		elif op == BinaryOp.LESS_EQ: return "is_less_or_equal"
		else: return op

	def invoke(self, operation, *args):
		name = self.translate_operation_name(operation)
		method = getattr(self, name)
		if method is None:
			raise Exception(self.to_string() + " does not respond to '" + name + "'")
		method.__call__(*args)

class StringObject(Object):
	def __init__(self, value):
		self.value = value

	def to_string(self):
		return StringObject(value)

	def check_type(self, other):
		if not isinstance(other, StringObject):
			raise Exception("Type mismatch error.")

	def add(self, other):
		self.check_type(other)
		return StringObject(self.value + other.value)

class IntObject(Object):
	def __init__(self, value):
		self.value = value

	def to_string(self):
		return StringObject(str(value))

	def check_type(self, other):
		if not isinstance(other, IntObject):
			raise Exception("Type mismatch error.")

	def add(self, other):
		self.check_type(other)
		return IntObject(self.value + other.value)

	def subtract(self, other):
		self.check_type(other)
		return IntObject(self.value - other.value)
		
	def multiply(self, other):
		self.check_type(other)
		return IntObject(self.value * other.value)

	def divide(self, other):
		self.check_type(other)
		return IntObject(self.value / other.value)

class BoolObject(Object):
	def __init__(self, value):
		self.value = value

	def to_string(self):
		if self.value:
			return StringObject("true")
		else:
			return StringObject("false")

	def is_equal(self, other):
		return self.value == other.value

# doesn't have a name b/c one func could be bound in several places
class FunctionObject(Object):
	def __init__(self, scope, params, expr):
		self.scope = scope
		self.params = params
		self.expr = expr

	def apply(self, args):
		print("Invoking '" + self.name + "'")