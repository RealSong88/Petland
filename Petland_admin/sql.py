import mariadb
from flask import request


def get_conn():
    conn = mariadb.connect(user="<DB 아이디>",
                           password="<패스워드>",
                           host="<서버IP>",
                           port=3306,
                           database="Petland")
    return conn


def show_res():
    result = ""
    sql = get_sql_form()
    print(sql)
    try:
        conn = get_conn()
        cur = conn.cursor()

        if sql[:6] == 'DELETE':
            cur.execute(sql)
            conn.commit()
            sql = """SELECT r.r_num, u.u_name, r.r_date, r.r_time, r.pet, r.service, r.r_p_id
                FROM reservation r
                LEFT JOIN user_info u ON u.u_id = r.r_u_id
                ORDER BY r.r_num
            """

        # conn.commit()후 변경 사항을 출력하기위한 쿼리 cmd가 없을 시에는
        # 현재 db값을 출력
        sql_base = sql
        cur.execute(sql_base)
        for r_num, u_name, r_date, r_time, pet, service, r_p_id in cur:
            result += "<tr>"
            result += "<td>" + str(r_num) + "</td>"
            result += "<td>" + u_name + "</td>"
            result += "<td>" + str(r_date) + "</td>"
            result += "<td>" + r_time + "</td>"
            result += "<td>" + pet + "</td>"
            result += "<td>" + service + "</td>"
            result += "<td>" + str(r_p_id) + "</td>"
            result += """<td><a href="/form?cmd=delete&r_num={}">삭제</a></td>""".format(
                str(r_num))
            result += "</tr>"

        # print(result)
    except mariadb.Error as e:
        # err = "예약 건수가 남아있어 삭제 할 수 없습니다."
        print("ERR: {}".format(e))
    finally:
        if conn:
            conn.close()
    return result


def show_cus():
    result = ""
    sql = get_sql_customer()
    print(sql)
    try:
        conn = get_conn()
        cur = conn.cursor()

        if sql[:6] == 'DELETE':
            cur.execute(sql)
            conn.commit()
            sql = """SELECT * FROM pet_sitter"""

        # sql = "SELECT * FROM user_info"
        sql_base = sql
        cur.execute(sql_base)
        for u_id, u_name, u_phone, u_address in cur:
            result += "<tr>"
            result += "<td>" + str(u_id) + "</td>"
            result += "<td>" + u_name + "</td>"
            result += "<td>" + u_phone + "</td>"
            result += "<td>" + u_address + "</td>"
            result += """<td><a href="/customer?cmd=delete&u_id={}">삭제</a></td>""".format(
                str(u_id))
            result += "</tr>"
    except mariadb.Error as e:
        print("ERR: {}".format(e))
    finally:
        if conn:
            conn.close()
    return result


def show_staff():
    result = ""
    sql = get_sql_staff()
    print(sql)
    try:
        conn = get_conn()
        cur = conn.cursor()

        if sql[:6] == 'DELETE':
            cur.execute(sql)
            conn.commit()
            sql = "SELECT * FROM pet_sitter"

        # sql = "SELECT * FROM pet_sitter"
        sql_base = sql
        print(sql)
        cur.execute(sql_base)
        for p_id, p_name, p_phone, p_local in cur:
            result += "<tr>"
            result += "<td>" + str(p_id) + "</td>"
            result += "<td>" + p_name + "</td>"
            result += "<td>" + p_phone + "</td>"
            result += "<td>" + p_local + "</td>"
            result += """<td><a href="/staff?cmd=delete&p_id={}">삭제</a></td>""".format(
                str(p_id))
            result += "</tr>"
        # print(result)
    except mariadb.Error as e:
        print("ERR: {}".format(e))
    finally:
        if conn:
            conn.close()
    return result


def get_sql_form():
    cmd = request.args.get('cmd')

    if cmd == 'delete':
        r_num = request.args.get('r_num')
        sql = """DELETE FROM reservation WHERE r_num={}
        """.format(int(r_num))
    elif cmd == 'search':
        name = request.args.get('name')
        print(name)
        print(type(name))
        sql = """SELECT r.r_num, u.u_name, r.r_date, r.r_time, r.pet, r.service, r.r_p_id
            FROM reservation r
            LEFT JOIN user_info u ON u.u_id = r.r_u_id
            WHERE u.u_name="{}"
        """.format(name)
    else:
        sql = """SELECT r.r_num, u.u_name, r.r_date, r.r_time, r.pet, r.service, r.r_p_id
        FROM reservation r
        LEFT JOIN user_info u ON u.u_id = r.r_u_id
        ORDER BY r.r_num
    """

    return sql


def get_sql_customer():
    cmd = request.args.get('cmd')

    if cmd == 'delete':
        u_id = request.args.get('u_id')
        sql = """DELETE FROM user_info WHERE u_id={}
        """.format(int(u_id))
    elif cmd == 'search':
        name = request.args.get('name')
        sql = """SELECT * FROM user_info WHERE u_name="{}"
        """.format(name)
    else:
        sql = """SELECT * FROM user_info"""

    return sql


def get_sql_staff():
    cmd = request.args.get('cmd')

    if cmd == 'delete':
        p_id = request.args.get('p_id')
        sql = """DELETE FROM pet_sitter WHERE p_id={}
        """.format(int(p_id))
    elif cmd == 'search':
        name = request.args.get('name')
        sql = """SELECT * FROM pet_sitter WHERE p_name="{}"
        """.format(name)
    else:
        sql = """SELECT * FROM pet_sitter"""

    return sql
