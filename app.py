
from flask import Flask, render_template, url_for, request, redirect


app = Flask(__name__)

proglen = ['Python','JavaScript','PHP','Ruby']
questions = ['Is it compiled','Does it run on a VM']

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/guess/<int:id>')
def guess(id):
	return render_template('guess.html', guess=proglen[id])

@app.route('/question/<int:id>', methods=['GET','POST'])
def question(id):
	if request.method == 'POST':
		if request.form['answer'] == 'yes':
			return redirect(url_for('question', id=id+1))
		else:
			return redirect(url_for('question', id=id))
	return render_template('question.html', question=questions[id])


if __name__ == '__main__':

	app.run(host='0.0.0.0', port=5000,debug=True)
