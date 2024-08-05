import ply.yacc as yacc
from csvpath.matching.matching_lexer import MatchingLexer
from csvpath.parser_utility import ParserUtility
from csvpath.matching.expression_encoder import ExpressionEncoder
from .productions import *
from .functions.function_factory import FunctionFactory
from ..exceptions import InputException
from typing import Any


class Matcher:
    tokens = MatchingLexer.tokens

    def __init__(self, *, csvpath=None, data=None, line=None, headers=None):
        if not headers:
            # raise Exception("no headers!")
            print("\nWARNING: no headers available. this is only Ok for unit testing.")
        if not data:
            raise InputException(f"need data input: data: {data}")
        self.path = data
        self.csvpath = csvpath
        self.line = line
        self.headers = headers
        self.expressions = []
        self.header_dict = None
        self.if_all_match = []
        if data is not None:
            self.lexer = MatchingLexer()
            self.parser = yacc.yacc(module=self, start="match_part")
            self.parser.parse(data, lexer=self.lexer.lexer)

    def __str__(self):
        return f"""
            line: {self.line}
            csvpath: {self.csvpath}
            parser: {self.parser}
            lexer: {self.lexer}
        """

    def to_json(self, e) -> str:
        return ExpressionEncoder().to_json(e)

    def reset(self):
        for expression in self.expressions:
            expression[1] = None
            expression[0].reset()

    def header_index(self, name: str) -> int:
        if not self.headers:
            return None
        if not self.header_dict:
            self.header_dict = {}
            for i, n in enumerate(self.headers):
                self.header_dict[n] = i
        return self.header_dict.get(name)

    def header_name(self, i: int) -> str:
        if not self.headers:
            return None
        if i < 0 or i >= len(self.headers):
            return None
        return self.headers[i]

    def header_value(self, name: str) -> Any:
        n = self.header_index(name)
        ret = None
        if n is None:
            pass
        else:
            ret = self.line[n]
        return ret

    def matches(self, *, syntax_only=False) -> bool:
        ret = True
        failed = False
        for i, et in enumerate(self.expressions):
            if et[1] is True:
                ret = True
            elif et[1] is False:
                ret = False
            elif not et[0].matches(skip=[]) and not syntax_only:
                et[1] = False
                ret = False
            else:
                et[1] = True
                ret = True
            if not ret:
                failed = True
            if failed:
                ret = False
        if ret is True:
            self.do_set_if_all_match()
        else:
            pass
        return ret

    def do_set_if_all_match(self) -> None:
        for _ in self.if_all_match:
            name = _[0]
            value = _[1]
            self.set_variable(name, value=value)
        self.if_all_match = []

    def set_if_all_match(self, name: str, value: Any) -> None:
        self.if_all_match.append((name, value))

    def get_variable(self, name: str, *, tracking=None, set_if_none=None) -> Any:
        return self.csvpath.get_variable(
            name, tracking=tracking, set_if_none=set_if_none
        )

    def set_variable(self, name: str, *, value: Any, tracking=None) -> None:
        return self.csvpath.set_variable(name, value=value, tracking=tracking)

    def last_header_index(self) -> int:
        if self.line and len(self.line) > 0:
            return len(self.line) - 1
        return None

    def last_header_name(self) -> str:
        if self.headers and len(self.headers) > 0:
            return self.headers[self.last_header_index()]
        return None

    # ===================
    # productions
    # ===================

    def p_error(self, p):
        ParserUtility().error(self.parser, p)
        raise InputException("halting for error")

    def p_match_part(self, p):
        """match_part : LEFT_BRACKET expression RIGHT_BRACKET
        | LEFT_BRACKET expressions RIGHT_BRACKET
        """

    def p_expressions(self, p):
        """expressions : expression
        | expression COMMENT
        | expressions expression
        | COMMENT expressions
        | expressions COMMENT
        """

    #        | COMMENT expression

    def p_expression(self, p):
        """expression : function
        | assignment_or_equality
        """
        e = Expression(self)
        e.add_child(p[1])
        self.expressions.append([e, None])
        p[0] = e

    def p_function(self, p):
        """function : SIMPLE_NAME OPEN_PAREN CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN equality CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN function CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN term CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN var_or_header CLOSE_PAREN
        """
        name = p[1]
        child = p[3] if p and len(p) == 5 else None
        f = FunctionFactory.get_function(self, name=name, child=child)
        p[0] = f

    def p_assignment_or_equality(self, p):
        """assignment_or_equality : equality
        | assignment
        """
        p[0] = p[1]

    def p_equality(self, p):
        """
        equality : function op term
                 | function op function
                 | function op var_or_header
                 | function DO assignment_or_equality
                 | var DO assignment_or_equality
                 | var DO function
                 | function DO function
                 | equality DO assignment_or_equality
                 | equality DO function
                 | var_or_header op function
                 | var_or_header op term
                 | var_or_header op var_or_header
                 | term op var_or_header
                 | term op term
                 | term op function
                 | equality op equality
                 | equality op term
                 | equality op function
        """
        e = Equality(self)
        e.left = p[1]
        e.set_operation(p[2])
        e.right = p[3]
        p[0] = e

    def p_op(self, p):
        """op : EQUALS
        | LT
        | GT
        | STAR
        | PLUS
        | MINUS
        | COMMA
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : var ASSIGNMENT var
                 | var ASSIGNMENT term
                 | var ASSIGNMENT function
                 | var ASSIGNMENT header
        """
        e = Equality(self)
        e.left = p[1]
        e.set_operation(p[2])
        e.right = p[3]
        p[0] = e

    def p_term(self, p):
        """term : QUOTED
        | QUOTE DATE QUOTE
        | QUOTE NUMBER QUOTE
        | NUMBER
        | REGEX
        """
        if len(p) == 4:
            p[0] = Term(self, value=p[2])
        else:
            p[0] = Term(self, value=p[1])

    def p_var_or_header(self, p):
        """var_or_header : header
        | var
        """
        p[0] = p[1]

    def p_var(self, p):
        """var : VAR_SYM SIMPLE_NAME"""
        v = Variable(self, name=p[2])
        p[0] = v

    def p_header(self, p):
        """header : HEADER_SYM SIMPLE_NAME
        | HEADER_SYM NUMBER
        | HEADER_SYM QUOTED
        """
        h = Header(self, name=p[2])
        p[0] = h
