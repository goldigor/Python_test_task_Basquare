import os
import sys
from sqlite3 import Error
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import delete

DELIMITERS = [" ", ",", ".", os.linesep, ]
default_db_name = 'Basquare.sqlite3'
table_name = 'WORDS_OCCURRENCE_TABLE'

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

try:
    engine = create_engine('sqlite://' + '/' + db_file)
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)
    if table is not None:
        # with DROP
        # Base.metadata.drop_all(engine, [table], checkfirst=True)

        # with DELETE
        connection = engine.connect()
        stmt = table.delete()
        connection.execute(stmt)

    class Words_occurrence_table(Base):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)
        word = Column(String)
        count = Column(Integer)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for word, count in words_occurrence.items():
        row = Words_occurrence_table(word=word, count=count)
        session.add(row)
except Error as e:
    print(e)
finally:
    session.commit()






