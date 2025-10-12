from strands import Agent
from services.lm_studio_ai import LMStudioAIService

from domain.tools.api_tools import data_gatherer_agent_tools

from domain.prompts.data_gatherer import DATA_GATHERER_SYSTEM_INSTRUCTION
from domain.prompts.orchestrator import ORCHESTRATOR_SYSTEM_INSTRUCTION
from domain.prompts.ui_smith import UI_SMITH_SYSTEM_INSTRUCTIONS

from shared.logger import Logger
logger = Logger()


system_instructions = {
    "DATA_GATHERER": DATA_GATHERER_SYSTEM_INSTRUCTION,
    "ORCHESTRATOR": ORCHESTRATOR_SYSTEM_INSTRUCTION,
    "UI_SMITH": UI_SMITH_SYSTEM_INSTRUCTIONS
}


agent_tools = {
    "DATA_GATHERER": data_gatherer_agent_tools(),
    "ORCHESTRATOR": [],
    "UI_SMITH": []
}


class AgentFactory:
    def __init__(self, agent_name: str, callback_handler=None):
        self.agentic_ai = None
        self.callback_handler = callback_handler

        self.lm_studio = LMStudioAIService(
            agent_name=agent_name
        )
        self.llm_model = self.lm_studio.initialize_llm()

        self.system_prompt = self.get_system_prompt(
            agent_name=agent_name
        )
        self.tools = self.get_tools(
            agent_name=agent_name
        )


    def get_system_prompt(self, agent_name: str):
        try:
            if not agent_name in system_instructions:
                raise ValueError(f"Agent '{agent_name}' not found in system instructions.")
            
            return system_instructions[agent_name]
        except Exception as e:
            logger.error("Error while getting system prompt", str(e))
            raise e
        
    
    def get_tools(self, agent_name: str):
        try:
            if not agent_name in agent_tools:
                raise ValueError(f"Agent '{agent_name}' not found in agent tools.")
            
            return agent_tools[agent_name]
        except Exception as e:
            logger.error("Error while getting tools", str(e))
            raise e
        
    def agent(self) -> Agent:
        try:
            if self.agentic_ai:
                return self.agentic_ai

            self.agentic_ai = Agent(
                model=self.llm_model,
                system_prompt=self.system_prompt,
                callback_handler=self.callback_handler,
                tools=self.tools
            )
            return self.agentic_ai
        except Exception as e:
            logger.error("Error while creating agent", str(e))
            raise e