from flask import Flask, render_template, request, redirect, url_for

import data_manager
import time

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    list_of_question = data_manager.show_all_questions()
    return render_template("list_questions.html", list_of_question=list_of_question)


@app.route("/question/<question_id>", methods=['GET'])
def display_question(question_id):
    data_manager.pluss_view_number(question_id)

    question_table = data_manager.find_question_from_id(question_id)
    answer_table = data_manager.find_answer_from_id(question_id)
    the_len=(len(answer_table))
    return render_template("display_a_question.html", question_table=question_table,
                           answer_table=answer_table, the_len=the_len)


@app.route("/add_a_question", methods=["GET", "POST"])
def add_a_question():
    id = data_manager.create_id(data_manager.question_csv)

    if request.method == "POST":
        new_data = request.form.to_dict()
        question_id = new_data['id']
        new_data['submission_time'] = time.time()
        data_manager.write_csv(data_manager.question_csv, data_manager.question_csv, data_manager.HEADER, new_data)
        return redirect(url_for('display_question', question_id=question_id))

    return render_template("add_a_question.html", id=id, submission_time='default', view_nr='0', vote_nr='5')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_an_answer(question_id):
    answer_id = data_manager.create_id(data_manager.answer_csv)

    if request.method == 'POST':
        answer_data = request.form.to_dict()
        answer_data['submission_time'] = time.time()
        data_manager.write_csv(data_manager.answer_csv, data_manager.answer_csv, data_manager.HEADER_ANSWER, answer_data)
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_answer.html', question_id=question_id, answer_id=answer_id,
                           submission_time='default', vote_nr='5')


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if request.method == "GET":
        question_id = data_manager.find_question_id_from_answers(answer_id)
        data_manager.delete_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id))
        #return ("POST")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if request.method == "GET":
        data_manager.delete_answers(question_id)
        data_manager.delete_question(question_id)
        return redirect ("/list")


# @app.route("/question/<question_id>/vote", methods=['GET'])
# def counting_votes(question_id):
#    question_data = data_manager.find_question_from_id(question_id)
#    vote_nr = question_data['vote_number']
#    if vote_nr == None:
#        vote_nr = 0
#    else:
#        vote_nr = int(question_data['vote_number']) + 1
#    question_data['vote_number'] = vote_nr
#    data_manager.write_csv(data_manager.question_csv, data_manager.question_csv, data_manager.HEADER, question_data)
#    return redirect(url_for('display_question', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
