# documents

## 실행방법

1 도커 이미지 생성

```
docker built -t fastapi:local -f Dockerfile.yaml .
```

2 docker compose up

```
cd Docker
docker compose up
```

3 run sql scripts
- sql.sql for production
- sql_testdb.sql for testdb

4 서비스 
service: localhost:8000
docs: localhost:8000/docs

## 디렉터리 구조  

```
├── dao
│   ├── product.py
│   ├── token.py
│   └── user.py
├── db
│   └── db.py
├── exceptions                # 예외들       
│   ├── exceptions.py
│   ├── no_content.py
│   ├── unauthorized.py
│   ├── unprocessable_content.py
│   ├── user_exists.py
│   ├── user_not_exists.py
│   └── user_passwords.py
├── main.py                     # API 서버 엔트리포인트
├── models                      #
│   ├── product_dto.py
│   ├── response
│   │   └── token_response.py
│   ├── response_dto.py
│   ├── token_dto.py
│   └── user_dto.py
├── repository                   # repository
│   ├── product.py
│   ├── repo.py
│   ├── token.py
│   └── user.py
├── routers                      # router
│   ├── auth_router.py
│   └── product_router.py
├── service                      # 서비스 
│   ├── auth_service.py
│   └── product_service.py
├── settings.yaml                # 환경변수
├── test                         # 테스트 폴더 
│   ├── service
│   │   ├── test_auth_service.py
│   │   └── test_product_service.py
│   └── utils
│       └── logger
│           └── test_logger.py
└── utils                        # 유틸함수 
    ├── korean
    │   └── korean.py
    ├── logger
    │   └── logger.py
    ├── time.py
    └── yaml
        └── settings.py
```
