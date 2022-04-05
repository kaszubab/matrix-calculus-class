from multiplication import splitMatrixIntoFourParts, joinMatrixFromFourParts, add, sub, addWithOperationCounting, subWithOperationCounting, hybridMultiplication, hybridMultiplicationWithOperationCounting
from inversion import invertMatrixBlock, invertMatrixBlockWithOperationCounting
from functools import reduce

def generateEmptyMatrix(matrix):
  return [[0.0 for j in range(len(matrix))] for i in range(len(matrix))]

def getEigenValues(U):
  return [U[i][i] for i in range(len(U))]

def calculateDeterminant(U):
  eigenValues = getEigenValues(U)
  return reduce(lambda x,y: x * y, eigenValues)

def doolittleLUFactorizationWithOperationCounting(matrix):
  fpOperations = 0
  L = [[0.0 for x in range(len(matrix))] for x in range(len(matrix))]
  U = []

  for i in range(len(matrix)):
    L[i][i] = 1.0

  for i in range(len(matrix)):
    U.append([0.0 if j < i else (matrix[i][j] - sum([L[i][k] * U[k][j] for k in range(0, i)])) for j in range(len(matrix))])
    fpOperations += sum([2 * i * (len(matrix) - i)])
    columnScaling = 1/U[i][i]
    for j in range(i + 1, len(matrix)):
      L[j][i] = columnScaling * (matrix[j][i] - sum([L[j][k] * U[k][i] for k in range(0, i)]))
      fpOperations += 1 + 2 * i
  
  return L, U, fpOperations

def doolittleLUFactorization(matrix):
  L = [[0.0 for x in range(len(matrix))] for x in range(len(matrix))]
  U = []

  for i in range(len(matrix)):
    L[i][i] = 1.0

  for i in range(len(matrix)):
    U.append([0.0 if j < i else (matrix[i][j] - sum([L[i][k] * U[k][j] for k in range(0, i)])) for j in range(len(matrix))])
    columnScaling = 1/U[i][i]
    for j in range(i + 1, len(matrix)):
      L[j][i] = columnScaling * (matrix[j][i] - sum([L[j][k] * U[k][i] for k in range(0, i)]))
  
  return L, U

def LUBlockFactorization(matrix):
  def multiply(matrixA, matrixB):
    return hybridMultiplication(matrixA, matrixB, 2 ** 5)
  def LUFactorizationRecur(matrix):
    if len(matrix) <= 2:
      L, U = doolittleLUFactorization(matrix) 
      return L, U

    A11, A12, A21, A22 = splitMatrixIntoFourParts(matrix)

    L11, U11 = LUFactorizationRecur(A11)
    invertedU11 = invertMatrixBlock(U11)
    L21 = multiply(A21, invertedU11)
    invertedL11 = invertMatrixBlock(L11)
    U12 = multiply(invertedL11, A12)
    S = sub(A22, multiply(multiply(A21, invertedU11), multiply(invertedL11, A12)))
    L22 = S
    LS, US = LUFactorizationRecur(S)
    U22 = US
    L22 = LS

    L12 = generateEmptyMatrix(L22)
    U21 = generateEmptyMatrix(U22)

    return joinMatrixFromFourParts((L11, L12, L21, L22)), joinMatrixFromFourParts((U11, U12, U21, U22))
  return LUFactorizationRecur(matrix)


def LUBlockFactorizationWithOperationCounting(matrix):
  fpOperations = 0

  def multiplyWithCounting(matrixA, matrixB):
    return hybridMultiplicationWithOperationCounting(matrixA, matrixB, 2 ** 3)

  def wrappedOperation(operation):
    def computeResult(*args):
      result = operation(*args)
      nonlocal fpOperations
      fpOperations += result[1]
      return result[0]
    return computeResult

  add = wrappedOperation(addWithOperationCounting)
  sub = wrappedOperation(subWithOperationCounting)
  mul = wrappedOperation(multiplyWithCounting)
  invertMatrixBlock = wrappedOperation(invertMatrixBlockWithOperationCounting)
  
  def LUFactorizationRecur(matrix):
    if len(matrix) <= 2:
      L, U, ops = doolittleLUFactorizationWithOperationCounting(matrix) 
      nonlocal fpOperations
      fpOperations += ops
      return L, U

    A11, A12, A21, A22 = splitMatrixIntoFourParts(matrix)

    L11, U11 = LUFactorizationRecur(A11)
    invertedU11 = invertMatrixBlock(U11)
    L21 = mul(A21, invertedU11)
    invertedL11 = invertMatrixBlock(L11)
    U12 = mul(invertedL11, A12)
    S = sub(A22, mul(mul(A21, invertedU11), mul(invertedL11, A12)))
    L22 = S
    LS, US = LUFactorizationRecur(S)
    U22 = US
    L22 = LS

    L12 = generateEmptyMatrix(L22)
    U21 = generateEmptyMatrix(U22)

    return joinMatrixFromFourParts((L11, L12, L21, L22)), joinMatrixFromFourParts((U11, U12, U21, U22))
  return *LUFactorizationRecur(matrix), fpOperations
