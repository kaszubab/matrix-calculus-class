const { strassenAlgorithm, strassenAlgorithmWithOperationCounting } = require('./strassenMultiplication')
const { basicMultiplication, basicMultiplicationWithOperationCounting } = require('./basicMultiplication')
const fs = require('fs');

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

const [inputFile1, inputFile2, outputFile, dummyOperation, counting, thresholdSize] = process.argv.slice(2, 8);

const matrixA = JSON.parse(fs.readFileSync(inputFile1));
const matrixB = JSON.parse(fs.readFileSync(inputFile2));

let result;
if(dummyOperation == 'True') {
    result = matrixA
} else if(counting == 'True') {
    result = hybridMultiplicationWithOperationCounting(matrixA, matrixB, thresholdSize)
} else {
    result = hybridMultiplication(matrixA, matrixB, thresholdSize)
}

fs.writeFileSync(outputFile, JSON.stringify(result));