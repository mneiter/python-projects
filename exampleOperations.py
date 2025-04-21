# exampleOperations.py

import numpy as np

def array_operations():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    # Сложение массивов
    result = a + b
    print("Сложение массивов:", result)

    # Умножение массива на скаляр
    result = a * 3
    print("Умножение на скаляр:", result)

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the division of two numbers. Raises an error if dividing by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

if __name__ == "__main__":
    array_operations()

    x = 10
    y = 5

    print(f"{x} + {y} = {add(x, y)}")
    print(f"{x} - {y} = {subtract(x, y)}")
    print(f"{x} * {y} = {multiply(x, y)}")
    print(f"{x} / {y} = {divide(x, y)}")
    try:
        print(f"{x} / 0 = {divide(x, 0)}")
    except ValueError as e:
        print(e)
    print(f"{x} + {y} = {add(x, y)}")