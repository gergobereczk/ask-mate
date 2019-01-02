import connection

question_csv = "sample_data/question.csv"

answer_csv = "sample_data/answer.csv"


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
    with open(filename, 'r') as file:
        id = line[0]
        for line in file:
            if line[0] == 'id':
                id = 0
            else:
                id +=1
        return id

