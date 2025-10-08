#!/usr/bin/env python3
"""
Pyrustlang - A Programming Language Combining Python and Rust Concepts
======================================================================

A minimal interpreted language that combines:
- Python's simple syntax and dynamic features
- Rust's type annotations and ownership-inspired memory safety

Author: fidelcastrodev
"""

import re
import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List, Dict, Optional, Union


# ============================================================================
# LEXER - Tokenization
# ============================================================================

class TokenType(Enum):
    """Token types for the language"""
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords (Python-like)
    LET = auto()
    MUT = auto()  # Rust-inspired mutability
    FN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    PRINT = auto()
    
    # Type annotations (Rust-inspired)
    TYPE_I32 = auto()
    TYPE_F64 = auto()
    TYPE_STR = auto()
    TYPE_BOOL = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    ARROW = auto()
    COMMA = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    """Represents a token in the source code"""
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    """Tokenizes source code into tokens"""
    
    KEYWORDS = {
        'let': TokenType.LET,
        'mut': TokenType.MUT,
        'fn': TokenType.FN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'print': TokenType.PRINT,
        'i32': TokenType.TYPE_I32,
        'f64': TokenType.TYPE_F64,
        'str': TokenType.TYPE_STR,
        'bool': TokenType.TYPE_BOOL,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead at characters without consuming them"""
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return the current character"""
        if self.pos < len(self.source):
            char = self.source[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        """Skip whitespace except newlines"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip comments (Python-style #)"""
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (integer or float)"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def read_string(self) -> Token:
        """Read a string literal"""
        start_line = self.line
        start_col = self.column
        quote = self.advance()  # consume opening quote
        string = ''
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    string += '\n'
                elif next_char == 't':
                    string += '\t'
                elif next_char == '\\':
                    string += '\\'
                elif next_char == quote:
                    string += quote
                else:
                    string += next_char
            else:
                string += self.advance()
        
        if not self.peek():
            self.error("Unterminated string")
        
        self.advance()  # consume closing quote
        return Token(TokenType.STRING, string, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_line = self.line
        start_col = self.column
        identifier = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            identifier += self.advance()
        
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        value = identifier if token_type == TokenType.IDENTIFIER else None
        
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Convert source code into tokens"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            self.skip_comment()
            
            if self.pos >= len(self.source):
                break
            
            char = self.peek()
            start_line = self.line
            start_col = self.column
            
            # Newlines
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, None, start_line, start_col))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, None, start_line, start_col))
            elif char == '-':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, None, start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.MINUS, None, start_line, start_col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, None, start_line, start_col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, None, start_line, start_col))
            elif char == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUALS, None, start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, None, start_line, start_col))
            elif char == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUALS, None, start_line, start_col))
                else:
                    self.error(f"Unexpected character: {char}")
            elif char == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, None, start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.LESS_THAN, None, start_line, start_col))
            elif char == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, None, start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.GREATER_THAN, None, start_line, start_col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, None, start_line, start_col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, None, start_line, start_col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, None, start_line, start_col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, None, start_line, start_col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, None, start_line, start_col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, None, start_line, start_col))
            else:
                self.error(f"Unexpected character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ============================================================================
# AST - Abstract Syntax Tree
# ============================================================================

@dataclass
class ASTNode:
    """Base class for AST nodes"""
    pass


@dataclass
class NumberNode(ASTNode):
    value: Union[int, float]


@dataclass
class StringNode(ASTNode):
    value: str


@dataclass
class BoolNode(ASTNode):
    value: bool


@dataclass
class IdentifierNode(ASTNode):
    name: str


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class AssignmentNode(ASTNode):
    name: str
    type_annotation: Optional[str]
    is_mutable: bool
    value: ASTNode


@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]]


@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class FunctionDefNode(ASTNode):
    name: str
    parameters: List[tuple]  # [(name, type), ...]
    return_type: Optional[str]
    body: List[ASTNode]


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    arguments: List[ASTNode]


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode]


@dataclass
class PrintNode(ASTNode):
    value: ASTNode


# ============================================================================
# PARSER - Build AST from tokens
# ============================================================================

