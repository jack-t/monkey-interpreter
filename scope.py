import value

# lexical scopes exist on a stack: as you call functions, different symbols are "visible" to the running code.
class Scope:
	def __init__(self, parent = None):
		self.parent = parent
		self.symbols = {}

	def bind(self, key, val):
		print("binding "+key+ " to "+str(val))
		if not isinstance(val, value.Object):
			raise Exception("Bound values must be Objects.")
		if key in self.symbols:
			raise Exception("Cannot let '" + key + "': it is already bound in this scope.")
		self.symbols[key] = val
		return val

	def assign(self, key, val):
		if not isinstance(val, value.Object):
			raise Exception("Bound values must be Objects.")
		if key not in self.symbols:
			raise Exception("Cannot assign '" + key + "': it is not yet bound in this scope.")
		self.symbols[key] = val
		return val

	def get(self, key):
		if key not in self.symbols:
			if self.parent != None:
				return self.parent.get(key)
			else: raise Exception("No such symbol '" + key + "'")
		return self.symbols[key]
