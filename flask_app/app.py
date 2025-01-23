from flask import Flask, render_template, g
from api import api_b


app = Flask(__name__) 
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(api_b) 

@app.route('/')
def index_r():
    return render_template('main.html')

@app.route('/m/<modal>')
def modal_r(modal):
    return render_template(f'{modal}.html')