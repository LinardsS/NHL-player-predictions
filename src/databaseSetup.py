import sqlite3

conn = sqlite3.connect('main.db')

c = conn.cursor()

# c.execute("""CREATE TABLE teams(
#             name text,
#             id integer,
#             abbreviation text,
#             conference_id integer,
#             division_id integer
#             ) """)

# c.execute("""CREATE TABLE players(
#             name text,
#             id integer,
#             position text
#             )""")
c.execute("ALTER TABLE players ADD team_id integer")

conn.commit()
conn.close()