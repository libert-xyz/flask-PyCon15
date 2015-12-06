
from flask import Flask


app = Flask(__name__)

proglen = ['Python','JavaScript','PHP','Ruby']

@app.route('/')
def index():
	return '<h1> Hello Flask </h1>'

@app.route('/guess/<int:id>')
def guess(id):
	return('<h1>Guess the Lenguage!</h1>'
		'<p>My guess: {0}</p>').format(proglen[id])
	


if __name__ == '__main__':

	app.run(debug=True)
