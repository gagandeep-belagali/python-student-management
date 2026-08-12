from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students
    )


@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO students (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)