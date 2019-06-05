import lex

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
	lex.TokenType("equals", r'^='),
	lex.TokenType("double-equals", r'^=='),
	lex.TokenType("plus", r'^\+'),
	lex.TokenType("minus", r'^\-'),
	lex.TokenType("star", r'^\*'),
	lex.TokenType("slash", r'^\/'),
	lex.TokenType("open-brace", r'^\{'),
	lex.TokenType("close-brace", r'^\}'),
	lex.TokenType("open-bracket", r'^\['),
	lex.TokenType("close-bracket", r'^\]'),
	lex.TokenType("open-paren", r'^\('),
	lex.TokenType("close-paren", r'^\)'),
	lex.TokenType("comma", r'^\,'),
	lex.TokenType("semi-colon", r'^\;'),
]

lexer = lex.Lexer(types)

for tok in lexer.tokenize(" let fn return if else 1 \"def\" 'abc' _Abc = == + - * / {}()[],;"):
	print(tok)