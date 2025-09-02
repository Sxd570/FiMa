from strands import Agent
from services.lm_studio_ai import LMStudioAIService
from pathlib import Path
from shared.logger import Logger
from domain.tools.budget_tools import BudgetTools
from domain.tools.goal_tools import GoalTools
from domain.tools.transaction_tools import TransactionTools

logger = Logger(__name__)


class InsightBot:
    def __init__(self):
        self.system_prompt = self.get_system_prompt()
        self.lm_studio = LMStudioAIService()
        self.llm_model = self.lm_studio.initialize_llm()
        self.insightbot = None

        self.budget_tools = BudgetTools()
        self.goal_tools = GoalTools()
        self.transaction_tools = TransactionTools()

    def get_system_prompt(self):
        try:
            prompt_path = Path(__file__).with_name("PROMPT.md")
            prompt = prompt_path.read_text(encoding="utf-8")
            return prompt
        except Exception as e:
            logger.error("Error while getting system prompt", str(e))
            raise e
        
    def extract_tools(self, obj):
        tools = []
        for attr_name in dir(obj):
            attr = getattr(obj, attr_name)
            if hasattr(attr, "_tool_spec"):
                tools.append(attr)
        return tools
    

    def agent(self):
        try:
            
            self.tools = (
                self.extract_tools(self.budget_tools) +
                self.extract_tools(self.goal_tools) +
                self.extract_tools(self.transaction_tools)
            )

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