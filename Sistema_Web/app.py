from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello(): 
    return 'Página Inicial '

@app.route('/sobre')
def sobre():
    return 'Página sobre'

if __name__ == '__main__':
    app.run(port=8000)
    app.run(debug = True)
    