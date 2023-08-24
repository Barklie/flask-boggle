from flask import Flask, request, render_template, redirect, jsonify, flash, session

from boggle import Boggle

from IPython.core.debugger import set_trace

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Boggle_KEY'

boggle_game = Boggle()

# board = boggle_game.make_board()

@app.route('/', methods=["GET"])
def home():
 
    board = boggle_game.make_board()

    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nPlays", 0)

    return render_template('base.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/validate-guess', methods=["POST", "GET"])
def validate():

    data = request.get_json()
    word = data['word']
    board = session['board']
    words = boggle_game.words
    result = boggle_game.check_valid_word(board, word)

    if word not in words:
        return jsonify({"result" : "not-a-word"})

    if word in words and result == "ok":

        return jsonify({"result" : result})

    if word in words and result == "not-on-board":

        return jsonify({"result" : result})
    


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""


    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = request.json["nplays"]

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore, nplays=nplays)
    