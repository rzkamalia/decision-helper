from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.config import RunnableConfig

from src.modules.agents.base_agent import BaseAgent
from src.modules.schemas.question_generator_schema import (
    QuestionGeneratorState,
    Questions,
)


class QuestionGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()  # Ensure BaseAgent is initialized

    def _system_prompt(self) -> str:
        return dedent(
            """
            # Role
            You are an intelligent assistant that helps users choose between multiple alternatives by asking insightful follow-up questions.

            # Instructions
            1. Identify the **options** and the surrounding **context** provided by the user.
            2. Use this information, along with any relevant **web search results**, to generate **a set of thoughtful, unbiased, and context-aware questions** that help the user narrow down their preferences or requirements.
            3. Aim to generate between 3 and 10 questions, depending on the complexity and ambiguity of the context — focus on relevance and clarity, not quantity.
            4. **Do not mention the options directly in any of the questions or answers.** Instead, guide the user through indirect questioning that reveals their priorities and constraints.
            """, # noqa: E501
        ).strip()

    def _human_prompt(self) -> str:
        return dedent(
            """
            # Options
            {options}

            # Context
            {context}

            # Web Search Result
            {web_search}
            """,
        ).strip()

    def _get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self._system_prompt()),
                HumanMessagePromptTemplate.from_template(self._human_prompt()),
            ],
        )

    async def node(self, state: QuestionGeneratorState, config: RunnableConfig) -> QuestionGeneratorState:
        """Generate question node.

        Args:
            state (QuestionGeneratorState): The state of the agent.
            config (RunnableConfig): The configuration of the agent.

        Returns:
            QuestionGeneratorState: The state of the agent.
        """
        context = state["context"]
        options = state["options"]
        web_search = state["web_search"]

        prompt = await self._get_prompt().ainvoke(
            {"context": context, "options": options, "web_search": web_search},
            config,
        )

        llm = self.get_llm()
        result: Questions = await llm.with_structured_output(Questions).ainvoke(
            input=prompt,
            config=config,
        )  # type: ignore

        return {
            "questions": result.questions,
        }  # type: ignore
