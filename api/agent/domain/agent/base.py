from strands import Agent
from services.lm_studio_ai import LMStudioAIService

from shared.logger import Logger
logger = Logger()

class AgentFactory:
    def __init__(self, system_prompt: str, tool_list: list = None, callback_handler=None):
        self.agentic_ai = None
        self.callback_handler = callback_handler
        self.system_prompt = system_prompt
        self.tool_list = tool_list or []

        self.lm_studio = LMStudioAIService()
        self.llm_model = self.lm_studio.initialize_llm()

        
    def create_agent(self) -> Agent:
        try:
            if self.agentic_ai:
                return self.agentic_ai

            self.agentic_ai = Agent(
                model=self.llm_model,
                system_prompt=self.system_prompt,
                callback_handler=self.callback_handler,
                tools=self.tool_list
            )
            return self.agentic_ai
        except Exception as e:
            logger.error("Error while creating agent", str(e))
            raise e