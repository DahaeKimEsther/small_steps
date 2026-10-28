# gemini-langgraph-basic
* 출처: [Gemini 및 LangGraph를 사용하여 처음부터 ReAct 에이전트 만들기](https://ai.google.dev/gemini-api/docs/langgraph-example?hl=ko)
* 주의: 이 레포지토리의 연습코드에서는 gemini api 대신에 openai api를 사용하였습니다.

## 가상환경(.venv) 만들기

`.venv` 폴더는 git에 포함하지 않으므로, 필요할 때 아래 순서로 다시 만듭니다.

1. conda의 `uv` 가상환경(uv 라이브러리가 설치된 환경)을 활성화합니다.

   ```powershell
   conda activate uv
   ```

2. 프로젝트 폴더로 이동합니다.

   ```powershell
   cd C:\Users\holla\workspaces\projects\small_steps\original_source\261015_agent_architecture\261015_gemini_langgrpah_basic
   ```

3. `uv sync`를 실행하면 `pyproject.toml`과 `uv.lock`에 맞춰 `.venv`가 생성되고 라이브러리가 설치됩니다.

   ```powershell
   uv sync
   ```

## 실행

```powershell
uv run python langgraph_example.py
```
