from strands import Agent
from services.lm_studio_ai import LMStudioAIService
from pathlib import Path
from shared.logger import Logger

logger = Logger(__name__)


class InsightBot:
    def __init__(self):
        self.system_prompt = self.get_system_prompt()
        self.lm_studio = LMStudioAIService()
        self.llm_model = self.lm_studio.initialize_llm()
        self.insightbot = None

    def get_system_prompt(self):
        try:
            prompt_path = Path(__file__).with_name("PROMPT.md")
            prompt = prompt_path.read_text(encoding="utf-8")
            return prompt
        except Exception as e:
            logger.error("Error while getting system prompt", str(e))
            raise e

    def agent(self):
        try:
            if self.insightbot:
                return self.insightbot
            
            self.insightbot = Agent(
                model=self.llm_model,
                system_prompt=self.system_prompt,
                callback_handler=None 
            )
            return self.insightbot
        except Exception as e:
            logger.error("Error while creating agent", str(e))
            raise e