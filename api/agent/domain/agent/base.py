from strands import Agent
from services.lm_studio_ai import LMStudioAIService
from domain.use_cases.callback_handler import AgentCallbackHandler, SilentCallbackHandler

from shared.logger import Logger
logger = Logger()

class AgentFactory:
    def __init__(
        self,
        system_prompt: str,
        model_name: str,
        agent_id: str,
        shared_callback: AgentCallbackHandler,
        silent: bool = False,
        tool_list: list = None,
    ):
        self.agentic_ai = None
        self.system_prompt = system_prompt
        self.tool_list = tool_list or []

        self.callback_handler = SilentCallbackHandler(
            callback=shared_callback,
            agent_id=agent_id,
            silent=silent,
        )

        self.lm_studio = LMStudioAIService()
        self.llm_model = self.lm_studio.initialize_llm(model_name=model_name)

        
    def create_agent(self) -> Agent:
        try:
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