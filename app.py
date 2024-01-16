from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

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
    return render_template('index_socketio.html', board=initial_board, current_player=current_player)

@app.route('/reset_board', methods=['GET'])
def reset_board():
    global initial_board, current_player
    initial_board = ["", "", "", "", "", "", "", "", ""]
    current_player = 'X'
    socketio.emit('reset', {'board': initial_board, 'current_player': current_player}, broadcast=True)
    return jsonify({'status': 'success', 'board': initial_board, 'current_player': current_player})

@socketio.on('make_move')
def handle_make_move(data):
    position = int(data['position'])
    global current_player
    if initial_board[position] == "":
        initial_board[position] = current_player
        winner = check_winner()
        current_player = 'O' if current_player == 'X' else 'X'
        socketio.emit('update_board', {'board': initial_board, 'current_player': current_player}, broadcast=True)
        if winner:
            socketio.emit('game_over', {'status': 'win', 'winner': winner})
        elif '' not in initial_board:
            socketio.emit('game_over', {'status': 'draw'})
    else:
        socketio.emit('error', {'status': 'error', 'message': 'Invalid move'})

def check_winner():
    for combination in winning_combinations:
        if initial_board[combination[0]] == initial_board[combination[1]] == initial_board[combination[2]] != "":
            return initial_board[combination[0]]
    return None


if __name__ == '__main__':
    socketio.run(app, debug=True, port = 80, host = "0.0.0.0", allow_unsafe_werkzeug=True)
