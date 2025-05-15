#here it can be the code of Frontend of the Project.
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'],['POST'])
def home():
    return "Protected App: Home Page"

@app.route('/login', methods=['POST'])
def login():
    return "Login endpoint reached"

if __name__ == '__main__':
    app.run(port=5000)
