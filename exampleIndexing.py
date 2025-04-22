# exampleIndexing.py
import numpy as np

# Create a 3x3 matrix
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

def demonstrate_indexing_operations():  
        # Accessing elements using indexing
        print("Element at (0, 0):", matrix[0, 0])  # First row, first column
        print("Element at (1, 2):", matrix[1, 2])  # Second row, third column

        # Slicing rows and columns
        print("First row:", matrix[0, :])  # All columns of the first row
        print("Second column:", matrix[:, 1])  # All rows of the second column

        # Modify an element
        matrix[2, 2] = 99
        print("Modified matrix:")
        print(matrix)

        # Extract a submatrix
        submatrix = matrix[0:2, 1:3]  # Rows 0-1, Columns 1-2
        print("Submatrix:")
        print(submatrix)

if __name__ == "__main__":
    demonstrate_indexing_operations()