from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv, dotenv_values 

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from app.service.Expense import Expense
import os

class LLMService:
    def __init__(self):
        load_dotenv()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                ("human", "{text}"),
            ]
        )
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=self.api_key,
            temperature=0.3,
        )
        self.runnable = self.prompt | self.llm.with_structured_output(schema=Expense)

    def runLLM(self, message):
        return self.runnable.invoke({"text":  message})
 