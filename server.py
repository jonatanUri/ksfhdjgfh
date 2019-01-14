from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/WORK-IN-PROGRESS')
def workinprogress():
    return render_template("workinprogress.html")


@app.route('/')
def home_redirect():
    return redirect('/list')


@app.route('/list')
def mainpage():
    questions_dict = data_manager.read_question()
    questions_dict = data_manager.sorted_by_submission_time(questions_dict)
    return render_template("index.html", questions_dict=questions_dict)


@app.route('/question/<num>')
def question(num):
    questions_dict = data_manager.read_question()
    questions_dict = data_manager.convert_csv_to_human_readable(questions_dict)
    answers_dict = data_manager.read_answer()
    answers_dict = data_manager.convert_csv_to_human_readable(answers_dict)
    for i in questions_dict:
        if i['id'] == num:
            this_question = i
            break
    answers_list = []
    for answer in answers_dict:
        if num == answer["question_id"]:
            answers_list.append(answer)
    return render_template("question.html", num=num, this_question=this_question, answers_list=answers_list)


@app.route('/question/<num>/new-answer')
def new_answer(num):
    return render_template("new-answer.html", num=num)


@app.route('/new-question')
def new_question():
    return render_template("new-question.html")


@app.route('/submit-question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        id_ = data_manager.get_new_question_id()
        submission_time = data_manager.get_current_unix_timestamp()
        title = request.form['title']
        message = request.form['message']
        views = 0
        votes = 0
        question_dict = {
            'id': id_,
            'submission_time': submission_time,
            'view_number': views,
            'vote_number': votes,
            'title': title,
            'message': message
        }
        data_manager.add_question(question_dict)
    return redirect('/question/'+id_)


@app.route('/submit-answer', methods=['GET', 'POST'])
def submit_answer():
    if request.method == 'POST':
        id_ = data_manager.get_new_answer_id()
        submission_time = data_manager.get_current_unix_timestamp()
        votes = 0
        question_id = request.form['question_id']
        message = request.form['message']
        answer_dict = {
            'id': id_,
            'submission_time': submission_time,
            'vote_number': votes,
            'question_id': question_id,
            'message': message
        }
        data_manager.add_answer(answer_dict)
    return redirect('/question/'+question_id)


@app.route('/delete-question/<num>')
def delete_question(num):
    data_manager.delete_question(num)
    return redirect('/list')


@app.route('/answer/<num>/delete', methods=['POST'])
def delete_answer(num):
    data_manager.delete_answer(request.form['answer_id'])
    return redirect('/question/'+num)


if __name__ == "__main__":
    app.run()

