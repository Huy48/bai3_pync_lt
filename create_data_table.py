import sqlite3

conn = sqlite3.connect('students.db')

c = conn.cursor()

c.execute(''' 
	CREATE TABLE IF NOT EXISTS students (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		HoTen TEXT NOT NULL,
		NgaySinh TEXT NOT NULL,
		Diem REAL NOT NULL,
		DieuKien TEXT NOT NULL
	)
''')

c.execute('''
	CREATE TABLE IF NOT EXISTS students_new (
		rowid INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		age INTEGER NOT NULL
	)
''')

try:
	c.execute('''
		INSERT INTO students_new (rowid, name, age)
		SELECT id, HoTen, 20 FROM students
	''')
except sqlite3.OperationalError:
	print("Bảng 'students' chưa có dữ liệu để sao chép!")

c.execute('DROP TABLE IF EXISTS students')

c.execute('ALTER TABLE students_new RENAME TO students')

conn.commit()

conn.close()

print("Bảng 'students' đã được thay đổi cấu trúc thành công.")
