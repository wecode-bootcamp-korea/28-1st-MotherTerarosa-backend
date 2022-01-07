# MotherTerarosa

## oo 프로젝트 Front-end/Back-end 소개

- 순수 국내 커피 체인점인 [테라로사](https://terarosa.com/) 클론 프로젝트
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은 모두 직접 개발한 백앤드와 연결하여
실제 서비스 수준으로 개발한 것입니다.

### 개발 인원 및 기간

- 개발기간 : 2021/12/27 ~ 2022/01/07
- 개발 인원 : 프론트엔드 3명, 백엔드 3명
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/28-westagram-backend-4-team)

### 데모 영상(이미지 클릭)

- [데모 영상](https://wecode-bootcamp.slack.com/files/U02HVJ9LFGW/F02TF34RZQ9/motherterarosa_frontend.mov)

<br>

## 적용 기술 및 구현 기능

### 적용 기술

> - Back-End :
>>  - Python
>>  - Django web framework
>>  - Bcrypt
>>  - MySQL
>>  - JWT
> - Common :
>>  - RESTful API
>>  - httpie

### 협업 도구

> - github
> - slack 
> - notion
> - trello
> - figma

### 구현 기능

#### 공통

- User flow
[개인이 이미지 다시 처리](https://www.notion.so/613177d6b2fb41378ff4789af33e2575#0cc54341de5f48c4aa3e1049fb9544ae)
- ERD
[개인이 이미지 다시 처리](https://www.notion.so/613177d6b2fb41378ff4789af33e2575#d278ed5703b04c9cb4a920357c2cbae3)

### 프로젝트 아키텍쳐 소개

#### 메인

1. create_at의 정보를 활용하여 신상품 구현
2. product_hits를 역순으로 호출하여 베스트(최다초회수 순서) 상품 구현

#### 회원가입

1. username, password, email 유효성 검사 (정규표현식 활용)
2. username, email 중복 검사 (exists() method 활용)
3. password 암호화 적용 (bcrypt 패키지 활용) 

#### 로그인

1. 암호화 되어 DB에 저장된 password와 로그인 시 유저가 입력한 password 값 매칭 검사
(bcrypt 패키지의 checkpw() 활용)
2. 로그인 성공시 유효시간이 설정된 token 발급 (PyJWT 패키지 활용)
3. 장바구니, 결제 등 로그인이 필요한 부분에서 유저의 권한 확인를 위한 decorator 작성

#### 상품 리스트

1. 제품 Category list를 호출해서 리턴 (Category list 별도 Request)
2. Request의 Query parameter에 따라 선택된 카테고리의 상품 리스트 조회
3. 가독성이 떨어지는 로직은 함수화하여 별도 처리, 관리

#### 상품 디테일

1. 역참조를 활용하여  data 호출

#### 결제

1. access token을 통한 유저 확인 후, 토큰의 user id값으로 유저정보를 호출
2. FE의 request를 받아서 db에 저장 후 User 정보를 response 한다.
3. 잔액부족과 except를 이용한 예외처리

<br>

## Reference

- 이 프로젝트는 [테라로사](https://terarosa.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.