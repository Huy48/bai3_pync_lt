import sqlite3
import os

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = os.urandom(24)

def get_students():
	conn = sqlite3.connect('students.db')
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()
	
	cursor.execute("SELECT rowid, HoTen, NgaySinh, Diem, DieuKien FROM students")
	
	students = cursor.fetchall()
	
	conn.close()
	return students

def init_db():
	conn = sqlite3.connect('students.db')
	conn.row_factory = sqlite3.Row
	conn.execute('''
	CREATE TABLE IF NOT EXISTS students (
		HoTen TEXT NOT NULL,
		NgaySinh TEXT NOT NULL,
		Diem REAL NOT NULL,
		DieuKien TEXT NOT NULL
	)
	''')
	conn.commit()
	conn.close()

def get_db_connection():
	conn = sqlite3.connect('students.db')
	conn.row_factory = sqlite3.Row
	return conn

@app.route('/')
def index():
	student_list = get_students()
	return render_template('index.html', students=student_list)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
	if request.method == 'POST':
		ho_ten = request.form['hoten']
		ngay_sinh = request.form['ngaysinh']
		diem = float(request.form['diem'])
		dieu_kien = "Hợp lệ" if diem >= 18 else "Cần xem xét"

		conn = sqlite3.connect('students.db')
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO students (HoTen, NgaySinh, Diem, DieuKien) VALUES (?, ?, ?, ?)''', (ho_ten, ngay_sinh, diem, dieu_kien))
		conn.commit()
		conn.close()

		flash('Sinh viên đã được thêm thành công!')
		return redirect(url_for('index'))
	return render_template('form.html')

@app.route('/delete/<int:rowid>', methods=['POST'])
def delete_student(rowid):
	conn = get_db_connection()
	conn.execute('DELETE FROM students WHERE rowid = ?', (rowid,))
	conn.commit()
	conn.close()
	flash('Sinh viên đã được xóa thành công!')
	return redirect(url_for('index'))

@app.route('/update/<int:rowid>', methods=['GET', 'POST'])
def update_student(rowid):
	conn = sqlite3.connect('students.db')
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()

	cursor.execute("SELECT rowid, HoTen, NgaySinh, Diem, DieuKien FROM students WHERE rowid = ?", (rowid,))
	student = cursor.fetchone()

	if request.method == 'POST':
		ho_ten = request.form['hoten']
		ngay_sinh = request.form['ngaysinh']
		diem = float(request.form['diem'])
		dieu_kien = "Hợp lệ" if diem >= 18 else "Cần xem xét"

		if ho_ten and ngay_sinh:
			cursor.execute('''
				UPDATE students 
				SET HoTen = ?, NgaySinh = ?, Diem = ?, DieuKien = ? 
				WHERE rowid = ?
			''', (ho_ten, ngay_sinh, diem, dieu_kien, rowid))
			conn.commit()
			conn.close()
			flash('Sinh viên đã được cập nhật thành công!')
			return redirect(url_for('index'))
		else:
			flash('Vui lòng nhập đầy đủ thông tin!')

	conn.close()
	return render_template('form.html', student=student)


if __name__ == "__main__":
	init_db()
	app.run(debug=True)
