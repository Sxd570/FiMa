from pydantic import BaseSettings, Field
from strands.models.openai import OpenAIModel


class LMStudioAIConfig(BaseSettings):
    model_name: str = Field(..., env="MODEL_NAME", description="Model name or ID")
    base_url: str = Field(..., env="LM_STUDIO_BASE_URL", description="Base URL of the LM Studio instance")
    port: int = Field(..., env="LM_STUDIO_PORT", description="Port number of the LM Studio instance")
    temperature: float = Field(..., env="MODEL_TEMPERATURE", description="Temperature for model responses")
    api_key: str = Field(..., env="API_KEY", description="API key for authentication")
    version: str = Field(..., env="LM_STUDIO_API_VERSION", description="API version for LM Studio")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class LMStudioAIService:
    def __init__(self):
        self.config = LMStudioAIConfig()
        self.llm = None


    def initialize_llm(self):
        try:
            if not self.llm:
                self.llm = OpenAIModel(
                    model_id = self.config.model_name,
                    client_args = {
                        "base_url": f"{self.config.base_url}:{self.config.port}/{self.config.version}",
                        "api_key": self.config.api_key
                    },
                    temperature = self.config.temperature
                )
            return self.llm
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            return None


# Example usage:
# if __name__ == "__main__":
#     service = LMStudioAIService(agent_name="agent_penny")
#     print(service.config)
