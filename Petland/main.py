from flask import Flask, render_template, request
from check_mod import check_local, check_date, check_phone, payment_save
import mariadb
import sys

app = Flask(__name__)
# 예약자 정보를 결제하기까지 저장하기위해 전역변수 사용
# 지역구 매칭 성공시 p_id 까지 저장
user_info = []


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/reservation")
def reservation():
    return render_template("reservation.html")


@app.route("/reservation", methods=['POST'])
def receive_form():
    name = request.form['name']
    phone = request.form['phone']
    pet = request.form['pet']
    # 세가지를 중복으로 선택할수있기 때문에 getlist로 받음
    service = request.form.getlist('service')
    date = request.form['date']
    time = request.form.getlist('time')  # 위 상황과 동일
    postcode = request.form['postcode']
    roadaddress = request.form['roadaddress']
    detailaddress = request.form['detailaddress']

    # 세가지를 모두 선택할 수 있기 때문에 value 구분을 위하여 한가지 선택할 경우 제외하고 ',' 추가
    if len(service) > 1:
        service = ",".join(service)
    else:
        service = service[0]
    # 위와 동일
    if len(time) > 1:
        time = ",".join(time)
    else:
        time = time[0]

    formData = []
    formData.append(name)  # [0]
    formData.append(phone)  # [1]
    formData.append(pet)  # [2]
    formData.append(service)  # [3]
    formData.append(date)  # [4]
    formData.append(time)  # [5]
    formData.append(postcode)  # [6]
    formData.append(roadaddress)  # [7]
    formData.append(detailaddress)  # [8]

    global user_info
    user_info = formData
    print(user_info)
    # 지역(구)와 data를 먼저 빼와서 DB와 비교
    str_addr = user_info[7].split(" ")[1]
    print(str_addr)

    # 1.해당 지역에 펫시터 있을시 검증 근무자 없을 시 펫시터 없음 전달, 있으면 다음단계
    # 2. 1번 검증 완료시 p_id와 유저가 입력한 날짜로 db 날짜 중복 검증
    p_id = check_local(str_addr)
    if p_id == 0:
        err = "해당 지역에 펫시터가 예약이 마감되었습니다.."
        return render_template("reservation.html", err=err)
    else:
        possible_sitter = check_date(p_id, user_info[4])
        if possible_sitter == 0:
            err = "해당 날짜에 펫시터는 예약이 마감되었습니다."
            return render_template("reservation.html", err=err)
        else:
            # 명확하게 html 태그의 변수들을 구분하기위해 reservation_info를 사용하지않고 각각의 변수에 저장한 데이터를 사용한다.
            user_info.append(possible_sitter)
            print(user_info)
            return render_template("reservation2.html",
                                   name=name, pet=pet,
                                   service=service, date=date,
                                   time=time)


@app.route("/reservation2", methods=['POST'])
# 결제하기 작동시 /reservation2로 form을 보내고, db에 데이터를 입력하고, reservation.html 로 이동
def reservation2():
    payment_save(user_info)
    # reservation_info = ""
    return render_template("reservation_check.html")


@app.route("/reservation_check")
def reservation_check():
    return render_template("reservation_check.html")


@app.route("/reservation_check", methods=['POST'])
def check_submit():
    name = request.form['name']
    phone = request.form['phone']
    user_info = check_phone(phone, name)
    if len(user_info) == 0:
        err = "예약정보가 없습니다."
        return render_template("reservation_check.html", err=err)
    else:
        # print(user_info)
        return render_template("reservation_check2.html", content=user_info)


@app.route("/intro")
def intro():
    return render_template("introduce.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
