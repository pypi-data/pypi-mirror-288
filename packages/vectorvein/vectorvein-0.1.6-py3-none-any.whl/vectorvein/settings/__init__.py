# @Author: Bi Ying
# @Date:   2024-07-27 00:30:56
from typing import List, Dict

from pydantic import BaseModel, Field

from ..types import defaults as defs
from ..types.enums import BackendType
from ..types.llm_parameters import BackendSettings, EndpointSetting


class Settings(BaseModel):
    endpoints: List[EndpointSetting] = Field(
        default_factory=list, description="Available endpoints for the LLM service."
    )

    anthropic_models: BackendSettings = Field(
        default_factory=BackendSettings, description="Anthropic models settings."
    )
    deepseek_models: BackendSettings = Field(default_factory=BackendSettings, description="Deepseek models settings.")
    gemini_models: BackendSettings = Field(default_factory=BackendSettings, description="Gemini models settings.")
    groq_models: BackendSettings = Field(default_factory=BackendSettings, description="Groq models settings.")
    local_models: BackendSettings = Field(default_factory=BackendSettings, description="Local models settings.")
    minimax_models: BackendSettings = Field(default_factory=BackendSettings, description="Minimax models settings.")
    mistral_models: BackendSettings = Field(default_factory=BackendSettings, description="Mistral models settings.")
    moonshot_models: BackendSettings = Field(default_factory=BackendSettings, description="Moonshot models settings.")
    openai_models: BackendSettings = Field(default_factory=BackendSettings, description="OpenAI models settings.")
    qwen_models: BackendSettings = Field(default_factory=BackendSettings, description="Qwen models settings.")
    yi_models: BackendSettings = Field(default_factory=BackendSettings, description="Yi models settings.")
    zhipuai_models: BackendSettings = Field(default_factory=BackendSettings, description="Zhipuai models settings.")

    def __init__(self, **data):
        model_types = {
            "anthropic_models": defs.ANTHROPIC_MODELS,
            "deepseek_models": defs.DEEPSEEK_MODELS,
            "gemini_models": defs.GEMINI_MODELS,
            "groq_models": defs.GROQ_MODELS,
            "local_models": {},
            "minimax_models": defs.MINIMAX_MODELS,
            "mistral_models": defs.MISTRAL_MODELS,
            "moonshot_models": defs.MOONSHOT_MODELS,
            "openai_models": defs.OPENAI_MODELS,
            "qwen_models": defs.QWEN_MODELS,
            "yi_models": defs.YI_MODELS,
            "zhipuai_models": defs.ZHIPUAI_MODELS,
        }

        for model_type, default_models in model_types.items():
            if model_type in data:
                model_settings = BackendSettings()
                model_settings.update_models(default_models, data[model_type])
                data[model_type] = model_settings
            else:
                data[model_type] = BackendSettings(models=default_models)

        super().__init__(**data)

    def load(self, settings_dict: Dict):
        self.__init__(**settings_dict)

    def get_endpoint(self, endpoint_id: str) -> EndpointSetting:
        for endpoint in self.endpoints:
            if endpoint.id == endpoint_id:
                return endpoint
        return EndpointSetting()

    def get_backend(self, backend: BackendType) -> BackendSettings:
        return getattr(self, f"{backend.value.lower()}_models")


settings = Settings()
