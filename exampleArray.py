# exampleArray.py

import numpy as np

def create_array():
    # Создание одномерного массива
    arr = np.array([1, 2, 3, 4, 5])
    print("Одномерный массив:", arr)

    # Создание двумерного массива    
    arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
    print("Двумерный массив:\n", arr_2d)

    arr_3d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    print("Трехмерный массив:\n", arr_3d)

if __name__ == "__main__":
    create_array()