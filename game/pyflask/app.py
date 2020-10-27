from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/game')
def game():
    return render_template('game.html')