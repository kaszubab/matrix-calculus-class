import copy
from multiplication import splitMatrixIntoFourParts, joinMatrixFromFourParts, add, sub, addWithOperationCounting, subWithOperationCounting, hybridMultiplication, hybridMultiplicationWithOperationCounting

def createIdentityMatrix(matrix):
    matrixSize = len(matrix)
    matrix = []
    for i in range(matrixSize):
        matrix.append([])
        for j in range(matrixSize):
            if i == j:
                matrix[i].append(1.0)
            else:
                matrix[i].append(0.0)
    return matrix

def invertMatrix(AM, IM):
  newAM = AM.copy()
  for fd in range(len(newAM)):
    fdScaler = 1.0 / newAM[fd][fd]
    for j in range(len(newAM)):
      newAM[fd][j] *= fdScaler
      IM[fd][j] *= fdScaler
    for i in list(range(len(newAM)))[0:fd] + list(range(len(newAM)))[fd+1:]:
      crScaler = newAM[i][fd]
      for j in range(len(AM)):
        newAM[i][j] = newAM[i][j] - crScaler * newAM[fd][j]
        IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
  return IM

def invertMatrixWithOperationCounting(AM, IM):
  operationCount = 0
  newAM = AM.copy()
  for fd in range(len(newAM)):
    fdScaler = 1.0 / newAM[fd][fd]
    for j in range(len(newAM)):
      newAM[fd][j] *= fdScaler
      IM[fd][j] *= fdScaler
      operationCount += 2
    for i in list(range(len(newAM)))[0:fd] + list(range(len(newAM)))[fd+1:]:
      crScaler = newAM[i][fd]
      for j in range(len(AM)):
        newAM[i][j] = newAM[i][j] - crScaler * newAM[fd][j]
        IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
        operationCount += 2          
  return IM, operationCount

def invertSmallMatrix(matrix):
  identityMatrix = createIdentityMatrix(matrix)
  copiedMatrix = copy.deepcopy(matrix)
  return invertMatrix(copiedMatrix, identityMatrix)

def invertSmallMatrixWithCounting(matrix):
  identityMatrix = createIdentityMatrix(matrix)
  copiedMatrix = copy.deepcopy(matrix)
  return invertMatrixWithOperationCounting(copiedMatrix, identityMatrix)

def negateMatrix(matrix):
  if(len(matrix) == 1): 
    return [[-matrix[0][0]]]
  return [[-x for x in row] for row in matrix]

def invertMatrixBlock(matrix):
  def multiply(matrixA, matrixB):
    return hybridMultiplication(matrixA, matrixB, 2 ** 5)
  def invertMatrixBlockRecur(matrix):  
    if len(matrix) <= 2:
      return invertSmallMatrix(matrix)
    resultMatrix = None

    A11, A12, A21, A22 = splitMatrixIntoFourParts(matrix)
    invertedA11 = invertMatrixBlockRecur(A11)
    S22 = add(A22, negateMatrix(multiply(multiply(A21, invertedA11), A12)))
    invertedS22 = invertMatrixBlockRecur(S22)

    tempResult = multiply(multiply(multiply(A12, invertedS22), A21), invertedA11)
    B11 = multiply(invertedA11, add(createIdentityMatrix(tempResult), tempResult))

    B12 = multiply(multiply(negateMatrix(invertedA11), A12), invertedS22)
    B21 = multiply(multiply(negateMatrix(invertedS22), A21), invertedA11)
    B22 = invertedS22
    resultMatrix = joinMatrixFromFourParts((B11, B12, B21, B22))
    return resultMatrix
  return invertMatrixBlockRecur(matrix)

def invertMatrixBlockWithOperationCounting(matrix):
  fpOperations = 0
  def multiplyWithCounting(matrixA, matrixB):
    return hybridMultiplicationWithOperationCounting(matrixA, matrixB, 2 ** 5)

  def wrappedOperation(operation):
    def computeResult(x, y):
      result = operation(x, y)
      nonlocal fpOperations
      fpOperations += result[1]
      return result[0]
    return computeResult

  add = wrappedOperation(addWithOperationCounting)
  sub = wrappedOperation(subWithOperationCounting)
  mul = wrappedOperation(multiplyWithCounting)

  def invertMatrixBlockRecur(matrix):
    nonlocal fpOperations
    if len(matrix) <= 2:
      resultMatrix, operations = invertSmallMatrixWithCounting(matrix)
      fpOperations += operations
      return resultMatrix
    resultMatrix = None

    A11, A12, A21, A22 = splitMatrixIntoFourParts(matrix)
    invertedA11 = invertMatrixBlockRecur(A11)
    S22 = add(A22, negateMatrix(mul(mul(A21, invertedA11), A12)))
    invertedS22 = invertMatrixBlockRecur(S22)

    tempResult = mul(mul(mul(A12, invertedS22), A21), invertedA11)
    B11 = mul(invertedA11, add(createIdentityMatrix(tempResult), tempResult))

    B12 = mul(mul(negateMatrix(invertedA11), A12), invertedS22)
    B21 = mul(mul(negateMatrix(invertedS22), A21), invertedA11)
    B22 = invertedS22
    resultMatrix = joinMatrixFromFourParts((B11, B12, B21, B22))
    return resultMatrix
  return invertMatrixBlockRecur(matrix), fpOperations
