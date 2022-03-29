const { add, addWithOperationCounting } = require('./strassenMultiplication')
const fs = require('fs');

const [inputFile1, inputFile2, outputFile] = process.argv.slice(2, 5);

const matrixA = JSON.parse(fs.readFileSync(inputFile1));
const matrixB = JSON.parse(fs.readFileSync(inputFile2));

const resultMatrix = add(matrixA, matrixB)

fs.writeFileSync(outputFile, JSON.stringify(resultMatrix));