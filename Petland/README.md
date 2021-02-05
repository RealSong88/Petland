# 펫시터 예약 웹사이트 프로젝트 

## **목표**
 * 해당 프로젝트는 DB를 활용한 예약 기능을 통해 펫시터와 반려인의 매칭을 도와주는 것을 목표로 한다.


## **활용언어와 도구**
1. Front : HTML, CSS, Vanila JS, VScode
2. Back : Python(Flask library), MariaDB, DBeaver


## **클래스 name 형식**
 * **BEM 형식**

## **Page 구성**
 * 메인페이지 (서비스 소개 포함)
 * 예약하기
 * 예약확인

### **예약 기능**
1. 고객의 예약 정보를 form에 입력 
2. form.js에서 입력 정보의 유효성을 검사
3. 검사가 완료된 경우, submit하여 펫시터 매칭
4. 지역을 기준으로 매칭되면 결제 페이지로 이동 => 결제하기를 클릭하면 reservation 테이블로 정보를 insert 
5. 매칭이 되지 않은 경우, 매칭 실패 알람을 띄움

### **예약 조회 기능**
1. 예약할 때 입력한 이름과 전화번호를 form에 입력
2. script에서 비어있는 데이터가 없는지 유효성 검사
3. 검사가 완료된 경우, submit하여 reservation 테이블 조회
4. 매칭된 정보가 있으면 select하여 고객에게 보여줌
5. 매칭이 되지 않은 경우, 조회 실패 알람을 띄움

## **DB 활용**
1. Petsitter table
2. Reservation table (FK : r_p_id from petsitter table)

## **Library 활용**
 * Scroll Reveal
 * Font Awesome

## **Developers**
 * (Front) 이종현 이소애
 * (Back) 변해성, 송종천