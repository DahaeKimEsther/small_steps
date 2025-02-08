from typing_extensions import TypedDict
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.prebuilt import tools_condition

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class LangGraphTutorial:
    tools:list = list()

    #Edges
    def grade_documents(self, state) -> Literal["generate", "rewrite"]:
        
        class grade(BaseModel):
            binary_score: str = Field(description="Relevance score 'yes' or 'no'")
            
        model = ChatOpenAI(temperature=0, model='gpt-4o')
        
        llm_with_tool = model.with_structured_output(grade)
        
        prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
        )
        
        chain = prompt | llm_with_tool
        
        messages = state["messages"]
        last_message = messages[-1]
        
        question = messages[0].content
        docs = last_message.content
        
        scored_result = chain.invoke({'question': question, 'context': docs})
        
        score = scored_result.binary_score
        
        if score=='yes':
            print("---DECISION: DOCS RELEVANT---")
            return "generate"
        else:
            print("---DECISION: DOCS NOT RELEVANT---")
            print(score)
            return "rewrite"
        
    def agent(self, state):
        """
        Invokes the agent model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the retriever tool, or simply end.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the agent response appended to messages
        """
        print("---CALL AGENT---")
        messages = state["messages"]
        model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
        model = model.bind_tools(self.tools)
        response = model.invoke(messages)
        return {"messages": [response]}
    
    def rewrite(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        print("---TRANSFORM QUERY---")
        messages = state["messages"]
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
        Look at the input and try to reason about the underlying semantic intent / meaning. \n 
        Here is the initial question:
        \n ------- \n
        {question} 
        \n ------- \n
        Formulate an improved question: """,
            )
        ]

        # Grader
        model = ChatOpenAI(temperature=0, model="gpt-4o")
        response = model.invoke(msg)
        return {"messages": [response]}
