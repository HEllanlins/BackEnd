from flask import Flask

app = Flask(__name__)

def hello(): 
    return 'hello world'

if __name__ == '__main__':
    app.run(debug = True)