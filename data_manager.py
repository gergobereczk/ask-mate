import connection

question_csv = "sample_data/question.csv"

answer_csv = "sample_data/answer.csv"

def find_question_from_id(question_id):
    list_from_right_question = []
    question_data = connection.read_csv(question_csv)
    for line in range(len(question_data)):
        if question_data[line][0] == question_id:
            list_from_right_question = question_data[line]
    return list_from_right_question

def find_answer_from_id(question_id):
    list_from_right_answer = []
    answer_data = connection.read_csv(answer_csv)
    for line in range(len(answer_data)):
        if answer_data[line][3] == question_id:
            list_from_right_answer.append(answer_data[line])
    return list_from_right_answer


def create_id(filename):
    with open(filename, 'r') as file:
        for line in file:
            id = line[0]
            if line[0] == 'id':
                id = 0
            else:
               id = int(id) + 1
        return id