class Parser:
    """Parses tokens into an Abstract Syntax Tree"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current()
        raise SyntaxError(f"Line {token.line}, Column {token.column}: {msg}")
    
    def current(self) -> Token:
        """Get current token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek(self, offset: int = 1) -> Token:
        """Look ahead at tokens"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self) -> Token:
        """Move to next token"""
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume a token of expected type"""
        token = self.current()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return self.advance()
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> List[ASTNode]:
        """Parse tokens into AST"""
        statements = []
        
        while self.current().type != TokenType.EOF:
            self.skip_newlines()
            if self.current().type == TokenType.EOF:
                break
            statements.append(self.parse_statement())
            self.skip_newlines()
        
        return statements
    
    def parse_statement(self) -> ASTNode:
        """Parse a single statement"""
        token = self.current()
        
        if token.type == TokenType.LET:
            return self.parse_assignment()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        elif token.type == TokenType.FN:
            return self.parse_function_def()
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        elif token.type == TokenType.PRINT:
            return self.parse_print()
        elif token.type == TokenType.IDENTIFIER:
            # Could be assignment or function call
            if self.peek().type == TokenType.ASSIGN:
                return self.parse_reassignment()
            elif self.peek().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                self.error("Invalid statement")
        else:
            self.error(f"Unexpected token: {token.type.name}")
    
    def parse_assignment(self) -> AssignmentNode:
        """Parse variable assignment: let [mut] name: type = value"""
        self.expect(TokenType.LET)
        
        is_mutable = False
        if self.current().type == TokenType.MUT:
            is_mutable = True
            self.advance()
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        type_annotation = None
        if self.current().type == TokenType.COLON:
            self.advance()
            type_token = self.current()
            if type_token.type in [TokenType.TYPE_I32, TokenType.TYPE_F64, 
                                   TokenType.TYPE_STR, TokenType.TYPE_BOOL]:
                type_annotation = type_token.type.name.replace('TYPE_', '').lower()
                self.advance()
            else:
                self.error("Expected type annotation")
        
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return AssignmentNode(name, type_annotation, is_mutable, value)
    
    def parse_reassignment(self) -> AssignmentNode:
        """Parse variable reassignment: name = value"""
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return AssignmentNode(name, None, True, value)
    
    def parse_if(self) -> IfNode:
        """Parse if statement"""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        then_body = []
        while self.current().type != TokenType.RBRACE:
            then_body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        self.skip_newlines()
        
        else_body = None
        if self.current().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            self.skip_newlines()
            
            else_body = []
            while self.current().type != TokenType.RBRACE:
                else_body.append(self.parse_statement())
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return IfNode(condition, then_body, else_body)
    
    def parse_while(self) -> WhileNode:
        """Parse while loop"""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current().type != TokenType.RBRACE:
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return WhileNode(condition, body)
    
    def parse_function_def(self) -> FunctionDefNode:
        """Parse function definition"""
        self.expect(TokenType.FN)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        
        while self.current().type != TokenType.RPAREN:
            param_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            param_type_token = self.current()
            
            if param_type_token.type in [TokenType.TYPE_I32, TokenType.TYPE_F64,
                                          TokenType.TYPE_STR, TokenType.TYPE_BOOL]:
                param_type = param_type_token.type.name.replace('TYPE_', '').lower()
                self.advance()
            else:
                self.error("Expected type annotation")
            
            parameters.append((param_name, param_type))
            
            if self.current().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        return_type = None
        if self.current().type == TokenType.ARROW:
            self.advance()
            return_type_token = self.current()
            if return_type_token.type in [TokenType.TYPE_I32, TokenType.TYPE_F64,
                                          TokenType.TYPE_STR, TokenType.TYPE_BOOL]:
                return_type = return_type_token.type.name.replace('TYPE_', '').lower()
                self.advance()
            else:
                self.error("Expected return type annotation")
        
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current().type != TokenType.RBRACE:
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return FunctionDefNode(name, parameters, return_type, body)
    
    def parse_function_call(self) -> FunctionCallNode:
        """Parse function call"""
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        arguments = []
        
        while self.current().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current().type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return FunctionCallNode(name, arguments)
    
    def parse_return(self) -> ReturnNode:
        """Parse return statement"""
        self.expect(TokenType.RETURN)
        
        value = None
        if self.current().type not in [TokenType.NEWLINE, TokenType.EOF, TokenType.RBRACE]:
            value = self.parse_expression()
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return ReturnNode(value)
    
    def parse_print(self) -> PrintNode:
        """Parse print statement"""
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        if self.current().type == TokenType.NEWLINE:
            self.advance()
        
        return PrintNode(value)
    
    def parse_expression(self) -> ASTNode:
        """Parse expression"""
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison operators"""
        left = self.parse_additive()
        
        while self.current().type in [TokenType.EQUALS, TokenType.NOT_EQUALS,
                                       TokenType.LESS_THAN, TokenType.GREATER_THAN,
                                       TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]:
            op_token = self.advance()
            op_map = {
                TokenType.EQUALS: '==',
                TokenType.NOT_EQUALS: '!=',
                TokenType.LESS_THAN: '<',
                TokenType.GREATER_THAN: '>',
                TokenType.LESS_EQUAL: '<=',
                TokenType.GREATER_EQUAL: '>=',
            }
            operator = op_map[op_token.type]
            right = self.parse_additive()
            left = BinaryOpNode(left, operator, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.current().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            operator = '+' if op_token.type == TokenType.PLUS else '-'
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, operator, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication and division"""
        left = self.parse_primary()
        
        while self.current().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op_token = self.advance()
            operator = '*' if op_token.type == TokenType.MULTIPLY else '/'
            right = self.parse_primary()
            left = BinaryOpNode(left, operator, right)
        
        return left
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions"""
        token = self.current()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value)
        
        elif token.type in [TokenType.TRUE, TokenType.FALSE]:
            self.advance()
            return BoolNode(token.type == TokenType.TRUE)
        
        elif token.type == TokenType.IDENTIFIER:
            # Could be variable or function call
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                self.advance()
                return IdentifierNode(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {token.type.name}")


# ============================================================================
# INTERPRETER - Execute AST
# ============================================================================

class Environment:
    """Variable scope management"""
    
    def __init__(self, parent=None):
        self.variables = {}
        self.mutability = {}
        self.parent = parent
    
    def define(self, name: str, value: Any, is_mutable: bool):
        """Define a new variable"""
        if name in self.variables:
            raise NameError(f"Variable '{name}' already defined in this scope")
        self.variables[name] = value
        self.mutability[name] = is_mutable
    
    def get(self, name: str) -> Any:
        """Get variable value"""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not defined")
    
    def set(self, name: str, value: Any):
        """Set variable value (only if mutable)"""
        if name in self.variables:
            if not self.mutability[name]:
                raise ValueError(f"Cannot reassign immutable variable '{name}'")
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Variable '{name}' not defined")


@dataclass
class Function:
    """Function object"""
    parameters: List[tuple]
    body: List[ASTNode]
    closure: Environment


class ReturnValue(Exception):
    """Used to implement return statement"""
    def __init__(self, value):
        self.value = value


class Interpreter:
    """Interprets and executes the AST"""
    
    def __init__(self):
        self.global_env = Environment()
        self.functions = {}
    
    def execute(self, statements: List[ASTNode]):
        """Execute a list of statements"""
        for statement in statements:
            self.eval_node(statement, self.global_env)
    
    def eval_node(self, node: ASTNode, env: Environment) -> Any:
        """Evaluate an AST node"""
        
        if isinstance(node, NumberNode):
            return node.value
        
        elif isinstance(node, StringNode):
            return node.value
        
        elif isinstance(node, BoolNode):
            return node.value
        
        elif isinstance(node, IdentifierNode):
            return env.get(node.name)
        
        elif isinstance(node, BinaryOpNode):
            left = self.eval_node(node.left, env)
            right = self.eval_node(node.right, env)
            
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            elif node.operator == '==':
                return left == right
            elif node.operator == '!=':
                return left != right
            elif node.operator == '<':
                return left < right
            elif node.operator == '>':
                return left > right
            elif node.operator == '<=':
                return left <= right
            elif node.operator == '>=':
                return left >= right
        
        elif isinstance(node, AssignmentNode):
            value = self.eval_node(node.value, env)
            
            # Type checking (Rust-inspired)
            if node.type_annotation:
                if node.type_annotation == 'i32' and not isinstance(value, int):
                    raise TypeError(f"Expected i32, got {type(value).__name__}")
                elif node.type_annotation == 'f64' and not isinstance(value, (int, float)):
                    raise TypeError(f"Expected f64, got {type(value).__name__}")
                elif node.type_annotation == 'str' and not isinstance(value, str):
                    raise TypeError(f"Expected str, got {type(value).__name__}")
                elif node.type_annotation == 'bool' and not isinstance(value, bool):
                    raise TypeError(f"Expected bool, got {type(value).__name__}")
            
            # Check if variable exists (reassignment vs new definition)
            # If we have a type annotation, it's always a new definition
            if node.type_annotation is not None:
                # New variable definition with type annotation
                env.define(node.name, value, node.is_mutable)
            else:
                # No type annotation - could be reassignment or new definition
                try:
                    env.get(node.name)
                    # Variable exists, try to reassign
                    env.set(node.name, value)
                except NameError:
                    # New variable without type annotation (type inference)
                    env.define(node.name, value, node.is_mutable)
            
            return value
        
        elif isinstance(node, IfNode):
            condition = self.eval_node(node.condition, env)
            if condition:
                for stmt in node.then_body:
                    self.eval_node(stmt, env)
            elif node.else_body:
                for stmt in node.else_body:
                    self.eval_node(stmt, env)
        
        elif isinstance(node, WhileNode):
            while self.eval_node(node.condition, env):
                for stmt in node.body:
                    self.eval_node(stmt, env)
        
        elif isinstance(node, FunctionDefNode):
            func = Function(node.parameters, node.body, env)
            self.functions[node.name] = func
        
        elif isinstance(node, FunctionCallNode):
            if node.name not in self.functions:
                raise NameError(f"Function '{node.name}' not defined")
            
            func = self.functions[node.name]
            
            # Evaluate arguments
            args = [self.eval_node(arg, env) for arg in node.arguments]
            
            # Check argument count
            if len(args) != len(func.parameters):
                raise TypeError(f"Function '{node.name}' expects {len(func.parameters)} arguments, got {len(args)}")
            
            # Create new environment for function
            func_env = Environment(func.closure)
            
            # Bind parameters
            for (param_name, param_type), arg_value in zip(func.parameters, args):
                func_env.define(param_name, arg_value, True)
            
            # Execute function body
            try:
                for stmt in func.body:
                    self.eval_node(stmt, func_env)
                return None
            except ReturnValue as ret:
                return ret.value
        
        elif isinstance(node, ReturnNode):
            value = self.eval_node(node.value, env) if node.value else None
            raise ReturnValue(value)
        
        elif isinstance(node, PrintNode):
            value = self.eval_node(node.value, env)
            print(value)
            return value
        
        else:
            raise NotImplementedError(f"Node type {type(node).__name__} not implemented")


# ============================================================================
# MAIN - CLI Interface
# ============================================================================

def run_file(filename: str):
    """Run a Pyrustlang source file"""
    try:
        with open(filename, 'r') as f:
            source = f.read()
        
        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpretation
        interpreter = Interpreter()
        interpreter.execute(ast)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run_repl():
    """Run interactive REPL"""
    print("Pyrustlang REPL v1.0")
    print("Type 'exit' to quit\n")
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input(">>> ")
            if line.strip() == 'exit':
                break
            
            if not line.strip():
                continue
            
            # Lexical analysis
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpretation
            for node in ast:
                result = interpreter.eval_node(node, interpreter.global_env)
                if result is not None and not isinstance(node, (AssignmentNode, PrintNode, 
                                                                  FunctionDefNode, IfNode, WhileNode)):
                    print(result)
        
        except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}", file=sys.stderr)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()


if __name__ == '__main__':
    main()
