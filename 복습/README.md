# FastAPI 복습 - 공식 튜토리얼로 다시 해보는 FastAPI 핵심

## 실습 순서

| 단계 | 내용 |
|---|---|
| 1. SQL_Database | User + Item 두 테이블, 1:N 관리, crud.py 분리 |
| 2. bigger_applications | routers / 폴더 분리 구조 |
| 3. app_testing | TestClient로 엔드포인트 자동 테스트 - pytest |

## 실습 환경
- python 3.11
- 패키지 관리 : `uv`
- DB : PostgreSQL 17
    - DB name : `reviewdb`
- IDE : VS Code
- 터미널 : Git Bash

## 1. SQL_Database --> User + Item, 1:N 관계 crud
- 공식 FastAPI 튜토리얼 예제를 PostgreSQL로 변환한 버전이다.
- `User` (사용자)가 여러 개의 `Item`(아이템)을 소유하는 **1:N 관계** 구조
- `crud.py`를 별도로 분리하여 DB 조작 로직과 라우터 로직을 나눈다.