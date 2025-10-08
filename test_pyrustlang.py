#!/usr/bin/env python3
"""
Test suite for Pyrustlang interpreter
"""

import sys
import io
from contextlib import redirect_stdout
from pyrustlang import Lexer, Parser, Interpreter


def run_code(source: str) -> str:
    """Run Pyrustlang code and capture output"""
    output = io.StringIO()
    
    try:
        with redirect_stdout(output):
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpreter()
            interpreter.execute(ast)
        return output.getvalue()
    except Exception as e:
        return f"Error: {e}"


def test_hello_world():
    """Test basic print statement"""
    code = 'print("Hello, World!")'
    output = run_code(code)
    assert output.strip() == "Hello, World!", f"Expected 'Hello, World!', got '{output.strip()}'"
    print("✓ Hello World test passed")


def test_variables():
    """Test variable declaration and types"""
    code = """
let x: i32 = 42
print(x)
let mut y: i32 = 10
print(y)
y = 20
print(y)
"""
    output = run_code(code)
    lines = output.strip().split('\n')
    assert lines[0] == "42", f"Expected 42, got {lines[0]}"
    assert lines[1] == "10", f"Expected 10, got {lines[1]}"
    assert lines[2] == "20", f"Expected 20, got {lines[2]}"
    print("✓ Variables test passed")


def test_immutability():
    """Test immutability enforcement"""
    code = """
let x: i32 = 42
x = 10
"""
    output = run_code(code)
    assert "Cannot reassign immutable variable" in output, f"Expected immutability error, got {output}"
    print("✓ Immutability test passed")


def test_arithmetic():
    """Test arithmetic operations"""
    code = """
let a: i32 = 10
let b: i32 = 3
print(a + b)
print(a - b)
print(a * b)
"""
    output = run_code(code)
    lines = output.strip().split('\n')
    assert lines[0] == "13", f"Expected 13, got {lines[0]}"
    assert lines[1] == "7", f"Expected 7, got {lines[1]}"
    assert lines[2] == "30", f"Expected 30, got {lines[2]}"
    print("✓ Arithmetic test passed")


def test_conditionals():
    """Test if/else statements"""
    code = """
let x: i32 = 10
if x > 5 {
    print("greater")
} else {
    print("not greater")
}
"""
    output = run_code(code)
    assert output.strip() == "greater", f"Expected 'greater', got '{output.strip()}'"
    print("✓ Conditionals test passed")


def test_while_loop():
    """Test while loops"""
    code = """
let mut i: i32 = 0
while i < 3 {
    print(i)
    i = i + 1
}
"""
    output = run_code(code)
    lines = output.strip().split('\n')
    assert lines == ["0", "1", "2"], f"Expected ['0', '1', '2'], got {lines}"
    print("✓ While loop test passed")


def test_functions():
    """Test function definitions and calls"""
    code = """
fn add(x: i32, y: i32) -> i32 {
    return x + y
}
let result = add(5, 3)
print(result)
"""
    output = run_code(code)
    assert output.strip() == "8", f"Expected 8, got {output.strip()}"
    print("✓ Functions test passed")


def test_type_checking():
    """Test type checking"""
    code = """
let x: i32 = "hello"
"""
    output = run_code(code)
    assert "Expected i32" in output, f"Expected type error, got {output}"
    print("✓ Type checking test passed")


def test_comparison_operators():
    """Test comparison operators"""
    code = """
let a: i32 = 5
let b: i32 = 10
print(a < b)
print(a == 5)
print(a != b)
"""
    output = run_code(code)
    lines = output.strip().split('\n')
    assert lines[0] == "True", f"Expected True, got {lines[0]}"
    assert lines[1] == "True", f"Expected True, got {lines[1]}"
    assert lines[2] == "True", f"Expected True, got {lines[2]}"
    print("✓ Comparison operators test passed")


def test_string_operations():
    """Test string operations"""
    code = """
let name = "Alice"
let greeting = "Hello, " + name
print(greeting)
"""
    output = run_code(code)
    assert output.strip() == "Hello, Alice", f"Expected 'Hello, Alice', got '{output.strip()}'"
    print("✓ String operations test passed")


def run_all_tests():
    """Run all tests"""
    print("Running Pyrustlang Test Suite\n" + "=" * 40)
    
    tests = [
        test_hello_world,
        test_variables,
        test_immutability,
        test_arithmetic,
        test_conditionals,
        test_while_loop,
        test_functions,
        test_type_checking,
        test_comparison_operators,
        test_string_operations,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 40)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
