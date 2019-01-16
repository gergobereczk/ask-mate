from flask import Flask, render_template, request, redirect, url_for
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def list_5_questions():
    list_of_question = data_manager.show_5_questions()
    return render_template('list_questions.html', list_of_question=list_of_question)


@app.route("/list")
def list_questions():
    list_of_question = data_manager.show_all_questions()
    return render_template("list_questions_2.html", list_of_question=list_of_question)


@app.route("/question/<int:question_id>", methods=['GET'])
def display_question(question_id):
    comment_ids = []
    comments = []
    question = data_manager.find_question_by_id(question_id)
    answer_table = data_manager.find_answer_by_id(question_id)
    add_view_count = data_manager.add_view_count(question_id)
    comment_to_question = data_manager.find_comment_by_question_id(question_id)
    for answer in answer_table:
        comments.append(data_manager.find_comment_by_answer_id(answer['id']))

    print(comments)
    return render_template("display_a_question.html", question=question,
                           answer_table=answer_table, view_number=add_view_count,
                           comment_to_question=comment_to_question,
                           comment_to_answer=comments)


@app.route("/add_a_question", methods=["GET", "POST"])
def add_a_question():
    if request.method == "POST":
        new_data = request.form.to_dict()
        new_data['submission_time'] = datetime.now().isoformat(timespec='seconds')
        submission_time = new_data['submission_time']
        view_nr = new_data['view_number']
        vote_nr = new_data['vote_number']
        title = new_data['title']
        message = new_data['message']
        image = new_data['image']
        question_id_dict = data_manager.add_question(submission_time, view_nr, vote_nr, title, message, image)
        question_id = question_id_dict[0]['id']

        return redirect(url_for('display_question', question_id=question_id))

    return render_template("add_a_question.html", submission_time='default', view_nr='0', vote_nr='5')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_an_answer(question_id):
    if request.method == 'POST':
        answer_data = request.form.to_dict()
        message = answer_data['message']
        submission_data = datetime.now()
        data_manager.add_answer(question_id, message, submission_data)
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_answer.html', question_id=question_id,
                           submission_time='default', vote_nr='5')


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if request.method == "GET":
        question_id_in_list = data_manager.find_question_id_from_answers(answer_id)
        make_dict_from_list = question_id_in_list[0]
        question_id = make_dict_from_list['question_id']
        data_manager.delete_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id))
        # return ("POST")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if request.method == "GET":
        data_manager.delete_question(question_id)
        return redirect("/list")


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == "GET":
        # data_manager.delete_answers(question_id)
        # data_manager.delete_question(question_id)
        # return redirect("/list")
        full_answer = data_manager.get_answer_by_id(answer_id)

        message = full_answer[0]['message']
        time = datetime.now()
        return render_template('edit_answer.html', message=message, answer_id=answer_id)
    if request.method == "POST":
        answer_data = request.form.to_dict()
        message = answer_data['message']
        question_id_in_list = data_manager.get_question_id(answer_id)
        question_id = question_id_in_list[0]['question_id']
        data_manager.update_answer_by_id(answer_id, message, datetime.now())

        return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_a_comment_to_question(question_id):
    if request.method == 'POST':
        message_data = request.form.to_dict()
        message = message_data['message']
        data_manager.add_comment_to_question(question_id, message)
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_a_comment_to_question.html', question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_a_comment_to_answer(answer_id):
    question_id = request.args.get('question_id')
    if request.method == 'POST':
        message_data = request.form.to_dict()
        message = message_data['message']
        answer_id = request.form.get('answer_id')
        data_manager.add_comment_to_answer(answer_id, message)
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_a_comment_to_answer.html', answer_id=answer_id, question_id=question_id)


@app.route("/search", methods=['GET', 'POST'])
def search_stuff():
    if request.method == 'POST':
        search = request.form.to_dict()
        data = search['search']
        search_message = data_manager.search_question(data)

        return render_template("search_results.html", search_message=search_message)

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
