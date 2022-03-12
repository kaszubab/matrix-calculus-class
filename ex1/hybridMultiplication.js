const { strassenAlgorithm, strassenAlgorithmWithOperationCounting } = require('./strassenMultiplication')
const { basicMultiplication, basicMultiplicationWithOperationCounting } = require('./basicMultiplication')

const hybridMultiplication = (matrixA, matrixB, thresholdSize) => {
  const recurrenceCounting = (matrixA, matrixB) => {
    if (matrixA.length > thresholdSize) {
      return strassenAlgorithm(matrixA, matrixB, recurrenceCounting)
    } else {
      return basicMultiplication(matrixA, matrixB)
    }

  }
  return recurrenceCounting(matrixA, matrixB)
}

const hybridMultiplicationWithOperationCounting = (matrixA, matrixB, thresholdSize) => {
  const recurrenceCounting = (matrixA, matrixB) => {
    if (matrixA.length > thresholdSize) {
      return strassenAlgorithmWithOperationCounting(matrixA, matrixB, recurrenceCounting)
    } else {
      return basicMultiplicationWithOperationCounting(matrixA, matrixB)
    }
  }
  return recurrenceCounting(matrixA, matrixB)
}

const generateMatrix = (size) => {
  const matrix = []
  for (let i = 0; i < size; i++) {
    matrix.push([])
    for (let j = 0; j < size; j++) {
      matrix[i].push(Math.random())
    }
  }
  return matrix
}

const test1 = generateMatrix(256)
const test2 = generateMatrix(256)

// console.log(test1)
// console.log(test2)

// console.log(hybridMultiplication(test1, test2, 8))
// console.log(strassenAlgorithmWithOperationCounting(test1, test2)[1])
console.log(hybridMultiplication(test1, test2, 32))
// console.log(basicMultiplicationWithOperationCounting(test1, test2)[1])
