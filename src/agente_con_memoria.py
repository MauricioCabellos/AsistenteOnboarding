#Herramientas Personalizadas
#Intro a Memoria

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.prompts import(ChatPromptTemplate, MessagesPlaceholder)
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import(AgentExecutor, create_tool_calling_agent)

load_dotenv()