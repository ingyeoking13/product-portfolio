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