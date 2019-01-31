from flask import Flask, render_template, request, session, escape, redirect, url_for
import data_manager
import hash
from datetime import datetime,date

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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

    return render_template("display_a_question.html", question=question,
                           answer_table=answer_table, view_number=add_view_count,
                           comment_to_question=comment_to_question,
                           comment_to_answer=comments,
                           question_id=question_id)


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
        user_name = session['username']

        user_id = data_manager.get_user_id(user_name)

        question_id_dict = data_manager.add_question(submission_time, view_nr, vote_nr, title, message, image,
                                                     user_id['user_id'])
        question_id = question_id_dict[0]['id']

        return redirect(url_for('display_question', question_id=question_id))

    return render_template("add_a_question.html", submission_time='default', view_nr='0', vote_nr='5')


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_a_comment_to_question(question_id):
    if request.method == 'POST':
        message_data = request.form.to_dict()
        message = message_data['message']

        user_name = session['username']

        user_id = data_manager.get_user_id(user_name)
        data_manager.add_comment_to_question(question_id, message, user_id['user_id'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_a_comment_to_question.html', question_id=question_id)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_an_answer(question_id):
    if request.method == 'POST':
        answer_data = request.form.to_dict()
        message = answer_data['message']
        submission_data = datetime.now().isoformat(timespec='seconds')
        username = session['username']
        user_id = data_manager.get_user_id(username)
        data_manager.add_answer(question_id, message, submission_data, user_id['user_id'])
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_answer.html', question_id=question_id,
                           submission_time='default', vote_nr='5')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_a_comment_to_answer(answer_id):
    question_id = request.args.get('question_id')
    if request.method == 'POST':
        message_data = request.form.to_dict()
        message = message_data['message']
        answer_id = request.form.get('answer_id')
        user_name = session['username']

        user_id = data_manager.get_user_id(user_name)
        data_manager.add_comment_to_answer(answer_id, message, user_id['user_id'])
        return redirect(url_for('display_question', question_id=question_id))

    return render_template('add_a_comment_to_answer.html', answer_id=answer_id, question_id=question_id)


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == "GET":
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


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if request.method == "GET":
        question_id_in_list = data_manager.find_question_id_from_answers(answer_id)
        make_dict_from_list = question_id_in_list[0]
        question_id = make_dict_from_list['question_id']
        data_manager.delete_answer(answer_id)
        return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if request.method == "GET":
        answers_id = data_manager.find_answer_id_by_question_id(question_id)
        for id in answers_id:
            data_manager.delete_answer(id['id'])
        data_manager.delete_question(question_id)
        return redirect("/list")


@app.route("/sort", methods=['GET', 'POST'])
def list_sorted_question():
    title = request.form.to_dict()['title']
    type = request.form.to_dict()['type']
    if type == "DESC":
        sorted = data_manager.sorted_title_desc(title)
    else:
        sorted = data_manager.sorted_title_asc(title)

    return render_template("list_questions.html", list_of_question=sorted)


@app.route("/search", methods=['GET', 'POST'])
def search_stuff():
    if request.method == 'POST':
        search = request.form.to_dict()
        data = search['search']
        search_message = data_manager.search_question(data)

        return render_template("search_results.html", search_message=search_message)


@app.route('/delete_comment/<comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
    if request.method == 'POST':
        data = request.form.to_dict()

        ids = request.form.to_dict()
        comment_id = ids['comment_id']
        question_id = data['question_id']

        data_manager.delete_comment(comment_id)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.method == 'POST':
            user_info = request.form.to_dict()
            username = user_info['username']
            unhashed_pass = user_info['password']
            retrieve_password = data_manager.check_login_data(username)
            actual_password = retrieve_password[0]['password']
            hashed_pass = hash.verify_password(unhashed_pass, actual_password)
            if hashed_pass is True:
                session['username'] = request.form['username']
                return redirect(url_for('list_5_questions'))
            else:
                return redirect(url_for('list_5_questions'))
        else:
            return render_template('list_questions.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('list_5_questions'))


@app.route('/registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = hash.hash_password(request.form['password'])
        registry_date = date.today()
        data_manager.add_user(username, password, registry_date)

        return redirect(url_for('list_5_questions'))

    return render_template('register.html')

@app.route("/list_users")
def list_users():
    users = data_manager.list_all_user()

    return render_template('list_users.html', users=users)

@app.route("/user_info/<int:id>")
def list_user_info(id):

    id = data_manager.get_user_all_question(id)

    answers = data_manager.get_user_all_answers(id)
    comments_for_answers = data_manager.get_user_all_comments_answer(id)
    comments_for_questions = data_manager.get_user_all_comments_question(id)
    username = data_manager.get_user_by_id(id)
    print(comments_for_answers,'asus 15:00')
    return render_template('user_info.html', questions=questions, answers=answers, comments_for_answers=comments_for_answers, comments_for_questions=comments_for_questions, username=username)

@app.route('/accept', methods=['GET', 'POST'])
def accept():
    if request.method == 'POST':

        ids = request.form.to_dict()

        question_id = ids['question_id']

        user_id = ids['user_id']


        data_manager.false_all_accept()

        data_manager.true_accept(user_id)

        return redirect(url_for('display_question', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
