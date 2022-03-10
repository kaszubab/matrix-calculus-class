from random import randint

# MATRIX_A_ROWS = 3
# MATRIX_A_COLS = 3
# MATRIX_B_ROWS = 3
# MATRIX_B_COLS = 3

MATRIX_A_ROWS = int(input("Wprowadź liczbę więrszy macierzy A: "))
MATRIX_A_COLS = int(input("Wprowadź liczbę kolumn macierzy A: "))
MATRIX_B_ROWS = int(input("Wprowadź liczbę więrszy macierzy B: "))
MATRIX_B_COLS = int(input("Wprowadź liczbę kolumn macierzy B: "))

def createMatrix(rows, cols):
    matrix = []
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(randint(0, 10))
    return matrix


def canMultiply():
    if (MATRIX_A_COLS != MATRIX_B_ROWS):
        print("Błędne rozmiary macierzy")
        return False
    return True


def basicMultiplication(matrixA, matrixB):
    matrix = []
    for i in range(MATRIX_A_ROWS):
        matrix.append([])
        for j in range(MATRIX_B_COLS):
            sum = 0
            for k in range(MATRIX_B_ROWS):
                #print(matrixA[i][k]);
                #print(matrixB[k][j]);
                sum += matrixA[i][k] * matrixB[k][j]
            matrix[i].append(sum)
    return matrix

def printMatrix(matrix):
    for row in matrix:
        print(row)

def StressenAlgorithm():
    print("Stressen")


def main():
    if (MATRIX_A_ROWS < 1 or MATRIX_A_COLS < 1 or MATRIX_B_ROWS < 1 or MATRIX_B_COLS < 1):
        return print("Liczba wierszy/kolumn musi być liczbą całkowitą większa od 0")

    matrixA = createMatrix(MATRIX_A_ROWS, MATRIX_A_COLS)
    matrixB = createMatrix(MATRIX_B_ROWS, MATRIX_B_COLS)

    print("Macierz A:")
    printMatrix(matrixA)
    print("Macierz B:")
    printMatrix(matrixA)

    if (canMultiply()):
        if (MATRIX_A_ROWS > 2 and MATRIX_A_COLS > 2):
            print("wynik mnożenia: ")
            printMatrix(basicMultiplication(matrixA,matrixB))
        else:
            StressenAlgorithm()

main()

"""
TODO
mnożenie liczba x macierz
mnożenie metodą Stressena
"""
