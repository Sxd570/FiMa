from strands import Agent
from services.lm_studio_ai import LMStudioAIService
from pathlib import Path
from shared.logger import Logger
from domain.tools import insight_tools

logger = Logger(__name__)


class InsightBot:
    def __init__(self):
        self.insightbot = None

        self.system_prompt = self.get_system_prompt()

        self.lm_studio = LMStudioAIService()
        self.llm_model = self.lm_studio.initialize_llm()

        self.tools = insight_tools()


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
                callback_handler=None,
                tools=self.tools
            )
            return self.insightbot
        except Exception as e:
            logger.error("Error while creating agent", str(e))
            raise e
        

# if __name__ == '__main__':
#     insight_bot = InsightBot()
#     agent = insight_bot.agent()
#     response = agent("can you tell me the all budgets details of user_id be2323eb-38ac-5a90-85a3-26b6f4fdfb25 for january 2025 and tell me how can i save up here")
#     print(response)