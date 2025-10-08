# Pyrustlang Quick Start Guide

Get started with Pyrustlang in 5 minutes!

## Installation

No installation needed! Just Python 3.6+.

```bash
# Make the interpreter executable
chmod +x pyrustlang.py
```

## Running Your First Program

### Method 1: Run a file
```bash
python3 pyrustlang.py examples/hello.prl
```

### Method 2: Use the REPL
```bash
python3 pyrustlang.py
```

Then type:
```pyrustlang
>>> print("Hello, World!")
Hello, World!
>>> let x: i32 = 42
>>> print(x)
42
>>> exit
```

## Your First Program

Create a file `my_program.prl`:

```pyrustlang
# Variables with types (Rust-inspired)
let name: str = "Alice"
let age: i32 = 25

# Print output
print("Name: " + name)
print(age)

# Mutable variables
let mut counter: i32 = 0
while counter < 3 {
    print(counter)
    counter = counter + 1
}

# Functions
fn greet(person: str) -> str {
    return "Hello, " + person + "!"
}

print(greet(name))
```

Run it:
```bash
python3 pyrustlang.py my_program.prl
```

## Language Basics

### Variables

```pyrustlang
# Immutable (default) - Rust-inspired
let x: i32 = 10

# Mutable - can be changed
let mut y: i32 = 20
y = 30  # OK

# Type inference - Python-like
let name = "Bob"  # inferred as str
```

### Types

- `i32` - Integer (42, -10)
- `f64` - Float (3.14, -2.5)
- `str` - String ("hello")
- `bool` - Boolean (true, false)

### Arithmetic

```pyrustlang
let a: i32 = 10
let b: i32 = 3
print(a + b)  # 13
print(a - b)  # 7
print(a * b)  # 30
print(a / b)  # 3.333...
```

### Comparisons

```pyrustlang
let x: i32 = 5
print(x == 5)    # true
print(x != 10)   # true
print(x < 10)    # true
print(x >= 5)    # true
```

### If/Else

```pyrustlang
let age: i32 = 18

if age >= 18 {
    print("Adult")
} else {
    print("Minor")
}
```

### Loops

```pyrustlang
let mut i: i32 = 0
while i < 5 {
    print(i)
    i = i + 1
}
```

### Functions

```pyrustlang
# Function with return type
fn add(x: i32, y: i32) -> i32 {
    return x + y
}

# Function without return
fn greet(name: str) {
    print("Hello, " + name)
}

let sum = add(5, 3)
print(sum)  # 8

greet("World")  # Hello, World
```

## Try the Examples

We've included several example programs:

```bash
# Hello World
python3 pyrustlang.py examples/hello.prl

# Variables and types
python3 pyrustlang.py examples/variables.prl

# Arithmetic operations
python3 pyrustlang.py examples/arithmetic.prl

# If/else statements
python3 pyrustlang.py examples/conditionals.prl

# While loops
python3 pyrustlang.py examples/loops.prl

# Functions
python3 pyrustlang.py examples/functions.prl

# Fibonacci sequence
python3 pyrustlang.py examples/fibonacci.prl

# Complete feature demo
python3 pyrustlang.py examples/demo.prl
```

## Common Patterns

### Counter Loop
```pyrustlang
let mut i: i32 = 0
while i < 10 {
    print(i)
    i = i + 1
}
```

### String Building
```pyrustlang
let first = "Hello"
let second = "World"
let combined = first + ", " + second + "!"
print(combined)  # Hello, World!
```

### Conditional Logic
```pyrustlang
fn max(a: i32, b: i32) -> i32 {
    if a > b {
        return a
    } else {
        return b
    }
}

print(max(10, 5))  # 10
```

### Simple Calculator
```pyrustlang
fn calculate(op: str, a: i32, b: i32) -> i32 {
    if op == "+" {
        return a + b
    } else {
        if op == "-" {
            return a - b
        } else {
            if op == "*" {
                return a * b
            } else {
                return a / b
            }
        }
    }
}

print(calculate("+", 10, 5))  # 15
print(calculate("*", 10, 5))  # 50
```

## Tips

1. **Type annotations are optional** - Use them for clarity and type safety
2. **Variables are immutable by default** - Use `let mut` when you need to change a value
3. **Functions need type annotations** - All parameters and return types must be specified
4. **Scoping works like Python** - Inner scopes can access outer variables
5. **Comments start with #** - Just like Python

## What's Different from Python?

- Variables are immutable by default (like Rust)
- Type annotations use `:` syntax (like Rust)
- Function syntax uses `fn` keyword (like Rust)
- Code blocks use `{}` instead of indentation (like Rust)

## What's Different from Rust?

- Much simpler type system (no lifetimes, ownership, borrowing)
- Interpreted, not compiled
- Dynamic features with optional type checking
- Simpler syntax overall

## Next Steps

1. Read the full [README.md](README.md) for more details
2. Check out [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) for complete language specification
3. Run the test suite: `python3 test_pyrustlang.py`
4. Experiment with the REPL: `python3 pyrustlang.py`
5. Build your own programs!

## Need Help?

- Check the examples in the `examples/` directory
- Read the language specification in `LANGUAGE_SPEC.md`
- Look at the test suite in `test_pyrustlang.py` for more examples

Happy coding with Pyrustlang! 🚀
