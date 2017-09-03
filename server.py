import re
from flask import flash, Flask, redirect, request, render_template, session, url_for
from mysqlconnection import MySQLConnection

emailRgxp = re.compile(r'^[\d\w]{1,60}[\d\w.]{0,20}@[\d\w]{1,5}[\d\w.]{0,20}.[a-zA-Z.]{2,6}/?$')

app = Flask(__name__)
app.secret_key = 'get_your_own_password,_kid!'
mysql = MySQLConnection(app, 'mydb')

@app.route('/', methods=['GET'])
def index():
    qstring = "SELECT * FROM emails;"
    emails = mysql.query_db(qstring)
    return render_template('index.html', emails=emails)

@app.route('/', methods=['POST'])
def validating():
    if emailRgxp.match(request.form['email']):
        qstring = """
                    INSERT INTO `mydb`.`emails`
                    (`address`)
                    VALUES
                    ('{}');
                  """.format(request.form['email'])
        print qstring
        try: 
            q = mysql.query_db(qstring)
            print dir(q)
        except Exception:
            flash('database error')
        return redirect('/')
    else:
        flash('{} is not a valid email in our book'.format(request.form['email']))
        return redirect('/')


if __name__ == '__main__':
  app.run(port=8000, debug=True)