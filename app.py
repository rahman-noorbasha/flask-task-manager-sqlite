from flask import Flask,render_template,request,redirect
import sqlite3
app=Flask(__name__)
def init_db():
    conn=sqlite3.connect("tasks.db")
    cursor= conn.cursor()
    cursor.execute(""" 
        create table if not exists tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task TEXT NOT NULL)""")
    conn.commit()
    conn.close()
init_db()
@app.route("/",methods=["GET","POST"])
def home():
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()
    if request.method=="POST":
        task=request.form["task"]
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
    cursor.execute("SELECT*FROM tasks")
    tasks=cursor.fetchall()
    return render_template("index.html",tasks=tasks)
@app.route("/delete/<int:id>")
def delete_task(id):
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
