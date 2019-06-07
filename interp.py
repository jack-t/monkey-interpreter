import lex
import parse

types = [
	lex.text_type("let"),
	lex.text_type("fn"),
	lex.text_type("return"),
	lex.text_type("if"),
	lex.text_type("else"),
	lex.text_type("true"),
	lex.text_type("false"),
	lex.TokenType("integer-literal", r'^([0-9]+)\b', 1, lex.TokenPayloadType.INT),
	lex.TokenType("string-literal", r'^([\"\'])(?P<payload>.*?)(\1)', "payload", lex.TokenPayloadType.STRING),
	lex.TokenType("identifier", r'^(_*?[a-zA-Z]\w*)\b', 1, lex.TokenPayloadType.STRING),
	lex.TokenType("=", r'^='),
	lex.TokenType("==", r'^=='),
	lex.TokenType("+", r'^\+'),
	lex.TokenType("-", r'^\-'),
	lex.TokenType("*", r'^\*'),
	lex.TokenType("/", r'^\/'),
	lex.TokenType("{", r'^\{'),
	lex.TokenType("}", r'^\}'),
	lex.TokenType("[", r'^\['),
	lex.TokenType("]", r'^\]'),
	lex.TokenType("(", r'^\('),
	lex.TokenType(")", r'^\)'),
	lex.TokenType(",", r'^\,'),
	lex.TokenType(";", r'^\;'),
	lex.TokenType(">", r'^\>'),
	lex.TokenType("<", r'^\<'),
	lex.TokenType("<=", r'^\<\='),
	lex.TokenType(">=", r'^\>\='),
]

lexer = lex.Lexer(types)
			
tokens = lexer.tokenize("let y = fn(a,b){let x = fn(c,d){c+d}; x(a,b)};")

parser = parse.Parser(tokens)
print(parser.parse())

