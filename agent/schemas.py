from typing import List
from pydantic import BaseModel, Field

class InstallPlan(BaseModel):
    target_os: str = "unknown"
    splunk_home: str = "/opt/splunk"
    package_path: str
    actions: List[str] = Field(default_factory=list)
    firewall_changes: bool = False
    requires_approval: bool = True
    rationale: str = ""
