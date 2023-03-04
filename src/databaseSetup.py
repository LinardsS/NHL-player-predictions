import sqlite3

conn = sqlite3.connect('main.db')

c = conn.cursor()

c.execute("""CREATE TABLE teams(
            name text,
            id integer,
            abbreviation text,
            conference_id integer,
            division_id integer
            ) """)

conn.commit()

conn.close()