## 1. 문서정리
### Coroutines
[PEP492 - Coroutines with async and await syntax](https://peps.python.org/pep-0492/)  
It is proposed to make **coroutines** a proper standalone concept in Python, and introduce new supporting syntax. **The ultimate goal is to help establish a common, easily approachable, mental model of asynchronous programming in Python and make it as close to synchronous programming as possible.**  
  
[coroutine](https://docs.python.org/3/glossary.html#term-coroutine): Coroutines are a more generalized form of subroutines. Subroutines are entered at one point and exited at another point. **Coroutines can be entered, exited, and resumed at many different points.** They can be implemented with the async def statement. See also PEP 492.

### [coroutine function - scheme of async def](https://docs.python.org/3/glossary.html#term-coroutine-function)  
* A function which returns a coroutine object. A coroutine function may be **defined with the async def statement, and may contain await, async for, and async with keywords.** These were introduced by PEP 492.  
* await (expression): **Suspend the execution of coroutine on an awaitable object.** Can only be used inside a coroutine function.
* awaitable object: [object with await() method](https://docs.python.org/3/reference/datamodel.html#object.__await__).

### [Coroutines by asyncio](https://docs.python.org/3/library/asyncio-task.html)
* Read '250527_async_await.py' first
* `asyncio.run()`: function to run the top-level entry point
* `asyncio.create_task()`: asyncio.run() runs all coroutines cocurrently. coroutines are,for example, tasks created by create_task() 
* `asyncio.TaskGroup()`: An asynchronous context manager holding a group of tasks. Tasks can be added to the group using create_task(). **All tasks are awaited when the context manager exits**
* `async with` in `asyncio.TaskGroup()`: According to the explanation in [TaskGroup](https://docs.python.org/3/library/asyncio-task.html#task-groups), **The async with statement will wait for all tasks in the group to finish.** While waiting, new tasks may still be added to the group. Once the last task has finished and the async with block is exited, no new tasks may be added to the group.  

* `async with statement`: "async" with statement.  
a. [with statement](https://docs.python.org/ko/3/reference/compound_stmts.html#the-with-statement): with문. with문 내 코드의 실행이 컨텍스트 관리자의 메서드들(enter(),exit()) 로 이뤄짐.  
b. [컨텍스트 관리자](https://docs.python.org/ko/3/reference/datamodel.html#context-managers): 컨텍스트로의 진입과 탈출을 처리.  
ex) global state의 보관 및 복구, 자원의 lock/unlock, *열린 파일을 닫기 (with open() as f:)*  
c. [비동기 컨텍스트 관리자](https://docs.python.org/ko/3/reference/datamodel.html#object.__aenter__): 컨텍스트 관리자로, aenter()와 aexit() 메서드를 이용하여 실행을 일시중지할 수 있음  
d. [aenter(), aexit()으로 구현한 async with문](https://docs.python.org/ko/3/reference/compound_stmts.html#the-async-with-statement)

## 2. 문서정리 사유
### Q. async with문은 왜 async def 안에 있어야 할까?
`250604_mcp_tutorials\250604_mcp_client.py`을 langchain-mcp-adapters에 있는 코드 그대로 실행했을 때 `SyntaxError: 'async with' outside async function`, 이런 에러가 났다. async with문을 async def 함수 안에 넣어준 후, async def 함수를 실행했더니 위 에러가 해결되었다.

###  async with 공식문서를 통한 이해
[async with 공식문서 링크](https://docs.python.org/ko/3/reference/compound_stmts.html#the-async-with-statement)

#### 1. 공식문서에도 SyntaxError가 언급되어있다.
`코루틴 함수의 바디 밖에서 async with 문을 사용하는 것은 SyntaxError 입니다.`

#### 2. 이 문서를 이해하려면 아래 내용을 더 알아야 할 것 같다.
- 코루틴 함수, 비동기 컨텍스트 관리자
- aenter(), aexit()

#### 3. async with TaskGroup()의 정황:
- `250604_mcp_tutorials\250604_mcp_client.py`에서 `async with stdio_client`의 'stdio_client'를 소스를 보면 task group을 정의하는 부분이 나온다. 그렇기에 `async with stdio_client~`로 코드를 짤 수 있는 것이 아닐까.. 