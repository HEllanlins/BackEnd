from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def hello(): 
    user = 'Hellan Lins'
    return render_template('Pagina.html', user = user)

@app.route('/sobre')
def sobre():
    return render_template('Sobre.html')

if __name__ == '__main__':
    app.run(port=8000)
    app.run(debug = True)
    