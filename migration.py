import sqlite3

print("Creating DB")
conn = sqlite3.connect("fb.db")
print("DB created")

conn.execute(
    "CREATE TABLE facebook (id INTEGER PRIMARY KEY AUTOINCREMENT, username char(100) NOT NULL, email char(100) NOT NULL UNIQUE, password char(100) NOT NULL, cookie char(128) UNIQUE)"
)
conn.execute(
    "INSERT INTO facebook (username, email, password) VALUES('Chrsitophe', 'christophe@facebook.com', 'TEST123@')"
)
conn.commit()

select = conn.execute("SELECT* FROM facebook")
print(select)
print("table created")
