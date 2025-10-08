
# Hi there 👋 

I am a computer software and hardware enthusiast, who has learnt a variety of programming languages and frameworks in his free time.

## Pyrustlang - A Python/Rust Hybrid Programming Language

**Pyrustlang** is a minimal, interpreted programming language that combines:
- **Python's** simple syntax and ease of use
- **Rust's** type safety and ownership-inspired mutability model

### Features

- ✅ **Type Annotations** (Rust-inspired): `i32`, `f64`, `str`, `bool`
- ✅ **Mutability Control** (Rust-inspired): `let` (immutable) vs `let mut` (mutable)
- ✅ **Simple Syntax** (Python-inspired): Clean, readable code
- ✅ **Functions** with type annotations
- ✅ **Control Flow**: if/else, while loops
- ✅ **Arithmetic Operations**: +, -, *, /
- ✅ **Comparison Operators**: ==, !=, <, >, <=, >=
- ✅ **Comments**: Python-style `#` comments

### Installation

No installation required! Just Python 3.6+.

```bash
chmod +x pyrustlang.py
./pyrustlang.py <filename.prl>
```

Or run the REPL:
```bash
python3 pyrustlang.py
```

### Quick Start

#### Hello World
```pyrustlang
# hello.prl
print("Hello, World!")
```

#### Variables with Type Safety
```pyrustlang
# Immutable variable (Rust-inspired)
let x: i32 = 42

# Mutable variable (Rust-inspired)
let mut y: i32 = 10
y = 20  # OK

# Type inference (Python-like)
let name = "Alice"
```

#### Functions
```pyrustlang
fn add(x: i32, y: i32) -> i32 {
    return x + y
}

let sum = add(5, 3)
print(sum)  # 8
```

#### Control Flow
```pyrustlang
let age: i32 = 18

if age >= 18 {
    print("You are an adult")
} else {
    print("You are a minor")
}
```

#### Loops
```pyrustlang
let mut counter: i32 = 0
while counter < 5 {
    print(counter)
    counter = counter + 1
}
```

### Language Syntax

#### Data Types
- `i32` - 32-bit integer
- `f64` - 64-bit floating point
- `str` - String
- `bool` - Boolean (true/false)

#### Variable Declaration
```pyrustlang
let x: i32 = 42        # Immutable (cannot be reassigned)
let mut y: i32 = 10    # Mutable (can be reassigned)
let name = "Alice"     # Type inference
```

#### Functions
```pyrustlang
fn function_name(param1: type1, param2: type2) -> return_type {
    # function body
    return value
}
```

#### Operators
- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Assignment: `=`

#### Control Flow
```pyrustlang
# If statement
if condition {
    # code
} else {
    # code
}

# While loop
while condition {
    # code
}
```

### Examples

Check out the `examples/` directory for more:
- `hello.prl` - Hello World
- `variables.prl` - Variable declarations and types
- `arithmetic.prl` - Arithmetic operations
- `conditionals.prl` - If/else statements
- `loops.prl` - While loops
- `functions.prl` - Function definitions
- `fibonacci.prl` - Fibonacci sequence

### Running Examples

```bash
python3 pyrustlang.py examples/hello.prl
python3 pyrustlang.py examples/fibonacci.prl
```

### Language Design Philosophy

Pyrustlang combines the best of both worlds:

**From Python:**
- Simple, clean syntax
- Easy to read and write
- Dynamic features with optional type hints

**From Rust:**
- Explicit mutability (`let` vs `let mut`)
- Type annotations for safety
- Function signatures with return types
- Ownership-inspired variable semantics

### Implementation

Pyrustlang is implemented in Python and consists of:
1. **Lexer** - Tokenizes source code
2. **Parser** - Builds Abstract Syntax Tree (AST)
3. **Interpreter** - Executes the AST

The interpreter includes:
- Type checking for annotated variables
- Immutability enforcement
- Lexical scoping with closures
- First-class functions

### Future Enhancements

Potential future features:
- For loops
- Lists/arrays
- Structs/classes
- Pattern matching
- Memory ownership tracking
- Compile to bytecode
- Standard library

### Contributing

This is a learning project demonstrating language design principles. Feel free to fork and experiment!

### License

Open source - feel free to use and modify.
