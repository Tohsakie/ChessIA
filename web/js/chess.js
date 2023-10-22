var config = {
    draggable: true,
    dropOffBoard: 'snapback', 
    position: 'start',
    onDrop: onDrop,
}

var board = Chessboard('board1', config);
document.getElementById('fen').value = board.fen();

document.getElementById('fen').onchange = function() {
    board.position(this.value)
}

document.getElementById('reset').onclick = function() {
    board.start()
    document.getElementById('fen').value = board.fen();
}

document.getElementById('predict').onclick = predict

function onDrop () {
    document.getElementById('fen').value = board.fen();
    predict();
  }

// Appel de l'API
function predict() {
    const apiUrl = 'http://localhost:8000/predict/'; 
    const myFen = document.getElementById('fen').value + ' b KQkq - 0 1';

    const data = new URLSearchParams();
    data.append('FEN', myFen); 

    fetch(apiUrl, {
    method: 'POST',
    body: data,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); 
        myMove = data.message;
        const transformedNotation = myMove.slice(0, 2) + "-" + myMove.slice(2);
        console.log(transformedNotation);
        board.move(transformedNotation);
        document.getElementById('fen').value = board.fen();
    })
    .catch(error => {
        console.error(error);
    });
}