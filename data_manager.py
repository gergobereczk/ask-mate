import connection
import data_connection
import csv

question_csv = "sample_data/question.csv"

answer_csv = "sample_data/answer.csv"

HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@data_connection.connection_handler
def show_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                   """, )
    questions = cursor.fetchall()
    return questions


@data_connection.connection_handler
def show_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                   """, )
    questions = cursor.fetchall()
    return questions


@data_connection.connection_handler
def find_question_by_id(cursor, question_id):
    cursor.execute("""
                        SELECT * FROM question
                        WHERE id=%(id)s;
                       """,
                   {'id': question_id})
    question = cursor.fetchall()

    return question


@data_connection.connection_handler
def find_answer_by_id(cursor, question_id):
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id=%(question_id)s;
                       """,
                   {'question_id': question_id})
    answers = cursor.fetchall()

    return answers


def create_id(filename):
    data = connection.read_csv(filename)
    for item in data:
        id = item['id']
        if id == 'id':
            id = 0
        else:
            id = int(id) + 1
    return id


def write_csv(from_filename, to_filename, fieldnames, form_data):
    data = connection.read_csv(from_filename)
    data.append(form_data)
    with open(to_filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        for line in data:
            writer.writerow(line)
        return data


def find_question_id_from_answers(answer_id):
    question_data = connection.read_csv(answer_csv)
    for line in question_data:
        if line["id"] == answer_id:
            right_question_id = line["question_id"]
    return right_question_id


def delete_answer(id):
    answer_data = connection.read_csv(answer_csv)
    item_deleted_list = []
    for line in (answer_data):
        if line["id"] != str(id):
            item_deleted_list.append(line)
    connection.rewrite_csv(answer_csv, item_deleted_list, HEADER_ANSWER)


def delete_answers(id):
    answer_data = connection.read_csv(answer_csv)
    item_deleted_list = []
    for line in (answer_data):
        if line["question_id"] != str(id):
            item_deleted_list.append(line)
    connection.rewrite_csv(answer_csv, item_deleted_list, HEADER_ANSWER)


def delete_question(id):
    question_data = connection.read_csv(question_csv)
    item_deleted_list = []
    for line in (question_data):
        if line["id"] != str(id):
            item_deleted_list.append(line)
    connection.rewrite_csv(question_csv, item_deleted_list, HEADER)


def pluss_view_number(question_id):
    question_data = connection.read_csv(question_csv)
    for line in question_data:
        if question_id == line["id"]:
            view_count = int(line["view_number"])
            view_count += 1
            line["view_number"] = view_count
    connection.rewrite_csv(question_csv, question_data, HEADER)


def get_vote(question_id):
    question_data = connection.read_csv(question_csv)
    for line in question_data:
        if question_id == line["id"]:
            return line['vote_nr']
