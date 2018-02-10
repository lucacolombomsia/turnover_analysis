from flask import Flask, render_template, request
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../develop')
from src import preprocess



app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage'

@app.route("/inputs")
def my_form():
    return render_template('my-form.html')

@app.route('/inputs', methods=['POST'])
def my_form_post():
    x = [float(request.form['satisfaction'])]
    x += [float(request.form['evaluation'])]
    x += [float(request.form['projects'])]
    x += [float(request.form['hours'])]
    x += [float(request.form['tenure'])]
    x += [request.form.get('accident')]
    x += [request.form.get('promotion')]
    x += [request.form.get('department')]
    x += [request.form.get('salary')]
    x = preprocess.preprocess(x)
    y = [str(n) for n in x]
    return str(','.join(y))

if __name__ == "__main__":
    app.run(debug=True)
