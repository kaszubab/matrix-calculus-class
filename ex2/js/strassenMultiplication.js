const matrixPairwiseOperation = (op) => (matrixA, matrixB) => {
  const sumMatrix = [];
  for (let i = 0; i < matrixA.length; i++) {
    sumMatrix.push([])
    for (let j = 0; j < matrixA.length; j++) {
      sumMatrix[i].push(op(matrixA[i][j], matrixB[i][j]))
    }
  }
  return sumMatrix
}

const matrixPairwiseOperationWithOperationCounting = (op) => (matrixA, matrixB) => {
  let fpOperations = 0
  const sumMatrix = [];
  for (let i = 0; i < matrixA.length; i++) {
    sumMatrix.push([])
    for (let j = 0; j < matrixA.length; j++) {
      sumMatrix[i].push(op(matrixA[i][j], matrixB[i][j]))
      fpOperations += 1
    }
  }
  return [sumMatrix, fpOperations]
}

const add = matrixPairwiseOperation((x, y) => x + y);
const sub = matrixPairwiseOperation((x, y) => x - y);

const addWithOperationCounting = matrixPairwiseOperationWithOperationCounting((x, y) => x + y)
const subWithOperationCounting = matrixPairwiseOperationWithOperationCounting((x, y) => x - y)

const splitMatrixIntoFourParts = (matrix) => {
  const length = matrix.length
  const firstQuarter = matrix.slice(0, length / 2).map(row => row.slice(0, length / 2))
  const secondQuarter = matrix.slice(0, length / 2).map(row => row.slice(length / 2))
  const thirdQuarter = matrix.slice(length / 2).map(row => row.slice(0, length / 2))
  const fourthQuarter = matrix.slice(length / 2).map(row => row.slice(length / 2))
  return [firstQuarter, secondQuarter, thirdQuarter, fourthQuarter]
}

const joinMatrixFromFourParts = (parts) => {
  const [first, second, third, fourth] = parts
  const firstHalf = first.map((item, index) => item.concat(second[index]))
  const secondHalf = third.map((item, index) => item.concat(fourth[index]))
  return firstHalf.concat(secondHalf)
}

const strassenAlgorithm = (matrixA, matrixB, multiplyMatrix) => { // we pass multiplyMatrix to enable algorithm switch during execution
  const mul = multiplyMatrix || strassenAlgorithm;
  const length = matrixA.length

  if (length === 1) return [[matrixA[0][0] * matrixB[0][0]]]
  const [A11, A12, A21, A22] = splitMatrixIntoFourParts(matrixA)
  const [B11, B12, B21, B22] = splitMatrixIntoFourParts(matrixB)

  const P1 = mul(add(A11, A22), add(B11, B22))
  const P2 = mul(add(A21, A22), B11)
  const P3 = mul(A11, sub(B12, B22))
  const P4 = mul(A22, sub(B21, B11))
  const P5 = mul(add(A11, A12), B22)
  const P6 = mul(sub(A21, A11), add(B11, B12))
  const P7 = mul(sub(A12, A22), add(B21, B22))

  const C11 = add(sub(add(P1, P4), P5), P7)
  const C12 = add(P3, P5)
  const C21 = add(P2, P4)
  const C22 = add(add(sub(P1, P2), P3), P6)

  return joinMatrixFromFourParts([C11, C12, C21, C22])
}

const strassenAlgorithmWithOperationCounting = (matrixA, matrixB, multiplyMatrixWithCounting) => { // we pass multiplyMatrix to enable algorithm switch during execution
  const mulWithCounting = multiplyMatrixWithCounting || strassenAlgorithmWithOperationCounting;
  const length = matrixA.length

  if (length === 1) return [[[matrixA[0][0] * matrixB[0][0]]], 1]
  const [A11, A12, A21, A22] = splitMatrixIntoFourParts(matrixA)
  const [B11, B12, B21, B22] = splitMatrixIntoFourParts(matrixB)

  let fpOperations = 0
  const wrappedOperation = (operation) => (x, y) => {
    const result = operation(x, y)
    fpOperations += result[1]
    return result[0]
  }

  const add = wrappedOperation(addWithOperationCounting)
  const sub = wrappedOperation(subWithOperationCounting)
  const mul = wrappedOperation(mulWithCounting)

  const P1 = mul(add(A11, A22), add(B11, B22))
  const P2 = mul(add(A21, A22), B11)
  const P3 = mul(A11, sub(B12, B22))
  const P4 = mul(A22, sub(B21, B11))
  const P5 = mul(add(A11, A12), B22)
  const P6 = mul(sub(A21, A11), add(B11, B12))
  const P7 = mul(sub(A12, A22), add(B21, B22))

  const C11 = add(sub(add(P1, P4), P5), P7)
  const C12 = add(P3, P5)
  const C21 = add(P2, P4)
  const C22 = add(add(sub(P1, P2), P3), P6)

  return [joinMatrixFromFourParts([C11, C12, C21, C22]), fpOperations]
}

module.exports = {
  strassenAlgorithm,
  strassenAlgorithmWithOperationCounting,
  add,
  sub,
  addWithOperationCounting,
  subWithOperationCounting
}
