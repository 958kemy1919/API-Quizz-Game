from flask import Flask, render_template
import requests
from random import shuffle

URL_ENDPOINT = "https://the-trivia-api.com/api/questions"
parameters = {
    "limit": 10,
    #"categories": "science,history,geography,sport"
}

response = requests.get(url=URL_ENDPOINT,params=parameters)
data = response.json()

list_of_answers = []
for d in data:
    list = []
    list.append(d['correctAnswer'])
    for x in d['incorrectAnswers']:
        list.append(x)
    shuffle(list)
    list_of_answers.append(list)

class Quizz:

    def __init__(self,id,category,question,answers,correct_answer):
        self.id = id
        self.category = category
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

quiz = []
i = 0
for d in data:
    quiz.append(Quizz(i,d['category'],d['question'],list_of_answers[i],d['correctAnswer']))
    i += 1


app = Flask(__name__)

score = 0
skipped_question = 0
@app.route('/')
def home():
    return render_template("index.html",quiz=quiz)

@app.route('/game/<int:id>/<string:x>')
def play_game(id,x):
    global score, skipped_question
    if id < len(quiz):
        for q in quiz:
            if q.correct_answer == x:
                score += 1
        for q in quiz:
            if q.id == id:
                return render_template("question.html",q=q,score=score,number_of_questions=quiz.index(q))
    else:
        sc = score
        score = 0
        return render_template("end.html",score=sc,number_of_questions=len(quiz))


if __name__ == "__main__":
    app.run(debug=True)