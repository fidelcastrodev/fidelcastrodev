# Pyrustlang Language Specification

## Overview

Pyrustlang is a statically-typed, interpreted programming language that combines Python's simple syntax with Rust's type safety and mutability semantics.

## Lexical Structure

### Comments
```
# Single-line comment (Python-style)
```

### Keywords
- `let` - Variable declaration
- `mut` - Mutability modifier
- `fn` - Function declaration
- `if`, `else` - Conditional statements
- `while` - Loop statement
- `return` - Return statement
- `print` - Built-in print function
- `true`, `false` - Boolean literals

### Type Keywords
- `i32` - 32-bit signed integer
- `f64` - 64-bit floating point
- `str` - String type
- `bool` - Boolean type

### Operators

#### Arithmetic
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division

#### Comparison
- `==` Equal
- `!=` Not equal
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal

#### Assignment
- `=` Assignment

### Delimiters
- `(` `)` Parentheses
- `{` `}` Braces
- `:` Colon (for type annotations)
- `->` Arrow (for function return types)
- `,` Comma (for parameter lists)

### Literals

#### Integer Literals
```
42
-10
0
```

#### Float Literals
```
3.14
-2.5
0.0
```

#### String Literals
```
"hello"
'world'
"with \"escaped\" quotes"
```

#### Boolean Literals
```
true
false
```

## Grammar

### Program
```
program ::= statement*
```

### Statements

#### Variable Declaration
```
statement ::= 'let' ['mut'] IDENTIFIER [':' type] '=' expression

Examples:
let x: i32 = 42
let mut y = 10
let name: str = "Alice"
```

#### Variable Assignment
```
statement ::= IDENTIFIER '=' expression

Examples:
x = 10
counter = counter + 1
```

#### Function Definition
```
statement ::= 'fn' IDENTIFIER '(' parameters ')' ['->' type] '{' statement* '}'
parameters ::= [IDENTIFIER ':' type (',' IDENTIFIER ':' type)*]

Examples:
fn add(x: i32, y: i32) -> i32 {
    return x + y
}

fn greet(name: str) {
    print("Hello, " + name)
}
```

#### Function Call
```
statement ::= IDENTIFIER '(' arguments ')'
arguments ::= [expression (',' expression)*]

Examples:
add(5, 3)
greet("Alice")
```

#### If Statement
```
statement ::= 'if' expression '{' statement* '}' ['else' '{' statement* '}']

Examples:
if x > 0 {
    print("positive")
} else {
    print("non-positive")
}
```

#### While Loop
```
statement ::= 'while' expression '{' statement* '}'

Examples:
while i < 10 {
    print(i)
    i = i + 1
}
```

#### Return Statement
```
statement ::= 'return' [expression]

Examples:
return 42
return x + y
return
```

#### Print Statement
```
statement ::= 'print' '(' expression ')'

Examples:
print("Hello")
print(x + y)
print(42)
```

### Expressions

#### Primary Expressions
```
expression ::= NUMBER
            | STRING
            | BOOLEAN
            | IDENTIFIER
            | function_call
            | '(' expression ')'
```

#### Binary Expressions
```
expression ::= expression '+' expression
            | expression '-' expression
            | expression '*' expression
            | expression '/' expression
            | expression '==' expression
            | expression '!=' expression
            | expression '<' expression
            | expression '>' expression
            | expression '<=' expression
            | expression '>=' expression
```

#### Operator Precedence (highest to lowest)
1. `()` Parentheses
2. `*`, `/` Multiplication, Division
3. `+`, `-` Addition, Subtraction
4. `<`, `>`, `<=`, `>=` Comparison
5. `==`, `!=` Equality

## Type System

### Basic Types

#### i32 (Integer)
32-bit signed integer. Used for whole numbers.
```
let x: i32 = 42
let y: i32 = -10
```

#### f64 (Float)
64-bit floating point number. Used for decimal numbers.
```
let pi: f64 = 3.14159
let temp: f64 = -273.15
```

#### str (String)
Text string. Supports concatenation with `+` operator.
```
let name: str = "Alice"
let greeting = "Hello, " + name
```

#### bool (Boolean)
Boolean value: `true` or `false`.
```
let is_active: bool = true
let done: bool = false
```

