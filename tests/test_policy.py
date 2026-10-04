from agent.schemas import InstallPlan
from agent.policy import validate_plan

def test_safe_plan():
    plan = InstallPlan(package_path="/tmp/splunk.tgz")
    ok, errors = validate_plan(plan)
    assert ok
    assert errors == []

def test_relative_package_is_rejected():
    plan = InstallPlan(package_path="splunk.tgz")
    ok, errors = validate_plan(plan)
    assert not ok
    assert any("absolute" in e for e in errors)

def test_firewall_changes_are_rejected():
    plan = InstallPlan(package_path="/tmp/splunk.tgz", firewall_changes=True)
    ok, errors = validate_plan(plan)
    assert not ok
    assert any("Firewall" in e for e in errors)
