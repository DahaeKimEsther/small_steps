* 출처: [파이썬 공식문서 - 로깅 HOWTO](https://docs.python.org/ko/3.13/howto/logging.html#advanced-logging-tutorial)

### 고급 로깅 자습서

로거: Logger 클래스의 인스턴스 사용
- 계층구조 존재, 루트로거: 로거 계층의 뿌리
- 모듈 수준의 로거를 사용하는 것을 권장
```
logger = logging.getLogger(__name__)
```

처리기: 로그 레코드를 적절한 목적지로 보냄
- Logger.addHanlder(): 로거에 처리기 할당
