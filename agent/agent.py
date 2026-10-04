import argparse
import json
import os

from .planner import build_deterministic_plan
from .policy import validate_plan
from .tools import host_facts, validate_package

def main():
    parser = argparse.ArgumentParser(description="Splunk AI Install Agent")
    parser.add_argument("--request", required=True)
    parser.add_argument("--package",
                        default=os.getenv("SPLUNK_PACKAGE_PATH",
                                           "/tmp/splunk-package.tgz"))
    parser.add_argument("--splunk-home", default="/opt/splunk")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    facts = host_facts()
    package = validate_package(args.package)
    plan = build_deterministic_plan(
        args.request, args.package, args.splunk_home
    )
    valid, errors = validate_plan(plan)

    report = {
        "host_facts": facts,
        "package": package,
        "plan": plan.model_dump(),
        "policy_valid": valid,
        "policy_errors": errors,
    }

    if not valid:
        print(json.dumps(report, indent=2))
        raise SystemExit(2)

    if args.execute and not args.plan_only:
        if not package["exists"]:
            raise SystemExit(
                f"Approved execution requested, but package does not exist: "
                f"{args.package}"
            )
        print("Execution gate reached.")
        print("Connect an approved executor (for example Ansible) after reviewing the plan.")
        report["execution"] = "not executed - executor backend not configured"

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
