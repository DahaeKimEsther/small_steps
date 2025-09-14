from langchain.chat_models import init_chat_model
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from rich import print
from rich.pretty import Pretty
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt


memory = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}

#local
from tools import tools
from utils import LoggingTool
logger = LoggingTool.get_logger(__name__)

llm = init_chat_model('openai:gpt-4.1')
llm_with_tools = llm.bind_tools(tools) 

class State(TypedDict):
    messages:Annotated[list, add_messages]

def chatbot(state:State):
    return {'messages': [llm_with_tools.invoke(state['messages'])]}

import json

from langchain_core.messages import ToolMessage

# class BasicToolNode: # from langgraph.prebuilt import ToolNode로 대체가능
#     """A node that runs the tools requested in the last AIMessage"""
    
#     def __init__(self, tools:list) -> None:
#         self.tools_by_name = {tool.name: tool for tool in tools}
    
#     def __call__(self, inputs:dict):
#         if messages := inputs.get("messages", []):
#             messages = messages[-1]
#         else:
#             raise ValueError("No message found in input")
        
#         outputs = []
#         for tool_call in messages.tool_calls:
#             tool_result = self.tools_by_name[tool_call['name']].invoke(
#                 tool_call['args']
#             ) # LLM이 사용할 tool을 추론하면 그 tool을 호출해서, 호출한 tool에 LLM이 추론한 args값을 넣어주기
#             outputs.append(
#                 ToolMessage(
#                     content=json.dumps(tool_result),
#                     name=tool_call['name'],
#                     tool_call_id=tool_call['id']
#                 )
#             )
        
#         return {'messages': outputs}
# tool_node = BasicToolNode(tools=tools)
tool_node = ToolNode(tools=tools)

# def route_tools(state:State): # from langgraph.prebuilt import tools_condition 으로 대체가능
    
#     # ai message 확보
#     if isinstance(state, list):
#         # logger.debug(f"state (list): {state}")
#         ai_message = state[-1]
#     elif messages := state.get("messages", []):
#         # logger.debug(f"state (dict): {state}")
#         ai_message = messages[-1]
#     else:
#         raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
#     # tools 노드 이동
#     if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
#         return "tools"
#     return END

# nodes
graph_builder = StateGraph(State)
graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('tool_execute', tool_node)

# edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition, 
                                    {"tools": "tool_execute", END: END})
# path_map: tell the graph to interpret the condition's outputs as a specific node
# ex) {"node_name_from_route_tools":"node_name_exists"}; defaults to identity func
graph_builder.add_edge("tool_execute", "chatbot") # tool_execute의 결과를 chatbot으로 보내기

graph = graph_builder.compile(checkpointer=memory)

if __name__ == "__main__":
    
    # # visualizaton
    # from IPython.display import Image, display
    # try:
    #     display(Image(graph.get_graph().draw_mermaid_png()))
    # except Exception:
    #     # This requires some extra dependencies and is optional
    #     pass
    def stream_graph_updates(user_input: str):
        resumable = False
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config, # 3. add memory
            stream_mode="updates",
            ):
            
            # # 5. add human-inthe-loop이해하기 - stream_mode = "updates"로 변경
            print(Pretty(event))
            
            # # 2. add tools
            # for value in event.values():
            #     print("Assistant:", value["messages"][-1].content)
            
            # 3. add memory, 5. add human-inthe-loop - stream_mode = "updates"로 변경
            resumable = event["__interrupt__"][0].resumable if "__interrupt__" in event else False
            event["chatbot"]["messages"][-1].pretty_print()
        return resumable
            
    def stream_resume_execution(human_response:str, config:dict):
        human_command = Command(resume={"data": tuple(human_response)})
        resumable = False
        for event in graph.stream(human_command, config, stream_mode="updates"):
            # interrupt로 끊겼던 그래프 재실행
            resumable = event["__interrupt__"][0].resumable if "__interrupt__" in event else False
            event["chatbot"]["messages"][-1].pretty_print()
        return resumable
        
            


    # 2. add tools
    resumable = False
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]: # user_input으로 대화종료
            print("Goodbye!")
            # 3. add memory - inspect the state
            snapshot = graph.get_state(config)
            print(f"snapshot: {snapshot}")
        else: # user_input으로 대화지속
            if resumable:
                human_response = user_input
                resumable = stream_resume_execution(human_response)
            else:
                # (중요)config, InMemorySaver가 있어서 stream_resume_execution에서 interrupt로 중단된 graph을 이어서 실행가능
                resumable = stream_graph_updates(user_input)
            
            # for i, snapshot in enumerate(graph.get_state_history(config), start=1):
            #     """역순으로 출력되므로 아래에서부터 보면 됨"""
            #     print(f"\n=== Step {i} ===")
            #     print(Pretty(snapshot))
            
# questions:
# I need some expert guidance for building an AI agent. Could you request assistance for me?
# We, the experts are here to help! We'd recommend you check out LangGraph to build your agent. It's much more reliable and extensible than simple autonomous agents.