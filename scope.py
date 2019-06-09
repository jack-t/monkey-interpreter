from value import Object

# lexical scopes exist on a stack: as you call functions, different symbols are "visible" to the running code.
class Scope:
	def __init__(self, parent = None):
		self.parent = parent
		self.symbols = {}

	def bind(self, key, value):
		print(key)
		print(value)
		if not isinstance(value, Object):
			raise Exception("Bound values must be Objects.")
		if key in self.symbols:
			raise Exception("Cannot let '" + key + "': it is already bound in this scope.")
		self.symbols[key] = value
		return value

	def assign(self, key, value):
		if key not in self.symbols:
			raise Exception("Cannot assign '" + key + "': it is not yet bound in this scope.")
		self.symbols[key] = value
		return value

	def get(self, key):
		if key not in self.symbols:
			if self.parent != None:
				return self.parent.get(key)
			else: raise Exception("No such symbol '" + key + "'")
		return self.symbols[key]
