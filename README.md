# Tic_tac_toe---Fusion
Tech Stack
Backend: Flask (Python) with WebSockets to handle real-time communication between the players.
Frontend: Pure HTML, CSS, and JavaScript, or alternatively, HTTP requests with Postman (for the minimalist approach).
WebSocket Library: flask-socketio to manage the bi-directional communication.
Game Logic: Handled on the server side, checking for win conditions, tracking game states, and sending updates to both clients in real time.

Entities and Flow
Game:
Keeps track of the game board, which is a 3x3 matrix.
Manages the game state (whose turn it is, whether the game is over, and if there’s a winner or a draw).

Player:
Two players identified by their symbols: 'X' and 'O'.
Players alternate turns, and their moves are sent to the server, which validates and broadcasts the new game state.
Move Validation:

The server ensures the move is valid (i.e., the cell is empty, and it’s the correct player's turn).
After a move, the server checks for a win condition or a draw and informs both players of the result.

Basic Flow:
Game Start:
Two clients connect to the server.
The server assigns them 'X' or 'O' and initializes a new game.

Player Move:
A player makes a move by selecting a cell on the game board (or via Postman, sending a request to mark a specific cell).
The move is sent to the server, which updates the game state and broadcasts the updated board to both players.
Checking Win Condition:

After each move, the server checks the game board for three consecutive 'X' or 'O' symbols horizontally, vertically, or diagonally.
If a player wins, or if there’s a draw, the server broadcasts the result.

Game End:
Once a game is over, players are notified, and a new game can be started.

Server Logic (Flask with WebSockets):
Endpoints:
/start: Initializes the game and assigns players.
/move: Handles player moves and validates them.
/status: Returns the current state of the game board.

WebSocket Events:
connect: When a player connects to the game.
move: When a player makes a move, broadcast to the other player.
game_over: Notifies players if someone wins or if the game ends in a draw.

How to Run:
Server Side:
Clone the repo.
Install dependencies: pip install flask flask-socketio.
Run the Flask server: python app.py.

Client Side (UI):
Open index.html in two different browsers (or tabs for testing).
Players make moves by clicking on the game board.
