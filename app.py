
from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import Form
from wtforms.fields import RadioField, SubmitField, StringField
from guess import Guess
from wtforms.validators import Required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

game = Guess('Python')

'''old_guess (str): The existing guess that is being expanded.
new_guess (str): The new guess added to the game.
question (str): A question to separate old_guess from new_guess.
answer_for_new (bool): The answer to the question for new_guess.'''

game.expand('Python','C++','Is interperded?',False)
game.expand('C++','Java','Does it run on a VM?',True)


class YesNoQuestionForm(Form):
	answer = RadioField('Your answer', choices=[('yes','Yes'), ('no', 'No')])
	submit = SubmitField('Submit')

class LearnForm(Form):
    language = StringField('What language did you pick?',
                           validators=[Required()])
    question = StringField('What is a question that differentiates your '
                           'language from mine?', validators=[Required()])
    answer = RadioField('What is the answer for your language?',
                        choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Submit')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/question/<int:id>', methods=['GET','POST'])
def question(id):
	question = game.get_question(id)
	if question is None:
		return redirect(url_for('guess', id=id))
	form = YesNoQuestionForm()
	if form.validate_on_submit():
		new_id = game.answer_question(form.answer.data == 'yes', id)
		return redirect(url_for('question', id=new_id))
	return render_template('question.html',question=question,form=form)


@app.route('/guess/<int:id>', methods=['GET', 'POST'])
def guess(id):
	form = YesNoQuestionForm()
	if form.validate_on_submit():
		if form.answer.data == 'yes':
			return redirect(url_for('index'))
    	return redirect(url_for('learn', id=id))
	return render_template('guess.html', guess=game.get_guess(id), form=form)

@app.route('/learn/<int:id>', methods=['GET', 'POST'])
def learn(id):
	guess = game.get_guess(id)
	form = LearnForm()
	if form.validate_on_submit():
	        game.expand(guess, form.language.data, form.question.data,
                    form.answer.data == 'yes')
        return redirect(url_for('index'))
	return render_template('learn.html', guess=guess, form=form)

if __name__ == '__main__':

	app.run(host='0.0.0.0', port=5000,debug=True)
