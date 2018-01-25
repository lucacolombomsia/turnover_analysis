from flask import Flask, render_template

app = Flask(__name__)

#here we are routing/mapping using decorator '@' -- use it to map URL to return value
#the response to the URL is what the function returns
# @ signifies a decorator
@app.route('/')
def index():
    return 'This is the homepage'

if __name__ == "__main__":
    app.run(debug=True)
