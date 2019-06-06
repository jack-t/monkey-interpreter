import lex

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens

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

	def test_next(self, token):
		tok = peek()
		return tok.name == token

	def expr(self):
		if test_next("let"):
			