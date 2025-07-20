
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

from src.modules.agents.decision_generator_agent import DecisionGeneratorAgent
from src.modules.agents.question_generator_agent import QuestionGeneratorAgent
from src.modules.agents.web_search_agent import WebSearchAgent
from src.modules.schemas.decision_generator_schema import DecisionGeneratorState
from src.modules.schemas.question_generator_schema import QuestionGeneratorState


class Graph:
    def __init__(self):
        self._question_generator_agent = QuestionGeneratorAgent()
        self._decision_generator_agent = DecisionGeneratorAgent()
        self._web_search_agent = WebSearchAgent()

    def generate_question_builder(self) -> StateGraph:
        builder = StateGraph(state_schema=QuestionGeneratorState)

        builder.add_node(
            "question_generator_agent",
            self._question_generator_agent.node,
            retry=RetryPolicy(max_attempts=3),
        )
        builder.add_node(
            "web_search_agent",
            self._web_search_agent.node,
            retry_policy=RetryPolicy(max_attempts=3),
        )

        builder.add_edge(START, "web_search_agent")
        builder.add_edge("web_search_agent", "question_generator_agent")
        builder.add_edge("question_generator_agent", END)

        return builder.compile()

    def generate_decision_builder(self) -> StateGraph:
        builder = StateGraph(state_schema=DecisionGeneratorState)

        builder.add_node(
            "decision_generator_agent",
            self._decision_generator_agent.node,
            retry=RetryPolicy(max_attempts=3),
        )

        builder.add_edge(START, "decision_generator_agent")
        builder.add_edge("decision_generator_agent", END)

        return builder.compile()

def generate_question_graph():
    return Graph().generate_question_builder()

def generate_decision_graph():
    return Graph().generate_decision_builder()
