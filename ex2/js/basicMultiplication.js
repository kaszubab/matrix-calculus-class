const basicMultiplication = (matrixA, matrixB) => {
    const sumMatrix = [];
    for (let i = 0; i < matrixA.length; i++) {
        sumMatrix.push([]);
        for (let j = 0; j < matrixB.length; j++) {
            let sum = 0;
            for (let k = 0; k < matrixB.length; k++) {
                sum += matrixA[i][k] * matrixB[k][j];
            }
            sumMatrix[i].push(sum);
        }
    }
    return sumMatrix;
};


const basicMultiplicationWithOperationCounting = (matrixA, matrixB) => {
    let fpOperations = 0
    const sumMatrix = [];
    for (let i = 0; i < matrixA.length; i++) {
        sumMatrix.push([]);
        for (let j = 0; j < matrixB.length; j++) {
            let sum = matrixA[i][0] * matrixB[0][j];
            fpOperations += 1;
            for (let k = 1; k < matrixB.length; k++) {
                sum += matrixA[i][k] * matrixB[k][j];
                fpOperations += 2;
            }
            sumMatrix[i].push(sum);
        }
    }
    return [sumMatrix, fpOperations];
};



module.exports = {
    basicMultiplication,
    basicMultiplicationWithOperationCounting
}

