import data_connection
from datetime import datetime
from psycopg2 import sql


@data_connection.connection_handler
def show_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id DESC;
                   """, )
    questions = cursor.fetchall()
    return questions


@data_connection.connection_handler
def show_5_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id DESC
                    LIMIT 5;
                    """)
    question_list = cursor.fetchall()

    return question_list


@data_connection.connection_handler
def find_question_by_id(cursor, id):
    cursor.execute("""
                        SELECT * FROM question
                        LEFT JOIN user_table ut on question.user_id = ut.user_id
                        WHERE question.id=%(id)s;
                       """,
                   {'id': id})
    question = cursor.fetchone()

    return question


@data_connection.connection_handler
def find_answer_by_id(cursor, question_id):
    cursor.execute("""
        SELECT * FROM answer
        JOIN user_table ut on answer.user_id = ut.user_id
        WHERE question_id=%(question_id)s;
       """,
                   {'question_id': question_id})
    answers = cursor.fetchall()

    return answers


@data_connection.connection_handler
def add_answer(cursor, question_id, message, submission_data, user_id):
    cursor.execute("""
                            INSERT INTO answer (question_id, message, submission_time, user_id)
                            VALUES (%(question_id)s, %(message)s, %(submission_data)s, %(user_id)s)
                           """,
                   {'question_id': question_id, 'message': message, 'submission_data': submission_data,
                    'user_id': user_id})


@data_connection.connection_handler
def find_question_id_from_answers(cursor, answer_id):
    cursor.execute("""
                            SELECT question_id FROM answer
                            WHERE id=%(id)s;
                           """,
                   {'id': answer_id})
    question_id = cursor.fetchall()

    return question_id


@data_connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                              DELETE FROM comment
                              WHERE answer_id=%(id)s;
                             """,
                   {'id': answer_id})
    cursor.execute("""
                              DELETE FROM answer
                              WHERE id=%(id)s;
                             """,
                   {'id': answer_id})


@data_connection.connection_handler
def add_comment_to_question(cursor, question_id, message, user_id):
    submission_time = datetime.now().isoformat(timespec='seconds')
    edited_count = 0
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s,%(user_id)s); """,
                   {'question_id': question_id, 'message': message, 'submission_time': submission_time,
                    'edited_count': edited_count, 'user_id': user_id})


@data_connection.connection_handler
def add_comment_to_answer(cursor, answer_id, message, user_id):
    submission_time = datetime.now().isoformat(timespec='seconds')
    edited_count = 0
    cursor.execute("""
                    INSERT INTO comment (answer_id, message, submission_time, edited_count, user_id)
                    VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s,%(user_id)s); """,
                   {'answer_id': answer_id, 'message': message, 'submission_time': submission_time,
                    'edited_count': edited_count, 'user_id': user_id})


@data_connection.connection_handler
def find_comment_by_question_id(cursor, question_id):
    cursor.execute("""
                        SELECT * FROM comment
                        LEFT JOIN user_table ut on comment.user_id = ut.user_id
                        WHERE question_id=%(question_id)s;
                       """,
                   {'question_id': question_id})
    comments = cursor.fetchall()

    return comments


@data_connection.connection_handler
def find_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                        SELECT * FROM comment
                        LEFT JOIN user_table ut on comment.user_id = ut.user_id
                        WHERE answer_id=%(answer_id)s;
                       """,
                   {'answer_id': answer_id})
    comments = cursor.fetchall()

    return comments


@data_connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id=%(id)s;""",
                   {'id': comment_id})


@data_connection.connection_handler
def add_question(cursor, submission_time, view_number, vote_number, title, message, image, user_id):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s,%(user_id)s);   
                    """,
                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': title, 'message': message, 'image': image, 'user_id': user_id})

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
                    SELECT * FROM question
                    WHERE (lower(title) LIKE lower(%(search_phrase)s) OR lower(message) LIKE lower(%(search_phrase)s));
    """,
                   {'search_phrase': '%' + search_phrase + '%'})

    result = cursor.fetchall()

    return result


@data_connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE id=%(answer_id)s;
                       """,
                   {'answer_id': answer_id})
    answers = cursor.fetchall()

    return answers


@data_connection.connection_handler
def update_answer_by_id(cursor, answer_id, message, submission_time):
    cursor.execute("""
                        UPDATE answer
                        SET message=%(message)s, submission_time=%(submission_time)s
                        WHERE id=%(answer_id)s;
                       """,
                   {'answer_id': answer_id, 'message': message, 'submission_time': submission_time})


@data_connection.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute("""
                        SELECT question_id FROM answer
                        WHERE id=%(answer_id)s;
                       """,
                   {'answer_id': answer_id})
    answers = cursor.fetchall()

    return answers


@data_connection.connection_handler
def find_answer_id_by_question_id(cursor, question_id):
    cursor.execute("""
                        SELECT id FROM answer
                        WHERE question_id=%(question_id)s;
                       """,
                   {'question_id': question_id})
    answers = cursor.fetchall()

    return answers


@data_connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                                  DELETE FROM comment
                                  WHERE question_id=%(question_id)s;
                                 """,
                   {'question_id': question_id})

    cursor.execute("""
                                  DELETE FROM question
                                  WHERE id=%(question_id)s;
                                 """,
                   {'question_id': question_id})


