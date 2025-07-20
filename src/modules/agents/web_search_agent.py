from datetime import datetime, timedelta
from textwrap import dedent

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables.config import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

from src.modules.agents.base_agent import BaseAgent
from src.modules.schemas.question_generator_schema import QuestionGeneratorState


class WebSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()  # Ensure BaseAgent is initialized

        self._tool = TavilySearch(
            max_results=3,
            start_date=(datetime.now() - timedelta(days=1 * 365)).date(),
        )

    def _get_prompt(self) -> ChatPromptTemplate:
        human_prompt = dedent(
            """
            Search about {options} in the context of {context}
            """,
        )
        return ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template(human_prompt),
            ],
        )

    async def node(self, state: QuestionGeneratorState, config: RunnableConfig) -> QuestionGeneratorState:
        """Web search agent node.

        Args:
            state (QuestionGeneratorState): The state of the agent.
            config (RunnableConfig): The configuration of the agent.

        Returns:
            QuestionGeneratorState: The state of the agent.
        """
        context = state["context"]
        options = state["options"]

        agent = create_react_agent(model=self.get_llm(), tools=[self._tool])

        prompt = await self._get_prompt().ainvoke(
            {
                "context": context,
                "options": ", ".join(options),
            },
            config
        )

        result = await agent.ainvoke(prompt, config)

        return {
            "web_search": result["messages"][-1].content,
        }  # type: ignore
