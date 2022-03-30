const { add, addWithOperationCounting } = require('./strassenMultiplication')
const fs = require('fs');

const [inputFile1, inputFile2, outputFile, dummyOperation, counting] = process.argv.slice(2, 7);

const matrixA = JSON.parse(fs.readFileSync(inputFile1));
const matrixB = JSON.parse(fs.readFileSync(inputFile2));

let result;
if(dummyOperation == 'True') {
    result = matrixA
} else if(counting == 'True') {
    result = addWithOperationCounting(matrixA, matrixB)
} else {
    result = add(matrixA, matrixB)
}

fs.writeFileSync(outputFile, JSON.stringify(result));