from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage'

#Using HTML Templates
@app.route("/get_inputs")
def get_inputs():
    return render_template("inputs.html")

if __name__ == "__main__":
    app.run(debug=True)
