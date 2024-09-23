from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

games = {}

# Game state structure for simplicity
def create_game():
    return {
        'board': ['' for _ in range(9)],
        'turn': 'X',
        'players': {},
        'winner': None
    }

# Serve the front-end HTML file
@app.route('/')
def index():
    return render_template('index.html')

# When a player joins, they are assigned 'X' or 'O'
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

    if room not in games:
        games[room] = create_game()

    game = games[room]

    if 'X' not in game['players']:
        game['players']['X'] = request.sid
        emit('assign_symbol', {'symbol': 'X'}, room=request.sid)
    elif 'O' not in game['players']:
        game['players']['O'] = request.sid
        emit('assign_symbol', {'symbol': 'O'}, room=request.sid)

    emit('update_board', {'board': game['board']}, room=room)

# Handle player move
@socketio.on('make_move')
def on_make_move(data):
    room = data['room']
    game = games.get(room)

    if game is None or game['winner']:
        return  # No moves allowed if the game is over

    symbol = data['symbol']
    cell = data['cell']

    if game['board'][cell] == '' and game['turn'] == symbol:
        game['board'][cell] = symbol
        game['turn'] = 'O' if symbol == 'X' else 'X'

        winner = check_winner(game['board'])
        if winner:
            game['winner'] = winner
            emit('game_over', {'winner': winner}, room=room)
        elif '' not in game['board']:  # It's a draw
            emit('game_over', {'winner': 'Draw'}, room=room)

        emit('update_board', {'board': game['board']}, room=room)

def check_winner(board):
    # All winning combinations
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]
    return None

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

