"""
Ollama implementation of OrchaelChatProcessor
"""

import os
from typing import List
from orchael_sdk import OrchaelChatProcessor, ChatInput, ChatOutput, ChatHistoryEntry
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama


class OllamaChatProcessor(OrchaelChatProcessor):
    """Ollama chat processor that asks questions of ollama"""

    def __init__(self) -> None:
        self._history: List[ChatHistoryEntry] = []

        # Get configuration from environment variables
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama2")
        self.ollama_temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))

        # Initialize Ollama chat model
        self.ollama = ChatOllama(
            base_url=self.ollama_url,
            model=self.ollama_model,
            temperature=self.ollama_temperature,
        )

        # Create a simple prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant. Answer questions clearly and concisely.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        # Create the chain
        self.chain = self.prompt | self.ollama

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        # Convert history to LangChain message format
        messages = []
        if chat_input.get("history"):
            for entry in chat_input["history"]:
                messages.append(HumanMessage(content=entry["input"]))
                messages.append(AIMessage(content=entry["output"]))

        # Add current question
        messages.append(HumanMessage(content=chat_input["input"]))

        # Get response from the model
        ai_response = self.chain.invoke(
            {"history": messages[:-1], "input": chat_input["input"]}
        )
        answer = getattr(ai_response, "content", str(ai_response))

        # Create output
        output = ChatOutput(input=chat_input["input"], output=answer)

        # Add to history
        self._history.append({"input": chat_input["input"], "output": answer})

        return output

    def get_history(self) -> List[ChatHistoryEntry]:
        """Return the chat history as an array of ChatHistoryEntry"""
        return self._history
