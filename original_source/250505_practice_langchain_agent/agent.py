from tool_utils import naver_news, naver_dict
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv('./projects/.env')

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 'You are a helpful assistant'),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}") # MUST

    ]
)
model = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [naver_news, naver_dict]
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

for step in agent_executor.stream({"input": "'기준금리'에 대해 뉴스를 검색해주고, 경제용어에 대해 사전에서 검색해줘 그리고 설명해줘. 중복되는 경제 용어는 설명하지 않아도 돼."},
):
    step["messages"][-1].pretty_print()