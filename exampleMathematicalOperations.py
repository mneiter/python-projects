import numpy as np
from functools import wraps

history = []

def log_operation(func):
    """Decorator to log operations into history."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        operation = f"{func.__name__.capitalize()}({', '.join(map(str, args))}) = {result}"
        history.append(operation)
        return result
    return wrapper

def add(a, b):
    return np.add(a, b)

def subtract(a, b):
    return np.subtract(a, b)

def multiply(a, b):
    return np.multiply(a, b)

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return np.divide(a, b)

def power(a, b):
    return np.power(a, b)

def square_root(a):
    if a < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return np.sqrt(a)

def factorial(n):
    if n < 0:
        raise ValueError("Cannot calculate the factorial of a negative number.")
    return np.math.factorial(n)

def average(numbers):
    """Returns the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list.")
    return sum(numbers) / len(numbers)


# Apply the decorator to mathematical functions
add = log_operation(add)
subtract = log_operation(subtract)
multiply = log_operation(multiply)
divide = log_operation(divide)
power = log_operation(power)
square_root = log_operation(square_root)
factorial = log_operation(factorial)
average = log_operation(average)

def main():
    
    while True:
        print("\nSelect operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power")
        print("6. Square Root")
        print("7. Factorial")
        print("8. Average")
        print("9. View History")
        print("10. Exit")

        choice = input("Enter choice (1-10): ")

        if choice == '10':
            print("Exiting the program. Goodbye!")
            break

        try:
            if choice in ['1', '2', '3', '4', '5']:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    result = add(num1, num2)
                    operation = f"{num1} + {num2} = {result}"
                elif choice == '2':
                    result = subtract(num1, num2)
                    operation = f"{num1} - {num2} = {result}"
                elif choice == '3':
                    result = multiply(num1, num2)
                    operation = f"{num1} * {num2} = {result}"
                elif choice == '4':
                    result = divide(num1, num2)
                    operation = f"{num1} / {num2} = {result}"
                elif choice == '5':
                    result = power(num1, num2)
                    operation = f"{num1} ^ {num2} = {result}"

            elif choice == '6':
                num = float(input("Enter a number: "))
                result = square_root(num)
                operation = f"√{num} = {result}"

            elif choice == '7':
                num = int(input("Enter a number: "))
                result = factorial(num)
                operation = f"{num}! = {result}"

            elif choice == '8':
                numbers = list(map(float, input("Enter numbers separated by spaces: ").split()))
                result = np.mean(numbers)
                operation = f"Average of {numbers} = {result}"

            elif choice == '9':
                print("\nCalculation History:")
                for entry in history:
                    print(entry)
                continue

            else:
                print("Invalid input. Please try again.")
                continue

            print(f"The result is: {result}")
            history.append(operation)

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