@data_connection.connection_handler
def add_view_count(cursor, question_id):
    cursor.execute("""
                    SELECT view_number FROM question
                    WHERE id=%(id)s;
                    """,
                   {'id': question_id})
    view_number = cursor.fetchone()
    view_number['view_number'] += 1
    number = view_number['view_number']

    cursor.execute("""
                    UPDATE question
                    SET view_number=(%(view_number)s)
                    WHERE id=%(id)s;
                    """,
                   {'id': question_id, 'view_number': number})

    cursor.execute("""
                    SELECT view_number FROM question
                    WHERE id=%(id)s;
                    """,
                   {'id': question_id})
    updated_view_number = cursor.fetchone()

    return updated_view_number


@data_connection.connection_handler
def sorted_title_desc(cursor, title):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                  ORDER BY {title} DESC;
        """).format(title=sql.Identifier(title)))
    title = cursor.fetchall()

    return title


@data_connection.connection_handler
def sorted_title_asc(cursor, title):
    cursor.execute(sql.SQL(""" SELECT * FROM question
                  ORDER BY {title} ASC;
        """).format(title=sql.Identifier(title)))
    title = cursor.fetchall()

    return title


@data_connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute(sql.SQL(""" SELECT user_id FROM user_table
                  WHERE username = %(username)s;
        """), {'username': username})
    id = cursor.fetchone()

    return id


@data_connection.connection_handler
def check_login_data(cursor, username):
    cursor.execute("""
                    SELECT username, password FROM user_table
                    WHERE username=%(username)s;
    """, {'username': username})

    login_info = cursor.fetchall()

    return login_info


@data_connection.connection_handler
def add_user(cursor, username, password, registry_date):
    cursor.execute("""
                    INSERT INTO user_table (username, password, registry_date) 
                    VALUES (%(username)s, %(password)s, %(registry_date)s); 
                    """,
                   {'username': username, 'password': password, 'registry_date': registry_date})

    cursor.execute("""
                    SELECT username, password, registry_date
                    FROM user_table
                    WHERE username=%(username)s;
                    """,
                   {'username': username})

    user = cursor.fetchone()

    return user


@data_connection.connection_handler
def get_user_all_question(cursor,id):
    cursor.execute("""select question.title,question.message
from user_table
right join question on user_table.user_id = question.user_id
WHERE user_table.user_id = %(id)s;
        """,  {'id': id})

    infos=cursor.fetchall()

    return infos

@data_connection.connection_handler
def list_all_user(cursor):
    cursor.execute("""
                    SELECT * FROM user_table
                    
                   """, )
    users = cursor.fetchall()
    return users

@data_connection.connection_handler
def get_user_all_answers(cursor,id):
    cursor.execute("""select answer.message, question.title as question_title
from user_table
right join answer on user_table.user_id = answer.user_id
right join question on user_table.user_id = question.user_id
WHERE user_table.user_id = %(id)s;
        """,  {'id': id})

    infos=cursor.fetchall()

    return infos

@data_connection.connection_handler
def get_user_all_comments_question(cursor,id):
    cursor.execute("""select username,comment.message,question.title as question_title ,question.message as question_message
from user_table 
right join comment on user_table.user_id = comment.user_id
right join  question on question.id= comment.question_id
WHERE user_table.user_id = %(id)s;
        """,  {'id': id})

    comments=cursor.fetchall()

    return comments

@data_connection.connection_handler
def get_user_all_comments_answer(cursor,id):
    cursor.execute("""select username,comment.message,answer.message as answer_message
from user_table 
right join comment on user_table.user_id = comment.user_id
right join  answer on answer.id = comment.answer_id 
WHERE user_table.user_id = %(id)s;
        """,  {'id': id})

    comments=cursor.fetchall()

    return comments

@data_connection.connection_handler
def check_login_data(cursor, username):
    cursor.execute("""
                    SELECT username, password FROM user_table
                    WHERE username=%(username)s;
    """, {'username': username})

    login_info = cursor.fetchall()

    return login_info

@data_connection.connection_handler
def get_user_by_id(cursor, id):
    cursor.execute(sql.SQL(""" SELECT username FROM user_table
                  WHERE user_id = %(id)s;
        """), {'id': id})
    id = cursor.fetchone()

    return id


@data_connection.connection_handler
def false_all_accept(cursor):
    cursor.execute("""
                    update answer set accepted = 'False'
where id >'0'
                   """, )

@data_connection.connection_handler
def true_accept(cursor,id):
    cursor.execute("""
                    update answer set accepted = 'True'
where id = %(id)s;
        """, {'id': id})
