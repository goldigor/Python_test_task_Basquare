import os
import sys
import sqlite3
from sqlite3 import Error

DELIMITERS = [" ", ",", ".", os.linesep, ]
default_db_name = 'Basquare.sqlite3'
table = {'name': 'WORDS_OCCURRENCE_TABLE',
         'column_1': {'name':'id',
                      'desc': 'integer PRIMARY KEY'},
         'column_2': {'name': 'word',
                      'desc': 'text'},
         'column_3': {'name': 'count',
                      'desc': 'integer'},
         }

try:
    used_dir=sys.argv[1]
except:
    print('Please, pass directory name!')
    sys.exit()

all_files = os.listdir(used_dir)
txt_files = [file for file in all_files if file.endswith('.txt')]

replacements = DELIMITERS[:]
replacements.remove(' ')

all_words = []
for file_name in txt_files:
    file = os.path.join(used_dir, file_name)
    with open(file) as input_file:
        text = input_file.read()
        text = text.lower()
        for replacement in replacements:
            text = text.replace(replacement, ' ')
        words = text.split()
        all_words.extend(words)

unique_words = set(all_words)
words_occurrence = dict()
for unique_word in unique_words:
    words_occurrence[unique_word] = all_words.count(unique_word)

db_file = [file for file in all_files if file.endswith('.sqlite3')]
if db_file:
    db_file = os.path.join(used_dir, db_file[0])
else:
    db_file = os.path.join(used_dir, default_db_name)

connection = None
try:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    sql_drop_table = "DROP TABLE IF EXISTS {0};".format(table['name'])
    cursor.execute(sql_drop_table)
    sql_create_table = """CREATE TABLE {0} (
                                            {1} {2},
                                            {3} {4},
                                            {5} {6}
                                        ); """.format(table['name'],
                                                      table['column_1']['name'],
                                                      table['column_1']['desc'],
                                                      table['column_2']['name'],
                                                      table['column_2']['desc'],
                                                      table['column_3']['name'],
                                                      table['column_3']['desc'])
    cursor.execute(sql_create_table)
    for word, count in words_occurrence.items():
        sql_insert_into_table = """INSERT INTO {0} ({1}, {2}) 
                                   VALUES('{3}', {4}); """.format(table['name'],
                                                                table['column_2']['name'],
                                                                table['column_3']['name'],
                                                                word,
                                                                count)
        cursor.execute(sql_insert_into_table)
except Error as e:
    print(e)
finally:
    if connection:
        connection.commit()
        connection.close()






