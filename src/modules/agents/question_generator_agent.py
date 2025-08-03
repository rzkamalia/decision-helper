from textwrap import dedent

from agents import Agent, Runner

from src.modules.schemas.question_generator_schema import Questions


class QuestionGeneratorAgent:
    def __init__(self):
        self.agent = Agent(
            name="Question Generator Agent",
            instructions=dedent(
                """
                # Role
                You are an intelligent assistant that helps users choose between multiple alternatives by asking insightful follow-up questions.

                # Instructions
                1. Identify the **options** and the surrounding **context** provided by the user.
                2. Use this information, along with any relevant **web search results**, to generate a set of **thoughtful, unbiased, and context-aware questions** that help the user narrow down their preferences or requirements.
                3. Aim to generate between **3 and 10 questions**, depending on the complexity and ambiguity of the context — focus on **relevance and clarity**, not quantity.
                4. All questions must be in the form of a **radio group**.
                5. **Do not**:
                - Mention the options directly in any of the questions or answers.
                - Ask leading questions that hint at or favor any specific option.
                Instead, guide the user through **indirect questioning** that helps uncover their priorities, constraints, and preferences.
                6. Make the questions as **engaging and thought-provoking** as possible to encourage meaningful reflection from the user.
                """  # noqa: E501
            ).strip(),
            output_type=Questions,
            model="gpt-4.1-mini",
        )

    async def node(self, context: str, options: str, web_search_content: str) -> Questions:
        input_text = dedent(
            f"""
            # Options
            {options}

            # Context
            {context}

            # Web Search Result
            {web_search_content}
            """,
        ).strip()
        result: Questions = await Runner.run(self.agent, input_text)

        return result.final_output
