### 경제뉴스 조회 및 용어설명
#### 1. tools 준비
- ~~뉴스검색: 네이버 뉴스 검색 API~~
- ~~뉴스 내 용어: 네이버 백과사전 API~~

#### 2. Agent, Agent Executor 사용
- ~~뉴스 전체 내용이 아닌 뉴스 제목으로만 용어검색 진행~~
-> ~~stream()이용하여 터미널에 출력하면서 AgentExecutor 실행완료~~
- chat history 넣어서 대화내역 반영하기 ([공식문서 Adding in-Memory](https://python.langchain.com/docs/tutorials/agents/#adding-in-memory) 참고)

#### 번외
- 기능추가: 중요한 경제뉴스를 골라 검색어로 만든 후 검색
- 고도화: 경제뉴스 내 다양한 용어를 추출