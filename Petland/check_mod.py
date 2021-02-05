# 총 6가지의 메서드가 있다
# 데이터베이스 사용 권한이 있는 메서드
# 사용자의 주소와 DB의 펫시터의 주소를 체크하는 메서드
# 사용자가 원하는 날짜에 펫시터가 예약이 가능한지 체크하는 메서드
# 사용자가 처음 서비스 사용자인지 기존 서비스 사용자인지 체크하는 메서드
# 최종 결제하기 클릭시 처음 사용자이면 user_info, reservation 테이블에 사용자 정보와 예약정보를 입력하고, 기존 사용자이면 reservation 테이블에 예약정보를 입력한다.
# 예약정보 조회시 사용자 이름과, 번호를 DB에서 조회하여 세가지 테이블을 조인하여 값을 리턴하는  메서드
import mariadb
import random
import sys


def get_conn():
    conn = mariadb.connect(user="<DB 아이디>",
                           password="<password>",
                           host="<서버 IP>",
                           port=3306,
                           database="Petland")
    return conn


def check_local(search_local):
    # 입력된 지역으로 펫시터가 있는지 체크한다.
    data = []
    sql_local = """
        SELECT p_id FROM pet_sitter WHERE p_local="{}"
    """.format(search_local)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql_local)
        for i in cur:
            data += i
        print(data)
    except mariadb.Error as e:
        print("ERR : {}".format(e))
    finally:
        if conn:
            conn.close()
    # data 를 리스트로 받았기 때문에 db 쿼리시 값이 안나오면 data는 [] 상태가 되서 None이 아니다.
    if len(data) == 0:
        return 0
    else:
        # 랜덤으로 해당 지역 근무자 id를 선택한다.
        choice_data = random.choice(data)
        return choice_data


def check_date(p_id, input_date):
    # 지역 확인 후 날짜를 비교하여 해당 날짜 db쿼리시 None일 때와, 입력 날짜와 다를 시 결제하기 페이지로 넘어간다.
    date = ""
    sql_date = """
                SELECT r_date FROM reservation 
                WHERE r_p_id={} AND r_date="{}" 
            """.format(p_id, input_date)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql_date)
        date = cur.fetchone()
        print(p_id)
    except mariadb.Error as e:
        print("ERR : {}".format(e))
    finally:
        if conn:
            conn.close()

        if date == None:
            return p_id
        else:
            # print()
            # print(date[0])
            # print(date)
            print(type(input_date))
            print(input_date)
            # DB datetime()  타입을 str 타입으로 변경
            date = date[0].isoformat()
            if input_date != date:
                return p_id
            return 0


def check_user(name, phone):
    # info = [name, phone, pet, service, date, time, postcode, roadaddress, detailaddress]
    user = ""
    sql = """
        SELECT u_id, u_name, u_phone FROM user_info 
        WHERE u_name="{}" AND u_phone="{}"
    """.format(name, phone)
    print(sql)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        user = cur.fetchone()
        print(user)
    except mariadb.Error as err:
        print("ERROR: {}".format(err))
    finally:
        if conn:
            conn.close()
        if user == None:
            return 0
        else:
            # user_info의 u_id를 리턴
            u_id = user[0]
            return u_id

# 결제하기 했을 때 예약자의 데이터를 저장


def payment_save(info):
    err = ""
    u_id = ""
    # 예약정보를 리스트형식으로 가지고있다. 최종 결제시 db에 입력
    # info = [name, phone, pet, service, date, time, postcode, roadaddress, detailaddress, p_id]
    print(info)
    # 유저 정보가 없으면 0을 리턴해서 user_info에 예약정보를 insert한다.
    # 유저 정보가 있으면 u_id를 리턴해서 reservation에만 insert한다.
    identify_user = check_user(info[0], info[1])
    full_address = ""
    full_address = info[6] + " " + info[7] + " " + info[8]
    # print(full_address)

    # 유저가 기존에 없는 경우
    if identify_user == 0:
        sql_insert_user = """
            INSERT INTO user_info (u_name, u_phone, u_address) VALUES ("{}", "{}", "{}")
        """.format(info[0], info[1], full_address)
        print(sql_insert_user)

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql_insert_user)
        except mariadb.Error as err:
            print("ERR: {}".format(err))
        finally:
            conn.commit()
            u_id = cur.lastrowid
            print(u_id)
            conn.close()

        sql_insert_reservation = """
            INSERT INTO reservation (r_date, r_time, r_p_id, r_u_id, pet, service)
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}")
        """.format(info[4], info[5], info[9], u_id, info[2], info[3])
        print(sql_insert_reservation)
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql_insert_reservation)
        except mariadb.Error as err:
            print("ERR: {}".format(err))
        finally:
            conn.commit()
            conn.close()
    # 유저가 있는 경우
    else:
        u_id = identify_user
        sql_insert_reservation = """
            INSERT INTO reservation (r_date, r_time, r_p_id, r_u_id, pet, service)
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}")
        """.format(info[4], info[5], info[9], u_id, info[2], info[3])
        print(sql_insert_reservation)
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql_insert_reservation)
        except mariadb.Error as err:
            print("ERR: {}".format(err))
        finally:
            conn.commit()
            conn.close()


def check_phone(user_phone, user_name):
    # 유저번호와 유저이름을 조건으로 검색하여 결과값이 있으면 result에 저장하고 없으면, ""을 리턴한다.
    result = ""
    sql_user_select = """
        SELECT u.u_id, u.u_name, u.u_phone, r.pet, r.service,
        r.r_date, r.r_time, p.p_name 
        FROM user_info u
        LEFT JOIN reservation r ON u.u_id = r.r_u_id
        LEFT JOIN pet_sitter p ON p.p_id = r.r_p_id 
        WHERE u.u_phone = "{}" AND u.u_name ="{}"
    """.format(user_phone, user_name)
    print(sql_user_select)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql_user_select)
        for u_id, u_name, u_phone, pet, service, r_date, r_time, p_name in cur:
            result += "<tr>"
            result += "<td>"+str(u_id)+"</td>"
            result += "<td>"+u_name+"</td>"
            result += "<td>"+u_phone+"</td>"
            result += "<td>"+pet+"</td>"
            result += "<td>"+service+"</td>"
            result += "<td>"+str(r_date)+"</td>"
            result += "<td>"+r_time+"</td>"
            result += "<td>"+p_name+"</td>"
            result += "</tr>"
        print(result)
        print()
        print(type(result))
    except mariadb.Error as e:
        print("ERR : {}".format(e))
    finally:
        if conn:
            conn.close()
    return result
