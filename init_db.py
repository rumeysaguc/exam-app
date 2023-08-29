import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="weather-forecast",
    user='postgres',
    password='1234')

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute('DROP TABLE IF EXISTS accounts;')
# cur.execute('CREATE TABLE accounts (id serial PRIMARY KEY,'
#             'username varchar (150) NOT NULL,'
#             'email varchar (50) NOT NULL,'
#             'password varchar (50) NOT NULL,'
#             'date_added date DEFAULT CURRENT_TIMESTAMP);'
#             )
#

# Insert data into the table

cur.execute('INSERT INTO question (text, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('python kim tarafından geliştirilmiştir',
             'Charles Dickens',
             489,
             'A great classic!')
            )


conn.commit()

cur.close()
conn.close()
