from flask import Flask, jsonify, request,render_template
import random

app = Flask(__name__)

# Global game state (not persistent — resets on server restart)
game_state = {
    "player1": 0,
    "player2": 0,
    "current_turn": "player1"
}

snakes = {
    16: 6, 48: 26, 49: 11, 56: 53, 62: 19,
    64: 60, 87: 24, 93: 73, 95: 75, 98: 78
}
ladders = {
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
    36: 44, 51: 67, 71: 91, 80: 100
}

def move_player(player):
    dice = random.randint(1, 6)
    current_pos = game_state[player]
    next_pos = current_pos + dice

    if next_pos > 100:
        next_pos = current_pos  # Do not move if it exceeds 100
    else:
        if next_pos in snakes:
            next_pos = snakes[next_pos]
        elif next_pos in ladders:
            next_pos = ladders[next_pos]

    game_state[player] = next_pos

    winner = None
    if next_pos == 100:
        winner = player

    # Switch turn
    game_state["current_turn"] = "player2" if player == "player1" else "player1"

    return dice, next_pos, winner

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/roll', methods=['POST'])
def roll():
    player = game_state["current_turn"]
    dice, new_pos, winner = move_player(player)
    return jsonify({
        "player": player,
        "dice": dice,
        "position": new_pos,
        "next_turn": game_state["current_turn"],
        "winner": winner
    })

@app.route('/state', methods=['GET'])
def state():
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    game_state["player1"] = 0
    game_state["player2"] = 0
    game_state["current_turn"] = "player1"
    return jsonify({"message": "Game reset."})

if __name__ == '__main__':
    app.run(debug=True)
