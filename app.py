from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os 
app = Flask(__name__)
 
#  MySQL Configuration
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "employee_db")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "root")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "localhost")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT", 3306))
mysql = MySQL(app)

# Home Page - Show Employees
@app.route('/')
def index():
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    cur.close()
    return render_template("index.html", employees=employees)

# Add Employee Page
@app.route('/add')
def add_page():
    return render_template("add.html")

# Insert Employee
@app.route('/insert', methods=["POST"])
def insert_employee():
    eid = request.form['eid']
    ename = request.form['ename']
    esal = request.form['esal']
    eaddr = request.form['eaddr']
    egender = request.form['egender']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO employee (eid, ename, esal, eaddr, egender) VALUES (%s, %s, %s, %s, %s)",
        (eid, ename, esal, eaddr, egender)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Edit Employee Page
@app.route('/edit/<int:eid>')
def edit_page(eid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE eid=%s", (eid,))
    employee = cur.fetchone()
    cur.close()
    return render_template("edit.html", employee=employee)

# Update Employee
@app.route('/update/<int:eid>', methods=["POST"])
def update_employee(eid):
    ename = request.form['ename']
    esal = request.form['esal']
    eaddr = request.form['eaddr']
    egender = request.form['egender']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE employee SET ename=%s, esal=%s, eaddr=%s, egender=%s WHERE eid=%s",
        (ename, esal, eaddr, egender, eid)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Delete Employee
@app.route('/delete/<int:eid>')
def delete_employee(eid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE eid=%s", (eid,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
