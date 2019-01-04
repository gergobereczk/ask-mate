import connection
import csv

question_csv = "sample_data/question.csv"

answer_csv = "sample_data/answer.csv"

HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def show_question():
    question_list = []
    question_data = connection.read_csv(question_csv)
    the_len_value = (len(question_data))+1
    for item in range(1, the_len_value):
        question_list.append(question_data[(item*-1)])
    return question_list


def find_question_from_id(question_id):
    question_data=connection.read_csv(question_csv)
    for item in question_data:
        if item['id'] == str(question_id):
            return item


def find_answer_from_id(question_id):
    list_from_right_answer = []
    answer_data = connection.read_csv(answer_csv)
    for line in answer_data:
        if line["question_id"] == str(question_id):
            list_from_right_answer.append(line)
    return list_from_right_answer


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
    connection.rewrite_csv(answer_csv,item_deleted_list, HEADER_ANSWER)