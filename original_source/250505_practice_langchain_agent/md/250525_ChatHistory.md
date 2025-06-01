## 1. RunnableWithMessageHistory
출처:  
[API reference - RunnableWithMessageHistory](https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html#runnablewithmessagehistory)

### definition:  
Runnable that manages chat message history  

### features:
- Wraps another Runnable
- Manage(read and update) chat history
- Expected to take "sessoin_id" as a single configuration parameter:  
`chain.invoke(…, config={“configurable”: {“session_id”: “bar”}})`

### parameters:
- **runnable**: The base Runnable to be wrapped. Must take as input one of: 1. A sequence of BaseMessages 2. A dict with one key for all messages 3. A dict with one key for the current input string/message(s) and a separate key for historical messages. <u>If the input key points to a string, it will be treated as a HumanMessage in history.</u>
```python
# example of input - case 3.
chain.invoke({"input": "난 경제를 잘 알고 싶어."})
```

- **get_session_history**: Function that returns a new BaseChatMessageHistory
```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
store = dict()

def get_by_session_history(session_id: str)-> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id] # -> BaseChatMessageHistory
```