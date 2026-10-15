"""LangGraph example (OpenAI ChatGPT version).

Adapted from: https://ai.google.dev/gemini-api/docs/langgraph-example?hl=ko
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Annotated, Sequence, TypedDict

import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages  # helper function to add messages to the state
from pydantic import BaseModel, Field

# Load the workspace-root .env (small_steps/.env) and read the API key from it
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")
api_key = os.getenv("OPENAI_API_KEY")


# ---------------------------------------------------------------------------
# Define the agent state
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    """The state of the agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int


# ---------------------------------------------------------------------------
# Define the weather tool
# ---------------------------------------------------------------------------
geolocator = Nominatim(user_agent="weather-app")


class SearchInput(BaseModel):
    location: str = Field(description="The city and state, e.g., San Francisco")
    date: str = Field(description="the forecasting date for when to get the weather format (yyyy-mm-dd)")


@tool("get_weather_forecast", args_schema=SearchInput, return_direct=True)
def get_weather_forecast(location: str, date: str):
    """Retrieves the weather using Open-Meteo API.

    Takes a given location (city) and a date (yyyy-mm-dd).

    Returns:
        A dict with the time and temperature for each hour.
    """
    # Note that Colab may experience rate limiting on this service. If this
    # happens, use a machine to which you have exclusive access.
    location = geolocator.geocode(location)
    if location:
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}"
            )
            data = response.json()
            return dict(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}


tools = [get_weather_forecast]

# ---------------------------------------------------------------------------
# Initialize the model and bind tools
# ---------------------------------------------------------------------------
# Create LLM class
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=1.0,
    max_retries=2,
    api_key=api_key,
)

# Bind tools to the model
model = llm.bind_tools([get_weather_forecast])

# Test the model with tools
res = model.invoke(f"What is the weather in Berlin on {datetime.today()}?")

print(res)

# ---------------------------------------------------------------------------
# Define nodes and the conditional edge
# ---------------------------------------------------------------------------
tools_by_name = {tool.name: tool for tool in tools}


# Define our tool node
def call_tool(state: AgentState):
    outputs = []
    # Iterate over the tool calls in the last message
    for tool_call in state["messages"][-1].tool_calls:
        # Get the tool by name
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                # OpenAI requires tool message content to be a string
                content=json.dumps(tool_result, ensure_ascii=False),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


def call_model(
    state: AgentState,
    config: RunnableConfig,
):
    # Invoke the model with the system prompt and the messages
    response = model.invoke(state["messages"], config)
    # This returns a list, which combines with the existing messages state
    # using the add_messages reducer.
    return {"messages": [response]}


# Define the conditional edge that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    # If the last message is not a tool call, then finish
    if not messages[-1].tool_calls:
        return "end"
    # default to continue
    return "continue"


# ---------------------------------------------------------------------------
# Assemble the graph
# ---------------------------------------------------------------------------
# Define a new graph with our state
workflow = StateGraph(AgentState)

# 1. Add the nodes
workflow.add_node("llm", call_model)
workflow.add_node("tools", call_tool)
# 2. Set the entrypoint as `agent`, this is the first node called
workflow.set_entry_point("llm")
# 3. Add a conditional edge after the `llm` node is called.
workflow.add_conditional_edges(
    # Edge is used after the `llm` node is called.
    "llm",
    # The function that will determine which node is called next.
    should_continue,
    # Mapping for where to go next, keys are strings from the function return,
    # and the values are other nodes.
    # END is a special node marking that the graph is finish.
    {
        # If `tools`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": END,
    },
)
# 4. Add a normal edge after `tools` is called, `llm` node is called next.
workflow.add_edge("tools", "llm")

# Now we can compile and visualize our graph
graph = workflow.compile()

# ---------------------------------------------------------------------------
# Visualize the graph (works in a notebook; in a script it only builds the image)
# # ---------------------------------------------------------------------------
# from IPython.display import Image, display  # noqa: E402