### Type Inference

Type annotations are optional. When omitted, the type is inferred from the value:
```
let x = 42        # Inferred as i32
let pi = 3.14     # Inferred as f64
let name = "Bob"  # Inferred as str
let flag = true   # Inferred as bool
```

### Type Checking

When a type annotation is provided, the value must match:
```
let x: i32 = 42      # OK
let y: i32 = "hello" # Error: Expected i32, got str
```

## Mutability

### Immutable Variables (Rust-inspired)
Variables declared with `let` are immutable by default:
```
let x = 42
x = 10  # Error: Cannot reassign immutable variable
```

### Mutable Variables (Rust-inspired)
Variables declared with `let mut` can be reassigned:
```
let mut x = 42
x = 10  # OK
```

## Scoping

### Lexical Scoping
Variables are lexically scoped. Inner scopes can access outer scope variables:
```
let x = 10

if true {
    print(x)  # OK: x is accessible
    let y = 20
}

print(y)  # Error: y is not in scope
```

### Function Closures
Functions capture their environment (closure):
```
let x = 10

fn print_x() {
    print(x)  # Captures x from outer scope
}
```

## Functions

### Function Declaration
Functions are declared with `fn` keyword:
```
fn function_name(param1: type1, param2: type2) -> return_type {
    # function body
    return value
}
```

### Parameters
All parameters must have type annotations:
```
fn add(x: i32, y: i32) -> i32 {
    return x + y
}
```

### Return Types
Return types are optional. If omitted, function returns nothing:
```
fn greet(name: str) {
    print("Hello, " + name)
}
```

### Return Statement
Use `return` to return a value:
```
fn square(x: i32) -> i32 {
    return x * x
}
```

## Control Flow

### If/Else Statements
```
if condition {
    # then branch
} else {
    # else branch
}
```

The `else` branch is optional:
```
if condition {
    # then branch
}
```

### While Loops
```
while condition {
    # loop body
}
```

Example:
```
let mut i: i32 = 0
while i < 10 {
    print(i)
    i = i + 1
}
```

## Built-in Functions

### print()
Prints a value to standard output:
```
print("Hello")
print(42)
print(x + y)
```

## Error Handling

### Syntax Errors
Reported with line and column information:
```
Error: Line 5, Column 10: Unexpected character: @
```

### Type Errors
Reported when type annotations don't match values:
```
Error: Expected i32, got str
```

### Runtime Errors

#### Name Error
```
Error: Variable 'x' not defined
```

#### Immutability Error
```
Error: Cannot reassign immutable variable 'x'
```

#### Division by Zero
```
Error: Division by zero
```

## Examples

### Hello World
```
print("Hello, World!")
```

### Fibonacci Sequence
```
fn fibonacci(n: i32) -> i32 {
    if n <= 1 {
        return n
    }
    
    let mut a: i32 = 0
    let mut b: i32 = 1
    let mut i: i32 = 2
    
    while i <= n {
        let mut temp = a + b
        a = b
        b = temp
        i = i + 1
    }
    
    return b
}

let mut counter: i32 = 0
while counter < 10 {
    print(fibonacci(counter))
    counter = counter + 1
}
```

### Factorial
```
fn factorial(n: i32) -> i32 {
    if n <= 1 {
        return 1
    }
    let mut result: i32 = 1
    let mut i: i32 = 2
    while i <= n {
        result = result * i
        i = i + 1
    }
    return result
}

print(factorial(5))  # 120
```

## Implementation Notes

### Interpreter Architecture
1. **Lexer** - Tokenizes source code into tokens
2. **Parser** - Builds Abstract Syntax Tree (AST) from tokens
3. **Interpreter** - Evaluates AST nodes

### Type Checking
Type checking is performed at runtime when:
- Variables are assigned with type annotations
- Function parameters are passed
- Return values are returned

### Memory Model
- Variables are stored in environments (scopes)
- Functions capture their defining environment (closures)
- No explicit memory management required

## Future Enhancements

Potential features for future versions:
- For loops with ranges
- Arrays/lists
- Dictionaries/maps
- Structs/classes
- Pattern matching
- Module system
- Error handling (Result/Option types)
- Ownership and borrowing tracking
- Compile to bytecode for performance
