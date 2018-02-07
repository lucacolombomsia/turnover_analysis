from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage'

@app.route("/inputs")
def my_form():
    return render_template('my-form.html')

@app.route('/inputs', methods=['POST'])
def my_form_post():
    x = [1] + [float(request.form['satisfaction'])]
    x += [float(request.form['evaluation'])]
    x += [float(request.form['projects'])]
    x += [float(request.form['hours'])]
    x += [float(request.form['tenure'])]
    x += [request.form.get('accident')]
    x += [request.form.get('promotion')]
    x += [request.form.get('department')]
    x += [request.form.get('salary')]
    y = [str(n) for n in x]
    return str(','.join(y))

if __name__ == "__main__":
    app.run(debug=True)
