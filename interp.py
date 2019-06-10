import lex
import parse
import scope
import run
import value

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
			
tokens = lexer.tokenize("let inp = input();")

parser = parse.Parser(tokens)
ast = parser.parse()

sc = scope.Scope()
sc.bind("print", value.ParamsBuiltinFunctionObject(lambda text: print(str(text))))
sc.bind("input", value.NoParamsBuiltinFunctionObject(lambda: value.StringObject(input())))
sc.bind("int", value.ParamsBuiltinFunctionObject(lambda s: value.IntObject(int(s.value))))
sc.bind("string", value.ParamsBuiltinFunctionObject(lambda i: value.StringObject(str(i.value))))


run.dispatch(sc, ast)