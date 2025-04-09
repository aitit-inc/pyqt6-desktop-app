"""
AI Agent module for the PyQt6 desktop application.
Provides AI functionality powered by LangGraph and OpenAI.
Handles conversation flow and model interaction.
"""

import os
from typing import List, Dict, Any, Optional

# LangGraph imports
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END


class AIAgent:
    """
    AI Agent class that provides AI functionality using LangGraph and OpenAI.
    Handles conversation flow and model interaction.
    """

    def __init__(self):
        """
        Initialize the AI Agent.
        """
        # Create message queue for chat history
        self.messages = []
        self.model = None
        self.agent = None

        # Check for API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print(
                "Warning: OPENAI_API_KEY environment variable not set. AI chat functionality will be limited."
            )

        try:
            # Initialize the model
            self.model = ChatOpenAI(
                api_key=api_key,
                model="gpt-4o-mini",
                temperature=0.7,
            )

            # Setup LangGraph for conversation management
            self._setup_langgraph()
        except Exception as e:
            print(f"Error setting up AI agent: {e}")
            self.model = None

    def _setup_langgraph(self):
        """Set up LangGraph for conversation flow"""
        # Define state schema
        workflow = StateGraph(MessagesState)

        # Define the model calling function
        def call_model(state):
            messages = state["messages"]
            if not self.model:
                return {
                    "messages": [
                        AIMessage(
                            content="APIキーが設定されていないため、応答できません。"
                        )
                    ]
                }

            response = self.model.invoke(messages)
            return {"messages": [response]}

        # Add nodes and edges
        workflow.add_node("agent", call_model)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)

        # Compile graph
        self.agent = workflow.compile()

    def process_message(self, user_input: str) -> str:
        """
        Process user message and get AI response.

        Args:
            user_input: The user's message

        Returns:
            AI response as a string
        """
        if not self.model:
            return "APIキーが設定されていないため、応答できません。OPENAI_API_KEYを環境変数に設定してください。"

        try:
            # Add user message to history
            self.messages.append(HumanMessage(content=user_input))

            # Get response
            result = self.agent.invoke({"messages": self.messages})

            # Extract response
            ai_message = result["messages"][-1]
            self.messages.append(ai_message)

            return ai_message.content
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return f"エラーが発生しました: {str(e)}"
