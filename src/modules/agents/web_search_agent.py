from textwrap import dedent

from agents import Agent, ModelSettings, Runner


class WebSearchAgent:
    def __init__(self, tools: list):
        self._agent = Agent(
            name="Web Search Agent",
            instructions=dedent(
                """
                Conduct a search about the provided options within the given context.
                """
            ).strip(),
            tools=tools,
            model="gpt-5-mini-2025-08-07",
            model_settings=ModelSettings(tool_choice="web_search")
        )

    async def node(self, context: str, options: list[str]) -> str:
        input_text = dedent(
            f"""
            # Options
            {", ".join(options)}

            # Context: {context}
            """
        ).strip()
        result = await Runner.run(self._agent, input_text)

        return result.final_output
