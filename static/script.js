const board = document.getElementById('board');
const diceResult = document.getElementById('dice-result');
const rollBtn = document.getElementById('roll-btn');

const totalCells = 100;
const cells = [];
let playerPositions = { player1: 0, player2: 0 };

// Build board and map number to cell
for (let row = 9; row >= 0; row--) {
  for (let col = 0; col < 10; col++) {
    const cell = document.createElement('div');
    cell.className = 'cell';

    let number;
    if (row % 2 === 0) {
      number = row * 10 + col + 1;
    } else {
      number = row * 10 + (10 - col);
    }

    cell.textContent = number;
    board.appendChild(cell);
    cells[number - 1] = cell; // position 1 is at index 0
  }
}

function updatePlayers() {
  cells.forEach(cell => {
    cell.querySelectorAll('.player').forEach(el => el.remove());
  });

  if (playerPositions.player1 > 0) {
    const cell = cells[playerPositions.player1 - 1];
    const p1 = document.createElement('div');
    p1.className = 'player player1';
    cell.appendChild(p1);
  }

  if (playerPositions.player2 > 0) {
    const cell = cells[playerPositions.player2 - 1];
    const p2 = document.createElement('div');
    p2.className = 'player player2';
    cell.appendChild(p2);
  }
}

updatePlayers();

// 🎲 Call Flask backend to roll dice
rollBtn.addEventListener('click', () => {
  fetch('/roll', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      const { player, dice, position, next_turn, winner } = data;

      playerPositions[player] = position;
      diceResult.textContent = `${player} rolled a ${dice} → moved to ${position}`;

      updatePlayers();

      if (winner) {
        diceResult.textContent = `🎉 ${winner} wins the game!`;
        rollBtn.disabled = true;
      }
    })
    .catch(err => {
      console.error('Error rolling dice:', err);
    });
});