# display(Image(graph.get_graph().draw_mermaid_png()))

# ---------------------------------------------------------------------------
# Run the agent
# ---------------------------------------------------------------------------
# Create our initial message dictionary
inputs = {"messages": [("user", f"What is the weather in Berlin on {datetime.today()}?")]}

# call our graph with streaming to see the steps
for state in graph.stream(inputs, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()

# ================================ Human Message =================================

# What is the weather in Berlin on 2026-10-15 13:32:39  .986553?
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather_forecast (call_k7lv9TecLtMTmBu4Xl1uLkgN)
#  Call ID: call_k7lv9TecLtMTmBu4Xl1uLkgN
#   Args:
#     location: Berlin
#     date: 2026-10-15
# ================================= Tool Message =================================
# Name: get_weather_forecast

# {"2026-10-15T00:00": 8.5, "2026-10-15T01:00": 8.0, "2026-10-15T02:00": 7.3, "2026-10-15T03:00": 6.9, "2026-10-15T04:00": 6.7, "2026-10-15T05:00": 6.5, "2026-10-15T06:00": 6.4, "2026-10-15T07:00": 6.8, "2026-10-15T08:00": 8.1, "2026-10-15T09:00": 9.9, "2026-10-15T10:00": 11.8, "2026-10-15T11:00": 13.5, "2026-10-15T12:00": 14.6, "2026-10-15T13:00": 15.4, "2026-10-15T14:00": 15.8, "2026-10-15T15:00": 15.8, "2026-10-15T16:00": 15.2, "2026-10-15T17:00": 14.2, "2026-10-15T18:00": 13.2, "2026-10-15T19:00": 12.5, "2026-10-15T20:00": 11.7, "2026-10-15T21:00": 11.2, "2026-10-15T22:00": 10.6, "2026-10-15T23:00": 10.1}
# ================================== Ai Message ==================================

# On October 15, 2026, at 13:00, the temperature in Berlin is expected to be 15.4°C. If you need the specific weather around the time you mentioned (13:32), it would be similar to this temperature.

# ---------------------------------------------------------------------------
# Continue the conversation
# ---------------------------------------------------------------------------
state["messages"].append(("user", "Would it be warmer in Munich?"))

for state in graph.stream(state, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()
    
# ================================ Human Message =================================

# Would it be warmer in Munich?
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather_forecast (call_bNFOxivyCLvuJTV8fXypF4kB)
#  Call ID: call_bNFOxivyCLvuJTV8fXypF4kB
#   Args:
#     location: Munich
#     date: 2026-10-15
# ================================= Tool Message =================================
# Name: get_weather_forecast

# {"2026-10-15T00:00": 8.7, "2026-10-15T01:00": 8.6, "2026-10-15T02:00": 8.9, "2026-10-15T03:00": 7.8, "2026-10-15T04:00": 7.7, "2026-10-15T05:00": 7.4, "2026-10-15T06:00": 7.7, "2026-10-15T07:00": 8.2, "2026-10-15T08:00": 8.9, "2026-10-15T09:00": 10.2, "2026-10-15T10:00": 12.5, "2026-10-15T11:00": 14.3, "2026-10-15T12:00": 15.1, "2026-10-15T13:00": 16.4, "2026-10-15T14:00": 16.8, "2026-10-15T15:00": 17.0, "2026-10-15T16:00": 16.7, "2026-10-15T17:00": 15.0, "2026-10-15T18:00": 13.2, "2026-10-15T19:00": 12.0, "2026-10-15T20:00": 10.8, "2026-10-15T21:00": 9.5, "2026-10-15T22:00": 9.3, "2026-10-15T23:00": 8.7}
# ================================== Ai Message ==================================

# On October 15, 2026, at 13:00, the temperature in Munich is expected to be 16.4°C, which is warmer than the 15.4°C forecasted for Berlin at the same time.
