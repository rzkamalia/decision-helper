from textwrap import dedent

from agents import Agent, Runner

from src.modules.schemas.question_generator_schema import Questions


class QuestionGeneratorAgent:
    def __init__(self):
        self._agent = Agent(
            name="Question Generator Agent",
            instructions=dedent(
                """
                # Role
                You are an intelligent assistant that helps users choose between multiple alternatives by asking insightful follow-up questions.

                # Language
                All response must be in English.

                # Instructions
                1. Identify the **options** and the surrounding **context** provided by the user.
                2. Use this information, along with any relevant **web search results**, to generate a set of **thoughtful, unbiased, and context-aware questions** that help the user narrow down their preferences or requirements.
                3. Aim to generate between **3 and 10 questions**, depending on the complexity and ambiguity of the context — focus on **relevance and clarity**, not quantity.
                4. All questions must be in the form of a **radio group**.
                5. **DO NOT**:
                    - Mention the options directly in any of the questions or answers.
                    - Ask leading questions that hint at or favor any specific option.
                    Instead, guide the user through **indirect questioning** that helps uncover their priorities, constraints, and preferences.
                6. Make the questions as **engaging and thought-provoking** as possible to encourage meaningful reflection from the user.
                """  # noqa: E501
            ).strip(),
            output_type=Questions,
            model="gpt-5-mini-2025-08-07",
        )

        self._image_agent = Agent(
            name="Image Question Generator Agent",
            instructions=dedent(
                """
                # Role
                You are an intelligent assistant that helps users choose between multiple alternative images by asking insightful follow-up questions.

                # Language
                All responses must be in English.

                # Instructions
                1. Identify **each image's description** and the surrounding **context** provided by the user.
                2. Use this information to generate a set of thoughtful, unbiased, and context-aware questions that help the user narrow down their preferences or requirements.
                3. Aim to generate between **3 and 10 questions**, depending on the complexity and ambiguity of the context — focus on **relevance and clarity**, not quantity.
                4. All questions must be in the form of a **radio group**.
                5. **DO NOT**:
                    - Mention the options directly in any of the questions or answers.
                    - Ask leading questions that hint at or favor any specific option.
                    Instead, guide the user through **indirect questioning** that helps uncover their priorities, constraints, and preferences.
                6. Make the questions as **engaging and thought-provoking** as possible to encourage meaningful reflection from the user.
                """  # noqa: E501
            ).strip(),
            output_type=Questions,
            model="gpt-5-mini-2025-08-07",
        )

    async def node(self, context: str, options: list[str], web_search_content: str) -> Questions:
        options_str = ""
        for i, option in enumerate(options, 1):
            options_str += f"""
            Option {i}. {option}
            """

        input_text = dedent(
            f"""
            # Options
            {options_str}

            # Context
            {context}

            # Web Search Result
            {web_search_content}
            """,
        ).strip()
        result: Questions = await Runner.run(self._agent, input_text)

        return result.final_output

    async def image_node(self, context: str, options: list[str]) -> Questions:
        options_str = ""
        for i, option in enumerate(options, 1):
            options_str += f"""
            Image {i}\nImage Description: {option}\n\n
            """

        input_text = dedent(
            f"""
            # Image
            {options_str}

            # Context
            {context}
            """,
        ).strip()
        result: Questions = await Runner.run(self._image_agent, input_text)

        return result.final_output
