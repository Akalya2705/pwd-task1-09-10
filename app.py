from flask import Flask, render_template, request, redirect, url_for, session, g
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
DATABASE = 'D:\quiz_assignment\quiz.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Load questions from JSON file
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

questions = load_questions()

@app.route('/')
def index():
    return render_template('i.html')

@app.route('/start_quiz')
def start_quiz():
    session['score'] = 0
    session['question_num'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    question_num = session.get('question_num', 0)
    
    # Redirect to result page if quiz is complete
    if question_num >= len(questions):
        return redirect(url_for('result'))
    
    question = questions[question_num]
    
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == question["answer"]:
            session['score'] += 1
        session['question_num'] += 1
        return redirect(url_for('quiz'))
    
    return render_template('q.html', question=question, question_num=question_num + 1, total_questions=len(questions))

@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(questions)

    # Save score to database
    db = get_db()
    db.execute("INSERT INTO scores (score, total_questions) VALUES (?, ?)", (score, total_questions))
    db.commit()

    return render_template('r.html', score=score, total_questions=total_questions)

@app.route('/scores')
def scores():
    db = get_db()
    cursor = db.execute("SELECT id, score, total_questions FROM scores")
    scores = cursor.fetchall()
    return render_template('s.html', scores=scores)

if __name__ == '__main__':
    # Set up database table for scores
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS scores
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       score INTEGER,
                       total_questions INTEGER)''')
        db.commit()
    app.run(debug=True)
