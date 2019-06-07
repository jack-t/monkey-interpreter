import re
from enum import Enum

class TokenPayloadType(Enum):
	STRING = 0
	INT = 1
	FLOAT = 2

class TokenType:
	def __init__(self, name, regex, payload_group = None, payload_type = None):
		self.name = name
		self.regex = re.compile(regex)
		if payload_group and payload_type == None:
			raise Exception("Can't have a None-typed payload")
		self.payload_group = payload_group
		self.payload_type = payload_type


class Token:
	def __init__(self, name, payload = None):
		self.name = name
		self.payload = payload
	def __str__(self):
		if self.payload != None:
			return self.name + " {" + str(self.payload) + "}"
		else:
			return "`" + self.name + "`"

def text_type(text):
	return TokenType(text, r"^" + text + r"\b")

class Lexer:
	def __init__(self, token_types):
		self.token_types = token_types

	def tokenize(self, code):
		tokens = []
		code = code.lstrip()
		while code:
			token = self.tokenize_one(code)
			tokens.append(token[0])
			code = code[token[1]:].lstrip() # chop off the leading part

		return tokens

	def tokenize_one(self, code):
		for tok in self.token_types:
			result = tok.regex.match(code)
			if result != None:
				return (Token(tok.name, self.get_payload(result, tok.payload_group, tok.payload_type)), result.end())
		raise Exception("Couldn't match code starting at '" + code + "'")

	def get_payload(self, match, name, type):
		if type is TokenPayloadType.STRING:
			return match.group(name)
		elif type is TokenPayloadType.INT:
			return int(match.group(name))
		elif type is TokenPayloadType.FLOAT:
			return float(match.group(name))
		else:
			None