""" This is the program to run"""
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests  # for API example
import random

mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__, template_folder="templates")

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'example'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/enternew')
def new_staff():
    return render_template('new.html')


@app.route('/update')
def update_staff():
    return render_template('update.html')


@app.route('/remove')
def remove_staff():
    return render_template('remove.html')


@app.route("/staff", methods=['GET'])
def staff():
    try:
        con = mysql.connect()  # set up database connection
        cur = con.cursor()

    except:
        con.rollback()

    finally:
        # API for date and time ---------------------------------------------------------------------------
        url = "http://worldtimeapi.org/api/timezone/Europe/London"
        response = requests.get(url).json()
        print("" + str(response))  # response details
        date_time = response["datetime"]  # retrieve response details form the attribute, datetime
        # -------------------------------------------------------------------------------------------------

        cur.execute('SELECT staff.id, staff.name, staff.position FROM staff')
        print("retrieve the data from the database")
        rows = cur.fetchall()
        con.commit()
        msg = "Date/Time: " + str(date_time)

        return render_template("index.html", rows=rows, msg=msg)

        con.close()


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        rows = []
        try:
            print("--------------------------Demo Start----------------------------------------")
            con = mysql.connect()  # set up database connection
            cur = con.cursor()

            s_id = "st" + str(random.randint(1000, 9999))
            name = request.form['name']  # retrieve form data
            position = request.form['position']
            print("to register a staff")

            # insert data to the database
            cur.execute('INSERT INTO staff (id, name, position)'
                        'VALUES( %s, %s, %s)',
                        (s_id, name, position))

            con.commit()
            print("write to the staff table")

            # testing - retrieve data from the database
            cur.execute('SELECT staff.id, staff.name, staff.position FROM staff')

            rows = cur.fetchall()
            row_num = len(rows)
            print("staff:  ", row_num)
            for row in rows:
                print("id: ", row[0])
                print("name: ", row[1])
                print("position: ", row[2])

            con.commit()
            rows = rows
            return render_template("index.html", rows=rows)
        except:
            con.rollback()
        finally:
            rows = rows
            return render_template("index.html", rows=rows)
            con.close()


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        try:
            s_id = request.form['id']
            position = request.form['position']

            con = mysql.connect()
            cur = con.cursor()
            cur.execute('UPDATE Staff SET position=%s WHERE id=%s', (position, s_id))
            con.commit()

            print("update the staff table")
            cur.execute('SELECT staff.id, staff.name, staff.position FROM staff')
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()
        finally:
            return render_template("index.html", rows=rows)
            con.close()


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            s_id = request.form['id']
            con = mysql.connect()
            cur = con.cursor()

            cur.execute('DELETE FROM Staff WHERE id=%s', s_id)
            con.commit()
            print("delete the staff from the staff table")

        except:
            con.rollback()

        finally:
            cur.execute('SELECT staff.id, staff.name, staff.position FROM staff')
            rows = cur.fetchall()
            con.commit()

            return render_template("index.html", rows=rows)
            con.close()


if __name__ == "__main__":
    app.run()