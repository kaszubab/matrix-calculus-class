const { strassenAlgorithm, strassenAlgorithmWithOperationCounting } = require('./strassenMultiplication')

const hybridMultiplication = (matrixA, matrixB, thresholdSize) =>
  matrixA.length > thresholdSize
    ? strassenAlgorithm(matrixA, matrixB, hybridMultiplication)
    : basicMultiplication(matrixA, matrixB)

const hybridMultiplicationWithOperationCounting = (matrixA, matrixB, thresholdSize) =>
  matrixA.length > thresholdSize
    ? strassenAlgorithmWithOperationCounting(matrixA, matrixB, hybridMultiplicationWithOperationCounting)
    : basicMultiplicationWithOperationCounting(matrixA, matrixB)

const generateMatrix = (size) => {
  const matrix = []
  for (let i = 0; i < size; i++) {
    matrix.push([])
    for (let j = 0; j < size; j++) {
      matrix[i].push(1)
    }
  }
  return matrix
}

const test1 = generateMatrix(32)
const test2 = generateMatrix(32)

console.log(test1)
console.log(test2)

console.log(hybridMultiplication(test1, test2, 0))