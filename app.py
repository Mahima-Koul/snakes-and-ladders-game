from flask import Flask, jsonify, request,render_template
import random   #for the dice roll

app = Flask(__name__)

# Global game state(using dictionary data structure)
game_state = {       
    "player1": 1,
    "player2": 1,
    "current_turn": "player1"
}

snakes = {
    17: 12, 52: 29, 57: 40, 62: 22, 88: 18,
    95: 51, 97:79
}
ladders = {
    3: 21, 8: 30, 28: 84, 58: 77,
    75: 88, 80: 100, 90:91
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
    game_state["player1"] = 1
    game_state["player2"] = 1
    game_state["current_turn"] = "player1"
    return jsonify({"message": "Game reset."})

if __name__ == '__main__':
    app.run(debug=True)
