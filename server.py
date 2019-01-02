from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)



@app.route("/question/<question_id>")
def display_question(question_id):
    question_table = data_manager.find_question_from_id(question_id)
    answer_table = data_manager.find_answer_from_id(question_id)
    the_len=(len(answer_table))
    print(the_len)
    return render_template("display_a_question.html", question_table=question_table, answer_table=answer_table , the_len=the_len)


@app.route("/add_a_question", methods=["GET", "POST"])
def add_a_question():
    if request.method == "POST":
        new_data = request.form.to_dict()
        id = new_data['id']
        return redirect(url_for('display_question', question_id=question_id))
    else:

        return render_template("add_a_question.html", id='1', submission_time='1436520101', view_number='5', vote_number='5')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
