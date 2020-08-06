from flask import Flask, request
from game import Mine
import json

# Build Flask app 
app = Flask(__name__)
mine = Mine(size=9, num_mines=10)

# Load HTML when navigating to web app
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Start new game by creating new Mine instance
@app.route('/new_game')
def new_game():
    global mine
    mine = Mine(size=9, num_mines=10)
    json_mine = mine.to_json()
    return json_mine

# Update game and send unclicked tiles to client
@app.route('/update_game', methods=['POST'])
def update_game():
    if not request.json:
        abort(400)

    y = request.json['x_guess']
    x = request.json['y_guess']

    # mine.x_guess and mine.y_guess are None when
    # game has just started and mines need to be added to board
    if mine.x_guess is None and mine.y_guess is None:
        mine.board, _ = mine.create_mines(x, y)
        mine.print_solution()
    mine.x_guess = x
    mine.y_guess = y

    mine.update(mine.x_guess, mine.y_guess)
    json_mine = mine.to_json()
    if mine.has_won():
        json_mine["message"] = "won"
    if mine.has_lost():
        json_mine["message"] = "lost"
    return json_mine

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)