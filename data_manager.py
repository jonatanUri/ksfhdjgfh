import csv
import time
import data_paths
import os
import database_common

question_path = data_paths.question_path
answer_path = data_paths.answer_path
question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@database_common.connection_handler
def read_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                    """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def read_latest_five_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def answer_by_question_id(cursor, id_):
    cursor.execute("""
                    SELECT * FROM answer  where question_id=%(id_)s;
                    """, {'id_': id_})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def read_a_question(cursor, id_):
    cursor.execute("""
                    SELECT * FROM question where id=%(id_)s;
                    """, {'id_': id_})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def read_answer(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                    """)
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def read_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment;""")
    comments = cursor.fetchall()
    return comments


def convert_dict_to_human_readable(list_of_dicts):
    new_csv = []
    for row in list_of_dicts:
        if 'submission_time' in row:
            row['submission_time'] = convert_time(row['submission_time'])
        new_csv.append(row)
    return new_csv


def convert_time(unix_timestamp):
    readable_time = time.ctime(int(unix_timestamp))
    return readable_time


@database_common.connection_handler
def update_answer(cursor, answer_update, id_):
        cursor.execute("""
                            UPDATE answer
                            SET message =%(answer_update)s
                            WHERE id= %(id_)s;
                            """, {'answer_update': answer_update, 'id_': id_})


@database_common.connection_handler
def update_comment(cursor, comment_update, question_id_, comment_id_):
        cursor.execute("""
                            UPDATE comment
                            SET message=%(comment_update)s
                            WHERE question_id=%(question_id_)s AND id= %(comment_id_)s
                            """, {'comment_update': comment_update, 'question_id_': question_id_,
                                  'comment_id_': comment_id_})


@database_common.connection_handler
def update_answer_comment(cursor, comment_update, answer_id_, comment_id_):
    cursor.execute("""
                    UPDATE comment
                    SET message=%(comment_update)s
                    WHERE answer_id=%(answer_id_)s AND id=%(comment_id_)s; 
                    """, {'comment_update': comment_update, 'answer_id_': answer_id_,
                          'comment_id_': comment_id_})

@database_common.connection_handler
def delete_all_comments_from_answer(cursor, id_):
    cursor.execute("""
                        DELETE FROM comment WHERE answer_id=%(id_)s 
                        """,
                   {'id_': id_})




@database_common.connection_handler
def delete_answer(cursor, id_):
    cursor.execute("""
                    DELETE FROM answer WHERE id= %(id_)s 
                    """,
                   {'id_': id_})


@database_common.connection_handler
def add_question(cursor, new_question):
    cursor.execute("""
                        INSERT INTO question(id, submission_time, view_number, vote_number, title, message, image) 
                        VALUES (%(id)s,%(submission_time)s, %(view_number)s, %(vote_number)s,%(title)s,%(message)s,
                        %(image)s);
                        """, new_question)


@database_common.connection_handler
def add_answer(cursor, new_answer):
    cursor.execute("""
                            INSERT INTO answer(id, submission_time, vote_number,question_id, message, image) 
                            VALUES (%(id)s,%(submission_time)s, %(vote_number)s, %(question_id)s,%(message)s,
                            %(image)s);
                            """, new_answer)


def sorted_by_submission_time(list_of_dicts):
    n = len(list_of_dicts)
    for i in range(n):
        for j in range(i, n):
            if list_of_dicts[j]['submission_time'] > list_of_dicts[i]['submission_time']:
                temp = list_of_dicts[i]
                list_of_dicts[i] = list_of_dicts[j]
                list_of_dicts[j] = temp
    return list_of_dicts


def get_new_question_id():
    questions = read_all_questions()
    max_id = "0"
    for i in questions:
        if int(max_id) < int(i['id']):
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)


def get_new_answer_id():
    answers = read_answer()
    max_id = "0"
    for i in answers:
        if int(max_id) < int(i['id']):
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)


def get_new_comment_id():
    comments = read_comments()
    max_id = "0"
    for i in comments:
        if int(max_id) < int(i['id']):
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)


def get_current_unix_timestamp():
    current_time = time.time()
    return int(current_time)


"""@database_common.connection_handler
def vote_up(cursor, id_):
    cursor.execute(
                  UPDATE answers
                  SET vote_number=vote_number+1
                  WHERE id=%(id_)s ;
                  ,
                   {'id_': id_}"""


"""@database_common.connection_handler
def vote_down(cursor, id_):
    cursor.execute(
                  #UPDATE answers
                  #SET vote_number=vote_number-1
                  #WHERE id=%(id_)s ;
                  ,
                   {'id_': id_})"""


@database_common.connection_handler
def comment_on_question(cursor, new_comment):
    cursor.execute("""INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count)
                        VALUES (%(id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);""", new_comment)


@database_common.connection_handler
def read_q_comments(cursor, id_):
    cursor.execute("""
                        SELECT message, submission_time,id FROM comment  where question_id=%(id_)s;
                        """, {'id_': id_})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def get_this_answer(cursor, question_id_, answer_id_):
    cursor.execute("""
                    SELECT message FROM answer  where id=%(answer_id_)s AND question_id=%(question_id_)s ;
                    """, {'question_id_': question_id_, 'answer_id_': answer_id_})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_this_answer_comment(cursor, comment_id_):
    cursor.execute("""
                    SELECT message FROM comment
                    WHERE id=%(comment_id_)s
                    """, {'comment_id_': comment_id_})
    comment = cursor.fetchall()
    return comment



@database_common.connection_handler
def read_a_comments(cursor, id_):
    cursor.execute("""
                        SELECT message, submission_time, id FROM comment  where answer_id=%(id_)s;
                        """, {'id_': id_})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def comment_on_answer_question(cursor, new_comment):
    cursor.execute("""INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count)
                        VALUES (%(id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);""", new_comment)


@database_common.connection_handler
def get_this_comment(cursor, question_id_, comment_id_):
    cursor.execute("""
                    SELECT message FROM comment WHERE question_id=%(question_id_)s AND id=%(comment_id_)s;
                    """, {'question_id_': question_id_, 'comment_id_': comment_id_})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def delete_comment(cursor, question_id_, comment_id_):
    cursor.execute("""
                    DELETE FROM comment WHERE question_id=%(question_id_)s AND id= %(comment_id_)s
                    """, {'question_id_': question_id_, 'comment_id_': comment_id_})

@database_common.connection_handler
def delete_comment_for_answer(cursor, answer_id_, comment_id_):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id =%(answer_id_)s AND id= %(comment_id_)s
                    """, {'answer_id_': answer_id_, 'comment_id_': comment_id_})


@database_common.connection_handler
def delete_all_comments_and_answer_for_a_question(cursor, answer_id_, question_id_):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id =%(answer_id_)s;
                    """, {'answer_id_': answer_id_})
    cursor.execute("""
                        DELETE FROM answer WHERE question_id =%(question_id_)s;
                        """, {'question_id_': question_id_})


@database_common.connection_handler
def delete_answer_comment(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id=%(answer_id)s;""",
                   {'answer_id': answer_id})


@database_common.connection_handler
def delete_question(cursor, id_):
    cursor.execute("""
                    DELETE FROM comment WHERE question_id=%(question_id_)s;
                    DELETE FROM comment WHERE answer_id 
                    IN (SELECT id FROM answer WHERE question_id =%(question_id_)s);
                    """, {'question_id_': id_})
    cursor.execute("""
                        DELETE FROM answer WHERE question_id= %(id_)s;
                        DELETE FROM question WHERE id= %(id_)s
                        """,
                   {'id_': id_})


