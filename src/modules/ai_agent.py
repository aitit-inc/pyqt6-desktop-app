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

# Import app config
from modules.config import config


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

        # Store current configuration values for change detection
        self._current_api_key = None
        self._current_model_name = None

        # Initialize with current settings
        self._update_configuration()

    def _update_configuration(self) -> bool:
        """
        Check and update configuration if settings have changed.

        Returns:
            bool: True if configuration was updated, False otherwise
        """
        # Get current settings from config
        api_key = config.OPEN_AI_API_KEY
        model_name = config.AI_MODEL_NAME

        # Check if settings have changed
        if api_key == self._current_api_key and model_name == self._current_model_name:
            return False  # No changes

        # Store new settings
        self._current_api_key = api_key
        self._current_model_name = model_name

        # Reset model
        self.model = None
        self.agent = None

        if not api_key:
            print(
                "Warning: OPEN_AI_API_KEY is not set in config. AI chat functionality will be limited."
            )
            return True

        try:
            # Initialize the model using config values
            self.model = ChatOpenAI(
                api_key=api_key,
                model=model_name,
                temperature=0.7,
            )

            # Setup LangGraph for conversation management
            self._setup_langgraph()
            return True
        except Exception as e:
            print(f"Error setting up AI agent: {e}")
            self.model = None
            return True

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
        # Check for configuration updates before processing
        self._update_configuration()

        if not self.model:
            return "APIキーが設定されていないため、応答できません。設定画面でAPIキーを設定してください。"

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
