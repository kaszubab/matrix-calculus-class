def basicMultiplication(matrixA, matrixB):
  sumMatrix = []
  for i in range(len(matrixA)):
    sumMatrix.append([])
    for j in range(len(matrixB)):
      sumMatrix[i].append(sum([matrixA[i][k] * matrixB[k][j] for k in range(len(matrixB))]))
  return sumMatrix

def basicMultiplicationWithOperationCounting(matrixA, matrixB):
  fpOperations = 0
  sumMatrix = []
  for i in range(len(matrixA)):
    sumMatrix.append([])
    for j in range(len(matrixB)):
      if len(matrixB) == 1:
        sumMatrix[i].append(matrixA[i][0] * matrixB[0][j])
        fpOperations += 1
      else:
        computedCell = [matrixA[i][k] * matrixB[k][j] for k in range(len(matrixB))] 
        sumMatrix[i].append(sum(computedCell))
        fpOperations += len(computedCell) * 2
  return sumMatrix, fpOperations

def matrixPairwiseOperation(op):
  def computeResult(matrixA, matrixB):
    resultMatrix = []
    for i in range(len(matrixA)):
      resultMatrix.append([op(matrixA[i][j], matrixB[i][j]) for j in range(len(matrixA))])
    return resultMatrix
  return computeResult

def matrixPairwiseOperationWithOperationCounting(op):
  def computeResult(matrixA, matrixB):
    fpOperations = 0
    resultMatrix = []
    for i in range(len(matrixA)):
      resultMatrix.append([op(matrixA[i][j], matrixB[i][j]) for j in range(len(matrixA))])
      fpOperations += len(resultMatrix[i])
    return [resultMatrix, fpOperations]
  return computeResult

add = matrixPairwiseOperation(lambda x, y: x + y)
sub = matrixPairwiseOperation(lambda x, y: x - y)

addWithOperationCounting = matrixPairwiseOperationWithOperationCounting(lambda x, y: x + y)
subWithOperationCounting = matrixPairwiseOperationWithOperationCounting(lambda x, y: x - y)

def splitMatrixIntoFourParts(matrix):
  length = len(matrix)
  firstHalf = matrix[0: length // 2]
  secondHalf = matrix[length // 2:]
  firstQuarter = [list(row)[0: length // 2] for row in firstHalf]
  secondQuarter = [list(row)[length // 2:] for row in firstHalf]
  thirdQuarter = [list(row)[0: length // 2] for row in secondHalf]
  fourthQuarter = [list(row)[length // 2:] for row in secondHalf]
  return firstQuarter, secondQuarter, thirdQuarter, fourthQuarter


def joinMatrixFromFourParts(parts):
  first, second, third, fourth = parts
  firstHalf = [first[idx] + second[idx] for idx in range(len(first))]
  secondHalf = [third[idx] + fourth[idx] for idx in range(len(third))]
  return firstHalf + secondHalf

def strassenAlgorithm(matrixA, matrixB, multiplyMatrix=None): # we pass multiplyMatrix to enable algorithm switch during execution
  mul = multiplyMatrix or strassenAlgorithm
  length = len(matrixA)

  if length == 1: return [[matrixA[0][0] * matrixB[0][0]]]
  A11, A12, A21, A22 = splitMatrixIntoFourParts(matrixA)
  B11, B12, B21, B22 = splitMatrixIntoFourParts(matrixB)

  P1 = mul(add(A11, A22), add(B11, B22))
  P2 = mul(add(A21, A22), B11)
  P3 = mul(A11, sub(B12, B22))
  P4 = mul(A22, sub(B21, B11))
  P5 = mul(add(A11, A12), B22)
  P6 = mul(sub(A21, A11), add(B11, B12))
  P7 = mul(sub(A12, A22), add(B21, B22))

  C11 = add(sub(add(P1, P4), P5), P7)
  C12 = add(P3, P5)
  C21 = add(P2, P4)
  C22 = add(add(sub(P1, P2), P3), P6)

  return joinMatrixFromFourParts((C11, C12, C21, C22))

def strassenAlgorithmWithOperationCounting(matrixA, matrixB, multiplyMatrixWithCounting=None): # we pass multiplyMatrix to enable algorithm switch during execution
  mulWithCounting = multiplyMatrixWithCounting or strassenAlgorithmWithOperationCounting
  length = len(matrixA)
  if length == 1: return ([[matrixA[0][0] * matrixB[0][0]]], 1)
  A11, A12, A21, A22 = splitMatrixIntoFourParts(matrixA)
  B11, B12, B21, B22 = splitMatrixIntoFourParts(matrixB)

  fpOperations = 0
  def wrappedOperation(operation):
    def computeResult(x, y):
      result = operation(x, y)
      nonlocal fpOperations
      fpOperations += result[1]
      return result[0]
    return computeResult

  add = wrappedOperation(addWithOperationCounting)
  sub = wrappedOperation(subWithOperationCounting)
  mul = wrappedOperation(mulWithCounting)

  P1 = mul(add(A11, A22), add(B11, B22))
  P2 = mul(add(A21, A22), B11)
  P3 = mul(A11, sub(B12, B22))
  P4 = mul(A22, sub(B21, B11))
  P5 = mul(add(A11, A12), B22)
  P6 = mul(sub(A21, A11), add(B11, B12))
  P7 = mul(sub(A12, A22), add(B21, B22))

  C11 = add(sub(add(P1, P4), P5), P7)
  C12 = add(P3, P5)
  C21 = add(P2, P4)
  C22 = add(add(sub(P1, P2), P3), P6)

  return (joinMatrixFromFourParts((C11, C12, C21, C22)), fpOperations)


def hybridMultiplication(matrixA, matrixB, thresholdSize):
  def recurrenceCounting(matrixA, matrixB):
    if len(matrixA) > thresholdSize:
      return strassenAlgorithm(matrixA, matrixB, recurrenceCounting)
    else:
      return basicMultiplication(matrixA, matrixB)
  return recurrenceCounting(matrixA, matrixB)

def hybridMultiplicationWithOperationCounting(matrixA, matrixB, thresholdSize):
  def recurrenceCounting(matrixA, matrixB):
    if len(matrixA) > thresholdSize:
      return strassenAlgorithmWithOperationCounting(matrixA, matrixB, recurrenceCounting)
    else:
      return basicMultiplicationWithOperationCounting(matrixA, matrixB)
  return recurrenceCounting(matrixA, matrixB)
