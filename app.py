from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define the initial state of the game board
initial_board = ["", "", "", "", "", "", "", "", ""]

# Define winning combinations
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]              # Diagonals
]

# Variable to keep track of the current player ('X' or 'O')
current_player = 'X'


@app.route('/')
def index():
    return render_template('index.html', board=initial_board, current_player=current_player)


@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player
    position = int(request.form['position'])

    # Check if the selected position is empty
    if initial_board[position] == "":
        initial_board[position] = current_player
        winner = check_winner()
        current_player = 'O' if current_player == 'X' else 'X'  # Switch to the other player for the next turn

        if winner:
            return jsonify({'status': 'win', 'winner': winner, 'board': initial_board, 'current_player': current_player})
        elif '' not in initial_board:
            return jsonify({'status': 'draw', 'board': initial_board, 'current_player': current_player})
        else:
            return jsonify({'status': 'success', 'board': initial_board, 'current_player': current_player})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move'})
def check_winner():
    for combination in winning_combinations:
        if initial_board[combination[0]] == initial_board[combination[1]] == initial_board[combination[2]] != "":
            return initial_board[combination[0]]
    return None

@app.route('/reset_board', methods=['GET'])
def reset_board():
    global initial_board, current_player
    initial_board = ["", "", "", "", "", "", "", "", ""]
    current_player = 'X'
    return jsonify({'status': 'success', 'board': initial_board, 'current_player': current_player})



if __name__ == '__main__':
    app.run(debug=True, port = 80, host = "0.0.0.0")
