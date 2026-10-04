from pathlib import Path
from .schemas import InstallPlan

SAFE_ACTIONS = {
    "validate_os",
    "validate_package",
    "create_user",
    "install_splunk",
    "enable_boot_start",
    "verify_service",
    "verify_management_port",
}

def validate_plan(plan: InstallPlan) -> tuple[bool, list[str]]:
    errors = []
    unknown = set(plan.actions) - SAFE_ACTIONS
    if unknown:
        errors.append(f"Unsupported actions: {sorted(unknown)}")
    if plan.firewall_changes:
        errors.append("Firewall changes are disabled by default.")
    if not Path(plan.package_path).is_absolute():
        errors.append("package_path must be an absolute local path.")
    return not errors, errors
