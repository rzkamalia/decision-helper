from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.config import RunnableConfig

from src.modules.agents.base_agent import BaseAgent
from src.modules.schemas.decision_generator_schema import Decision, DecisionGeneratorState


class DecisionGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()  # Ensure BaseAgent is initialized


    def _system_prompt(self) -> str:
        return dedent(
            """
            # Role
            You are an expert decision-making assistant. Your job is to help the user select the most suitable option based on their context and preferences.

            # Instructions
            1. Carefully analyze all available options.
            2. Consider the user's context (concerns, goals, or preferences).
            3. Take into account the user's answers to follow-up questions.
            4. Return your response in the following structured format:
                - chosen_option: <the most suitable option>
                - reason: <a cponcise explanation with one paragraph based on the user's context and answers>
            5. Be fair and objective. Do not return vague responses like "it depends" or "there is no best choice".
            """, # noqa: E501
        ).strip()


    def _human_prompt(self) -> str:
        return dedent(
            """
            # Available Options
            {options}

            # User's Context or Concern
            {context}

            # User's Answers to Follow-Up Questions
            {question_answer_pairs}

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

    async def node(self, state: DecisionGeneratorState, config: RunnableConfig) -> DecisionGeneratorState:
        """Generate decision node.

        Args:
            state (DecisionGeneratorState): The state of the agent.
            config (RunnableConfig): The configuration of the agent.

        Returns:
            DecisionGeneratorState: The state of the agent.
        """
        context = state["context"]
        options = state["options"]
        web_search = state["web_search"]
        question_answer_pairs = state["question_answer_pairs"]

        question_answer_pairs_str = "\n".join(
            f"{i}. Question: {qa['question']}\n   User's Answer: {qa['answer']}"
            for i, qa in enumerate(question_answer_pairs, 1)
        )

        prompt = await self._get_prompt().ainvoke(
            {"context": context, "options": options, "web_search": web_search, "question_answer_pairs": question_answer_pairs_str},
            config,
        )

        llm = self.get_llm()
        result: Decision = await llm.with_structured_output(Decision).ainvoke(
            input=prompt,
            config=config,
        )  # type: ignore

        return {
            "chosen_option": result.chosen_option,
            "reason": result.reason,
        }  # type: ignore
