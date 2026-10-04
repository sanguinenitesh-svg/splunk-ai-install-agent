import platform
from pathlib import Path
from .schemas import InstallPlan

def build_deterministic_plan(request: str, package_path: str,
                             splunk_home: str = "/opt/splunk"):
    return InstallPlan(
        target_os=platform.system().lower(),
        splunk_home=splunk_home,
        package_path=str(Path(package_path).resolve()),
        actions=[
            "validate_os",
            "validate_package",
            "create_user",
            "install_splunk",
            "enable_boot_start",
            "verify_service",
            "verify_management_port",
        ],
        firewall_changes=False,
        requires_approval=True,
        rationale=f"Plan generated for request: {request}",
    )
