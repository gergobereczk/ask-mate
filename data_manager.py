import connection
import data_connection
from datetime import datetime
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
def find_question_by_id(cursor, id):
    cursor.execute("""
                        SELECT * FROM question
                        WHERE id=%(id)s;
                       """,
                   {'id': id})
    question = cursor.fetchone()

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

@data_connection.connection_handler
def add_answer(cursor, question_id, message, submission_data):
    cursor.execute("""
                            INSERT INTO answer (question_id, message, submission_time)
                            VALUES (%(question_id)s, %(message)s, %(submission_data)s)
                           """,
                   {'question_id': question_id, 'message':message, 'submission_data':submission_data})


@data_connection.connection_handler
def find_question_id_from_answers(cursor, answer_id):
    cursor.execute("""
                            SELECT question_id FROM answer
                            WHERE id=%(id)s;
                           """,
                   {'id': answer_id})
    question_id = cursor.fetchall()

    return question_id

    return right_question_id


@data_connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                              DELETE FROM answer
                              WHERE id=%(id)s;
                             """,
                   {'id': answer_id})


@data_connection.connection_handler
def add_comment(cursor, question_id, message):
    submission_time = datetime.now()
    edited_count = 0
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s); """,
                   {'question_id': question_id, 'message': message, 'submission_time':submission_time,
                    'edited_count': edited_count})


def add_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);   
                    """,
                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': title, 'message': message, 'image': image})

    cursor.execute("""
                    SELECT id FROM question
                    WHERE submission_time=%(submission_time)s;
                    """,
                   {'submission_time': submission_time})
    id = cursor.fetchall()

    return id

@data_connection.connection_handler
def search_question(cursor, search_phrase):
    cursor.execute("""
                        SELECT * FROM question, answer
                        WHERE title OR message LIKE search_phrase; 
    """,
                   {'search_phrase': '%' + search_phrase + '%'})

    result = cursor.fetchall()

    return result




@data_connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                                  DELETE FROM answer
                                  WHERE question_id=%(question_id)s;
                                 """,
                   {'question_id': question_id})
    cursor.execute("""
                                  DELETE FROM question
                                  WHERE id=%(id)s;
                                 """,
                   {'id': question_id})


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
