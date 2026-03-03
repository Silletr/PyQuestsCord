from parser import DB_PATH
import sqlite3 as sq

conn = sq.connect(DB_PATH)
cursor = conn.cursor()

game_name = "Grand Theft "
cursor.execute("SELECT * FROM games WHERE game_name LIKE ?", (f"%{game_name}%",))

rows = cursor.fetchall()

print(rows)

conn.close()
