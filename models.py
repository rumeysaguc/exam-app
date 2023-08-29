from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/weather-forecast'
db = SQLAlchemy(app)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    is_correct = db.Column(db.Boolean, default=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))
    date_added = db.Column(db.Date, default=db.func.current_timestamp())

    answers = db.relationship('Answer', secondary='question_answer', backref='questions')


question_answer = db.Table('question_answer',
                           db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
                           db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
                           )
if __name__ == "__main__":
    with app.app_context():
        # Run this file directly to create the database tables.
        print("Creating database tables...")
        db.create_all()
        print("Done!")
