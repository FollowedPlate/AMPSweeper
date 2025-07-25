#python -m flask run
import random

from flask import Flask, jsonify, request, render_template
import os, sys

fpath = os.path.join(os.path.dirname(__file__), 'helpers')
sys.path.append(fpath)
from helpers import Game

my_game = Game.Game()

app = Flask(__name__, static_url_path='', static_folder='static')

# http://127.0.0.1:5000
@app.route('/')
def login():
    # index.html is dynamically generated i.e. the footer component is added
    return render_template('index.html', title=my_game.title) 

# http://127.0.0.1:5000/board                                                      
@app.route('/board')
def board():
    board_str = str(my_game)
    return board_str #everything you return is a str

# http://127.0.0.1:5000/board_json     
@app.route('/board_json')
def board_json():
    return jsonify(my_game.board) # sets the mimetype to json-formatted str
                          # useful for sending data separate from HTML

# http://127.0.0.1:5000/game?username=Dave&board_size=4     
@app.route('/game')
def game():
    # Accessing Query string variables in URL
    username = request.args.get('username')
    size = int(request.args.get('board_size')) #all data arrives as a str
    board_seed = request.args.get('board_seed')
    if not board_seed:
        board_seed = str(random.randint(1,10000))
    my_game.create_board(size, board_seed)

    template_info={#useful to group template info into one dictionary
        "username": username,
        "title": my_game.title,
        "board_str": my_game.html(),
        "symbols":my_game.symbols,
        "board_size": size,
        "board_seed": board_seed,
    }
    return render_template('game.html', info=template_info)

# http://127.0.0.1:5000/solve/<id>
@app.route('/solve/<id>', methods=['POST'])
def process_results(id):
    # data = request.json
    # # print("Received JSON:", data)
    # result = my_game.process_click(data)
    # return result
    return {"result": ""}

@app.route('/click', methods=['POST'])
def do_click():
    data = request.json
    # print("Received JSON:", data)
    result = my_game.process_click(data)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)