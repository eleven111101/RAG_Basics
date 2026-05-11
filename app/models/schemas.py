from pydantic import BaseModel
from typing import Dict


class Scenario(BaseModel):
    sheet_name: str
    scenario_id: str
    scenario_title_jp: str
    parameters: Dict[str, str]