from flask import Flask, request
from game import Mine
import json

app = Flask(__name__)

mine = Mine(size=9, num_mines=10)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/new_game')
def new_game():
    global mine
    mine = Mine(size=9, num_mines=10)
    json_mine = mine.to_json()
    print(json_mine)
    return json_mine

@app.route('/update_game', methods=['POST'])
def update_game():
    if not request.json:
        abort(400)

    y = request.json['x_guess']
    x = request.json['y_guess']

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