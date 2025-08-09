from textwrap import dedent

from agents import Agent, Runner

from src.modules.schemas.decision_generator_schema import Decision


class DecisionGeneratorAgent:
    def __init__(self):
        self.agent = Agent(
            name="Decision Generator Agent",
            instructions=dedent(
                """
                # Role
                You are an expert decision-making assistant. Your job is to help the user select the most suitable option based on their context and preferences.

                # Language
                All response must be in English.

                # Instructions
                1. Carefully analyze all available options.
                2. Consider the user's context (concerns, goals, or preferences).
                3. Take into account the user's answers to follow-up questions.
                4. Return your response in the following structured format:
                    - chosen_option: <the most suitable option>
                    - reason: <a cponcise explanation with one paragraph based on the user's context and answers>
                5. Be fair and objective. Do not return vague responses like "it depends" or "there is no best choice".
                """  # noqa: E501
            ).strip(),
            output_type=Decision,
            model="gpt-5-mini",
        )

        self.image_agent = Agent(
            name="Decision Generator Agent",
            instructions=dedent(
                """
                # Role
                You are an expert decision-making assistant. Your job is to help the user select the most suitable option based on their context and preferences.

                # Language
                All response must be in English.

                # Instructions
                1. Carefully analyze all available options.
                2. Consider the user's context (concerns, goals, or preferences).
                3. Take into account the user's answers to follow-up questions.
                4. Return your response in the following structured format:
                    - chosen_option: <the most suitable option — specify the image number only, without its description>
                    - reason: <a cponcise explanation with one paragraph based on the user's context and answers>
                5. Be fair and objective. Do not return vague responses like "it depends" or "there is no best choice".
                """  # noqa: E501
            ).strip(),
            output_type=Decision,
            model="gpt-5-mini",
        )

    async def node(
        self,
        context: str,
        options: list[str],
        question_answer_pairs: list[dict[str, str]],
        image_content: list[str],
        web_search_content: str,
    ) -> Decision:
        question_answer_pairs_str = "\n".join(
            f"{i}. Question: {qa['question']}\n   User's Answer: {qa['answer']}"
            for i, qa in enumerate(question_answer_pairs, 1)
        )

        if len(image_content) == 0:
            options_str = ""
            for i, option in enumerate(options, 1):
                options_str += f"""
                Option {i}. {option}
                """
            input_text = dedent(
                f"""
                # Available Options
                {options_str}

                # User's Context or Concern
                {context}

                # User's Answers to Follow-Up Questions
                {question_answer_pairs_str}

                # Web Search Result
                {web_search_content}
                """,
            ).strip()
            result: Decision = await Runner.run(self.agent, input_text)
        else:
            options_str = ""
            for i, option in enumerate(image_content, 1):
                options_str += f"""
                Image {i}\nImage Description: {option}\n\n
                """

            input_text = dedent(
                f"""
                # Available Options
                {options_str}

                # User's Context or Concern
                {context}

                # User's Answers to Follow-Up Questions
                {question_answer_pairs_str}
                """,
            ).strip()

            result: Decision = await Runner.run(self.image_agent, input_text)

        return result.final_output
