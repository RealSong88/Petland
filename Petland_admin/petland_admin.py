from flask import Flask, render_template, session, url_for, request, redirect
import mariadb
from sql import show_res, show_cus, show_staff, get_conn

app = Flask(__name__)
app.debug = True
app.secret_key = b'aaa!111/'


def user(form_id, form_passwd):
    data = []
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        SELECT * FROM admin WHERE id="{}" AND password="{}"
    """.format(form_id, form_passwd)
    cur.execute(sql)
    # for num, id, password, name in cur:
    #     data += num, name
    data = cur.fetchone()
    return data


@app.route('/')
def base():
    # return render_template("login.html")
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # if session['user'] != None:
        #     return redirect(url_for('form'))

        # return render_template('login.html')
        if 'user' in session:
            return redirect(url_for('form'))
        return render_template("login.html")
    else:
        id = request.form['id']
        passwd = request.form['passwd']
        try:
            data = user(id, passwd)
            print(data)
            if data != None:
                session['user'] = id
                print(session['user'])
                return """
                    <script> alert("안녕하세요~ {}님");
                    location.href="/reservation"
                    </script>
                """.format(id)
                # return redirect(url_for('base'))
            else:
                return """
                    <script> alert("아이디 또는 패스워드를 확인 하세요.");
                    location.href="/login"
                    </script>
                """
                # return "아이디 또는 패스워드를 확인 하세요"
        except:
            return "Don't Login"


@app.route('/logout')
def logout():
    session.clear()
    # session.pop('user', None)
    return redirect(url_for('form'))


@app.route('/reservation', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':

        if 'user' in session:
            content = show_res()
            return render_template('base.html', user=session['user'], content=content)
        return redirect(url_for('login'))
    # else:


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'GET':
        if 'user' in session:
            content = show_cus()
            return render_template("customer_management.html", user=session['user'], content=content)
        return redirect(url_for('login'))


@app.route('/staff', methods=['GET', 'POST'])
def staff():
    if request.method == 'GET':
        if 'user' in session:
            content = show_staff()
            return render_template("staff_management.html", user=session['user'], content=content)
        return redirect(url_for('login'))


if __name__ == "__main__":

    app.run(host='0.0.0.0')
