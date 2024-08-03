from lark import Lark, Transformer

# Define the grammar
flow_grammar = """
    start: assignment+
    assignment: VAR "=" expression
    expression: sequence | parallel | BRIDGE
    sequence: "(" expression ">>" expression (">>" expression)* ")"
    parallel: "(" expression "||" expression ("," IDENTIFIER)? ")"
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    VAR: IDENTIFIER
    BRIDGE: IDENTIFIER
    %import common.WS
    %ignore WS
    %import common.ESCAPED_STRING   -> STRING

"""

# Create the parser
flow_parser = Lark(flow_grammar, start='start')

# Define a transformer to convert the parse tree to a more useful structure
class TreeToAst(Transformer):
    def assignment(self, items):
        for i in items: print(i)
        return ('assign', items[0], items[1])
    
    def sequence(self, items):
        return ('seq', items)

    def parallel(self, items):
        return ('par', items)
    
    def IDENTIFIER(self, items):
        return str(items)


def test():
    # Test input
    input_data = """
    s1 = (b_m64 >> b_m128 >> b_m256)
    s2 = (denseint8 >> densef32)
    p1 = (s2 || bm25, rrf)
    p2 = (p1 || s1) 
    end = (p2 >> late)
    """

    # Parse the input
    parse_tree = flow_parser.parse(input_data)
    # Transform the parse tree to an AST
    ast = TreeToAst().transform(parse_tree)
    print(ast)

