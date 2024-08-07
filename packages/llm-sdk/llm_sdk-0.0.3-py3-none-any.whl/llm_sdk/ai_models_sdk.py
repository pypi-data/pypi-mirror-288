import requests
from typing import List, Optional
from pydantic import parse_obj_as
from .schemas_sdk import AvailableModelModel, ProviderModel

class ModelsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_available_models(
            self, model_type_name: Optional[str] = None, provider_name: Optional[str] = None,
            is_verified: Optional[bool] = None
    ) -> List[AvailableModelModel]:
        params = {}
        if model_type_name:
            params['model_type_name'] = model_type_name
        if provider_name:
            params['provider_name'] = provider_name
        if is_verified is not None:
            params['is_verified'] = str(is_verified).lower()
        response = requests.get(f"{self.base_url}/available-models/", params=params)
        response.raise_for_status()
        return parse_obj_as(List[AvailableModelModel], response.json())

    def get_providers(self, model_type_name: Optional[str] = None) -> List[ProviderModel]:
        params = {}
        if model_type_name:
            params['model_type_name'] = model_type_name
        response = requests.get(f"{self.base_url}/providers/", params=params)
        response.raise_for_status()
        return parse_obj_as(List[ProviderModel], response.json())


ai_models = ModelsAPI('https://web-production-6c25.up.railway.app')
