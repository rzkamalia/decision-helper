from src.modules.agents.decision_generator_agent import DecisionGeneratorAgent
from src.modules.agents.question_generator_agent import QuestionGeneratorAgent
from src.modules.agents.web_search_agent import WebSearchAgent
from src.modules.tools.image_understanding_tool import image_understanding
from src.modules.tools.web_search_tool import web_search


class Agents:
    def __init__(self):
        self._decision_generator_agent = DecisionGeneratorAgent()
        self._question_generator_agent = QuestionGeneratorAgent()
        self._web_search_agent = WebSearchAgent(tools=[web_search])

    async def generate_image_question_agents(
        self, context: str, options: list[str]
    ) -> tuple[list, list[dict[str, str | list]]]:
        image_content = [image_understanding(option) for option in options]
        questions = await self._question_generator_agent.image_node(context=context, options=image_content)
        questions = [
            {
                "question": question.question,
                "answer_choices": question.answer_choices,
            }
            for question in questions.questions
        ]

        return image_content, questions

    async def generate_question_agents(
        self, context: str, options: list[str]
    ) -> tuple[str, list[dict[str, str | list]]]:
        web_search_content = await self._web_search_agent.node(context=context, options=options)
        questions = await self._question_generator_agent.node(
            context=context, options=options, web_search_content=web_search_content
        )
        questions = [
            {
                "question": question.question,
                "answer_choices": question.answer_choices,
            }
            for question in questions.questions
        ]

        return web_search_content, questions

    async def generate_decision_agents(
        self,
        context: str,
        options: list[str],
        question_answer_pairs: list[dict[str, str]],
        image_content: list[str],
        web_search_content: str,
    ) -> dict[str, int | str]:
        print(type(context))
        print(type(options))
        print(type(question_answer_pairs))
        print(type(image_content))
        print(type(web_search_content))

        decision = await self._decision_generator_agent.node(
            context=context,
            options=options,
            question_answer_pairs=question_answer_pairs,
            image_content=image_content,
            web_search_content=web_search_content,
        )
        if len(image_content) == 0:
            decision = {
                "chosen_option": decision.chosen_option,
                "reason": decision.reason,
            }
            return decision

        chosen_option = decision.chosen_option
        number = int(chosen_option.split(" ")[-1])

        decision = {
            "chosen_option": options[number - 1],
            "reason": decision.reason,
        }
        return decision
