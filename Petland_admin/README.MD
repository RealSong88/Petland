# Petland 관리자페이지 API

## **활용언어와 도구**

1. Front : HTML, CSS, Vanila JS, VScode
2. Back : Python(Flask library), MariaDB, DBeaver

## **클래스 name 형식**

- **BEM 형식**

## **Page 구성**

- 관리자 로그인 페이지
- 예약 관리 페이지
- 고객 관리 페이지
- 펫시터 관리 페이지

### **관리자 기능**

1. 로그인 기능
2. 예약정보를 삭제하고 고객 검색
3. 고객정보를 삭제하고 고객 검색
4. 펫시터정보를 삭제하고 펫시터 검색

## **DB 활용**

1. admin table
2. pet_sitter table
3. user_info table
4. reservation table (FK : r_p_id from pet_sitter table,
   r_u_id from user_info table)

## **보안할 점**

- 예약현황과 해당 펫시터의 예약 건수 등을 통계로 메인 페이지를 뿌리는게 관리자 페이지 취지에 맞다.
- 삭제 및 검색 기능만 넣어서 실제 관리자가 제어할 수 있는 방법이 많지않다.
- 예약 테이블에 서비스 대기상태와 완료상태를 구분 할 수가 없어서 문제점이 발생한다.
- reservation 테이블에서 p_id, 와 u_id 를 참조하는데 펫시터나 고객테이블에서 수정할 일이 생길 때 reservation에서 예약이 되어있을 시에는 수정을 할 수 없게 restrict로 걸어두었다. (set null설정시 예약관리 페이지에 null 값이 들어가 쿼리시 에러발생.)

## **Developers**

- (Front) 이종현 이소애
- (Back) 변해성, 송종천
