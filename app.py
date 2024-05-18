import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def db_connection():
    conn = sqlite3.connect('user_db.sqlite3')
    return conn


def get_all_users():
    conn = db_connection()
    users_data = conn.execute("SELECT * FROM students order by id desc limit 5").fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1], 'gender': row[2], 'phone': row[3], 'email': row[4], 'address': row[5]} for
            row in users_data]


@app.route('/')
def hello_world():
    return render_template('master.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', module='dashboard')


@app.route('/user')
def user():
    return render_template('user.html', module='user', data=get_all_users())


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.form
        conn = db_connection()
        conn.execute("INSERT INTO students (username,email,gender,phone,address) VALUES (?, ?, ?, ?, ?)",
                     (data['username'], data['email'], data['gender'], data['phone'], data['address']))
        conn.commit()
        conn.close()
        return redirect(url_for('user'))
    return render_template('user.html', module='user')


@app.route('/view_user', methods=['GET'])
def view_user():
    user_id = request.args.get('id')
    conn = db_connection()
    user = conn.execute("SELECT * FROM students WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return render_template('view_user.html', user=user, data=user)


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    user_id = request.args.get('id')
    conn = db_connection()
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['username']
        email = request.form['email']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']

        conn.execute("""
            UPDATE students
            SET username=?, email=?, gender=?, phone=?, address=?
            WHERE id=?
        """, (name, email, gender, phone, address, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('user'))
    user = conn.execute("SELECT * FROM students WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return render_template('edit_user.html', module='user', data=user)


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    user_id = request.args.get('id')
    conn = db_connection()
    user = conn.execute("SELECT * FROM students WHERE id=?", (user_id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        conn = db_connection()
        conn.execute("DELETE FROM students WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('user'))
    return render_template('delete_user.html', module='user', data=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

@app.errorhandler(500)
def page_error(e):
    return render_template('error-500.html')

if __name__ == '__main__':
    app.run()
